import os
import time
import shutil
import pydicom
import numpy as np

from scipy.ndimage import zoom

from mosamaticdesktop.tasks.task import Task, TaskStatus


class RescaleDicomFilesTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(RescaleDicomFilesTask, self).__init__(input_dir, output_dir_name, params)

    def process_file(self, f_name, target_size, input_dir, output_dir):
        source = os.path.join(input_dir, f_name)
        p = pydicom.dcmread(source)
        if p.Rows != target_size or p.Columns != target_size:
            pixel_array = p.pixel_array
            hu_array = pixel_array * p.RescaleSlope + p.RescaleIntercept
            hu_air = -1000
            new_rows = max(p.Rows, p.Columns)
            new_cols = max(p.Rows, p.Columns)
            padded_hu_array = np.full((new_rows, new_cols), hu_air, dtype=hu_array.dtype)
            padded_hu_array[:pixel_array.shape[0], :pixel_array.shape[1]] = hu_array
            pixel_array_padded = (padded_hu_array - p.RescaleIntercept) / p.RescaleSlope
            pixel_array_padded = pixel_array_padded.astype(pixel_array.dtype) # Image now has largest dimensions
            pixel_array_rescaled = zoom(pixel_array_padded, zoom=(target_size / new_rows), order=3) # Cubic interpolation
            pixel_array_rescaled = pixel_array_rescaled.astype(pixel_array.dtype)
            original_pixel_spacing = p.PixelSpacing
            new_pixel_spacing = [ps * (new_rows / target_size) for ps in original_pixel_spacing]
            p.PixelSpacing = new_pixel_spacing
            p.PixelData = pixel_array_rescaled.tobytes()
            p.Rows = target_size
            p.Columns = target_size
            items = os.path.splitext(f_name)
            target = os.path.join(output_dir, items[0] + f'_{target_size}' + items[1])
            p.save_as(target)
        else:
            target = os.path.join(output_dir, f_name)
            shutil.copy(source, target)

    def execute(self):
        files = os.listdir(self.get_input_dir())
        target_size = self.get_param('target_size', 512)
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 

            # Load DICOM image
            f = files[step]
            self.process_file(f, target_size, self.get_input_dir(), self.get_output_dir())

            # Update progress
            self.set_progress(step, nr_steps)

            # Wait if delay was specified
            time.sleep(self.get_param('delay', 0))
