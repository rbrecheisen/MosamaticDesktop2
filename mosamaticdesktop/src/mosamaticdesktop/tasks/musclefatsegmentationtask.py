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
from mosamaticdesktop.utils import get_pixels_from_dicom_object, normalize_between, convert_labels_to_157


class MuscleFatSegmentationTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(MuscleFatSegmentationTask, self).__init__(input_dir, output_dir_name, params)

    def load_model_files(self, model_dir):
        model, contour_model, params = None, None, None
        for f in os.listdir(model_dir):
            with torch.serialization.safe_globals([UNet, MaxPool2d, Sequential, Conv2d, PReLU, BatchNorm2d, Dropout, ConvTranspose2d]):
                f_path = os.path.join(model_dir, f)
                if f.startswith('model'):
                    model = torch.load(f_path, map_location=torch.device('cpu'))
                    model.to('cpu')
                    model.eval()
                elif f.startswith('contour_model'):
                    contour_model = torch.load(f_path, map_location=torch.device('cpu'))
                    contour_model.to('cpu')
                    contour_model.eval()
                elif f == 'params.json':
                    with open(f_path, 'r') as obj:
                        params = json.load(obj)
                else:
                    pass
        return model, contour_model, params

    def predict_contour(self, contour_model, img, params) -> np.array:
        ct = np.copy(img)
        ct = normalize_between(ct, params['min_bound_contour'], params['max_bound_contour'])
        target_shape = (512, 512)  
        ct_resized = cv2.resize(ct, target_shape, interpolation=cv2.INTER_LINEAR)
        ct_resized_tensor = torch.tensor(ct_resized, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to('cpu')
        with torch.no_grad():
            pred = contour_model(ct_resized_tensor).cpu().numpy()
        pred_max = pred.argmax(axis=1)
        mask = np.uint8(pred_max)
        return mask

    def process_file(self, f_path, output_dir, model, contour_model, params):
        p = pydicom.dcmread(f_path)
        img1 = get_pixels_from_dicom_object(p, normalize=True)
        if contour_model:
            mask = self.predict_contour(contour_model, img1, params)
            img1 = normalize_between(img1, params['min_bound'], params['max_bound'])
            img1 = img1 * mask
        img1 = img1.astype(np.float32)
        img1_tensor = torch.tensor(img1, dtype=torch.float32).unsqueeze(0).to('cpu')
        with torch.no_grad():
            pred = model(img1_tensor).cpu().numpy()
        pred_squeeze = np.squeeze(pred)
        segmentation_file_path = None
        pred_max = pred_squeeze.argmax(axis=0)
        pred_max = convert_labels_to_157(pred_max)
        segmentation_file_name = os.path.split(f_path)[1]
        segmentation_file_path = os.path.join(output_dir, f'{segmentation_file_name}.seg.npy')
        np.save(segmentation_file_path, pred_max)
        print(f'Saved segmentation: {segmentation_file_path}')

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