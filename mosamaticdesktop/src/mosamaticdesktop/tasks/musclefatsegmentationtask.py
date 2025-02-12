import os
import json
import pydicom
import pydicom.errors
import torch
import cv2
import numpy as np

from torch.nn import MaxPool2d, Sequential, Conv2d, PReLU, BatchNorm2d, Dropout, ConvTranspose2d

from models import UNet
from mosamaticdesktop.tasks.task import Task, TaskStatus
from mosamaticdesktop.utils import (
    get_pixels_from_dicom_object, normalize_between, convert_labels_to_157,
    current_time_in_seconds, elapsed_time_in_seconds
)


class MuscleFatSegmentationTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(MuscleFatSegmentationTask, self).__init__(input_dir, output_dir_name, params)

    def load_model_files(self, model_dir):
        print('Loading model files...')
        start_time_total = current_time_in_seconds()
        model, contour_model, params = None, None, None
        for f in os.listdir(model_dir):
            f_path = os.path.join(model_dir, f)
            with torch.serialization.safe_globals([UNet, MaxPool2d, Sequential, Conv2d, PReLU, BatchNorm2d, Dropout, ConvTranspose2d]):
                if f.startswith('model'):
                    start_time_model = current_time_in_seconds()
                    model = torch.load(f_path, map_location=torch.device('cpu'))
                    model.to('cpu')
                    model.eval()
                    elapsed_time_model = elapsed_time_in_seconds(start_time_model)
                    print(f'load_model_files() Elapsed loading model: {elapsed_time_model} seconds')
                elif f.startswith('contour_model'):
                    start_time_contour_model = current_time_in_seconds()
                    contour_model = torch.load(f_path, map_location=torch.device('cpu'))
                    contour_model.to('cpu')
                    contour_model.eval()
                    elapsed_time_contour_model = elapsed_time_in_seconds(start_time_contour_model)
                    print(f'load_model_files() Elapsed loading contour model: {elapsed_time_contour_model} seconds')
                elif f == 'params.json':
                    with open(f_path, 'r') as obj:
                        params = json.load(obj)
                else:
                    pass
        elapsed_time_total = elapsed_time_in_seconds(start_time_total)
        print(f'load_model_files() Elapsed total: {elapsed_time_total}')
        return model, contour_model, params

    def predict_contour(self, contour_model, img, params) -> np.array:
        start_time_total = current_time_in_seconds()

        start_time_normalization = current_time_in_seconds()
        ct = np.copy(img)
        ct = normalize_between(ct, params['min_bound_contour'], params['max_bound_contour'])
        elapsed_time_normalization = elapsed_time_in_seconds(start_time_normalization)
        print(f'predict_contour() Elapsed time normalization: {elapsed_time_normalization}')
        
        start_time_resize = current_time_in_seconds()
        target_shape = (512, 512)  
        ct_resized = cv2.resize(ct, target_shape, interpolation=cv2.INTER_LINEAR)
        elapsed_time_resize = elapsed_time_in_seconds(start_time_resize)
        print(f'predict_contour() Elapsed time resize: {elapsed_time_resize}')
        
        start_time_upload_tensor = current_time_in_seconds()
        ct_resized_tensor = torch.tensor(ct_resized, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to('cpu')
        elapsed_time_upload_tensor = elapsed_time_in_seconds(start_time_upload_tensor)
        print(f'predict_contour() Elapsed time upload tensor: {elapsed_time_upload_tensor}')

        start_time_predict = current_time_in_seconds()
        with torch.no_grad():
            pred = contour_model(ct_resized_tensor).cpu().numpy()
        pred_max = pred.argmax(axis=1)
        elapsed_time_predict = elapsed_time_in_seconds(start_time_predict)
        mask = np.uint8(pred_max)
        print(f'predict_contour() Elapsed time predict: {elapsed_time_predict}')

        elapsed_time_total = elapsed_time_in_seconds(start_time_total)
        print(f'predict_contour() Elapsed time total: {elapsed_time_total}')
        return mask

    def process_file(self, f_path, output_dir, model, contour_model, params):
        start_time_total = current_time_in_seconds()

        start_time_predict_contour = current_time_in_seconds()
        p = pydicom.dcmread(f_path)
        img1 = get_pixels_from_dicom_object(p, normalize=True)
        if contour_model:
            mask = self.predict_contour(contour_model, img1, params)
            img1 = normalize_between(img1, params['min_bound'], params['max_bound'])
            img1 = img1 * mask
        img1 = img1.astype(np.float32)
        elapsed_time_predict_contour = elapsed_time_in_seconds(start_time_predict_contour)
        print(f'process_file() Elapsed time predict contour: {elapsed_time_predict_contour}')

        start_time_upload_tensor = current_time_in_seconds()
        img1_tensor = torch.tensor(img1, dtype=torch.float32).unsqueeze(0).to('cpu')
        elapsed_time_upload_tensor = elapsed_time_in_seconds(start_time_upload_tensor)
        print(f'process_file() Elapsed time upload tensor: {elapsed_time_upload_tensor}')

        start_time_predict = current_time_in_seconds()
        with torch.no_grad():
            pred = model(img1_tensor).cpu().numpy()
        pred_squeeze = np.squeeze(pred)
        pred_max = pred_squeeze.argmax(axis=0)
        pred_max = convert_labels_to_157(pred_max)
        elapsed_time_predict = elapsed_time_in_seconds(start_time_predict)
        print(f'process_file() Elapsed time predict: {elapsed_time_predict}')

        segmentation_file_name = os.path.split(f_path)[1]
        segmentation_file_path = os.path.join(output_dir, f'{segmentation_file_name}.seg.npy')
        np.save(segmentation_file_path, pred_max)
        elapsed_time_total = elapsed_time_in_seconds(start_time_total)
        print(f'process_file() Elapsed time total: {elapsed_time_total}')

    def execute(self):
        # Load PyTorch models and parameters
        model_dir = self.get_param('model_dir', None)
        if not model_dir:
            self.set_status(TaskStatus.FAILED, message='Model directory not found')
        model, contour_model, params = self.load_model_files(model_dir)
        if model is None or params is None:
            self.set_status(TaskStatus.FAILED, message='Model or parameters could not be loaded')

        # Process DICOM files (use CopyDicomFilesTask to ensure input directory with only DICOM)
        files = os.listdir(self.get_input_dir())
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 
            
            f = files[step]
            f_path = os.path.join(self.get_input_dir(), f)

            # Load DICOM image (assumes decompressed if needed, use CopyDicomFilesTask for this with 'decompressed' = true)
            # We also assume the images have dimensions 512 x 512. You can ensure this by first running the RescaleDicomFilesTask
            # with 'rows' = 512 and 'cols' = 512.
            self.process_file(f_path, self.get_output_dir(), model, contour_model, params)

            # Update progress
            self.set_progress(step, nr_steps)