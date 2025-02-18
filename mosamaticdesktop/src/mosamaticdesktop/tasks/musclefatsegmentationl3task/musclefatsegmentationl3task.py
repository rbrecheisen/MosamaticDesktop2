import os
import numpy as np

from mosamaticdesktop.tasks.task import Task, TaskStatus
from mosamaticdesktop.tasks.musclefatsegmentationl3task.torchmodel import TorchModel
from mosamaticdesktop.tasks.musclefatsegmentationl3task.tensorflowmodel import TensorFlowModel
from mosamaticdesktop.utils import get_pixels_from_dicom_object, normalize_between, convert_labels_to_157, load_dicom


class MuscleFatSegmentationL3Task(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(MuscleFatSegmentationL3Task, self).__init__(input_dir, output_dir_name, params)

    def load_model_files(self, model_dir, model_type, model_version):
        if model_type == 'torch':
            torch_model = TorchModel()
            model, contour_model, params = torch_model.load(model_dir, model_version)
            return model, contour_model, params
        elif model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            model, contour_model, params = tensorflow_model.load(model_dir, model_version)
            return model, contour_model, params
        else:
            pass
        return None

    def predict_contour(self, contour_model, img, params, model_type):
        if model_type == 'torch':
            torch_model = TorchModel()
            mask = torch_model.predict_contour(img, contour_model, params)
            return mask
        elif model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            mask = tensorflow_model.predict_contour(img, contour_model, params)
            return mask
        else:
            pass
        return None

    def process_file(self, f_path, output_dir, model, contour_model, params, model_type):
        p = load_dicom(f_path)
        if p is None:
            self.log_info(f'File {f_path} is not valid DICOM, skipping...')
            return
        img1 = get_pixels_from_dicom_object(p, normalize=True)        
        if contour_model:
            mask = self.predict_contour(contour_model, img1, params, model_type)
            img1 = normalize_between(img1, params['min_bound'], params['max_bound'])
            img1 = img1 * mask
        img1 = img1.astype(np.float32)
        if model_type == 'torch':
            torch_model = TorchModel()
            pred_max = torch_model.predict(img1, model)
        elif model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            pred_max = tensorflow_model.predict(img1, model)
        else:
            pass
        pred_max = convert_labels_to_157(pred_max)
        segmentation_file_name = os.path.split(f_path)[1]
        segmentation_file_path = os.path.join(output_dir, f'{segmentation_file_name}.seg.npy')
        np.save(segmentation_file_path, pred_max)

    def execute(self):
        model_dir = self.get_param('model_dir', None)
        if not model_dir:
            self.set_status(TaskStatus.FAILED, message='Model directory not found')
        model_type = self.get_param('model_type', 'torch')
        self.log_info(f'Using model type: {model_type}')
        model_version = self.get_param('model_version', None)
        if model_version is None:
            self.set_status(TaskStatus.FAILED, message='Model version not specified')
        model, contour_model, params = self.load_model_files(model_dir, model_type, model_version)
        if model is None or params is None:
            self.set_status(TaskStatus.FAILED, message='Model or parameters could not be loaded')
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
            self.process_file(f_path, self.get_output_dir(), model, contour_model, params, model_type)
            self.set_progress(step, nr_steps)