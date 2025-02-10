import os
import json
import pydicom
import pydicom.errors
import torch

from mosamaticdesktop.tasks.task import Task, TaskStatus


class MuscleFatSegmentationTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(MuscleFatSegmentationTask, self).__init__(input_dir, output_dir_name, params)

    def load_model_files(self, model_dir):
        model, contour_model, params = None, None, None
        for f in os.listdir(model_dir):
            f_path = os.path.join(model_dir, f)
            if f.startswith('model'):
                model = torch.load(f_path)
                model.to('cpu')
                model.eval()
            elif f.startswith('contour_model'):
                contour_model = torch.load(f_path)
                contour_model.to('cpu')
                contour_model.eval()
            elif f == 'params.json':
                with open(f_path, 'r') as obj:
                    params = json.load(obj)
            else:
                pass
        return model, contour_model, params

    def execute(self):
        # Load PyTorch models and parameters
        model_dir = self.get_param('model_dir', None)
        if not model_dir:
            self.set_status(TaskStatus.FAILED, message='Model directory not found')
        model, contour_model, params = self.load_model_files(model_dir)
        if model is None or params is None:
            self.set_status(TaskStatus.FAILED, message='Model or parameters could not be loaded')

        # Process DICOM files (use CopyDicomFilesTask to ensure input directory with only DICOM)
        files = os.listdir(self.input_dir())
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 
            
            f = files[step]
            f_path = os.path.join(self.input_dir(), f)

            # Load DICOM image (assumes decompressed if needed, use CopyDicomFilesTask for this with 'decompressed' = true)
            # We also assume the images have dimensions 512 x 512. You can ensure this by first running the RescaleDicomFilesTask
            # with 'rows' = 512 and 'cols' = 512.
            p = pydicom.dcmread(f_path)

            # Process single file

            # Update progress
            self.set_progress(step, nr_steps)