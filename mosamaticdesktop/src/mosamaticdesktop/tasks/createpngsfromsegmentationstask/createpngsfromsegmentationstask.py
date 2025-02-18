import os
import numpy as np

from mosamaticdesktop.tasks.task import Task, TaskStatus
from mosamaticdesktop.utils import convert_numpy_array_to_png_image, AlbertaColorMap


class CreatePngsFromSegmentationsTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(CreatePngsFromSegmentationsTask, self).__init__(input_dir, output_dir_name, params)

    def execute(self):
        files = os.listdir(self.get_input_dir())
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 
            # Convert source image to PNG format and copy to output
            f = files[step]
            source = os.path.join(self.get_input_dir(), f)
            source_image = np.load(source)
            png_file_name = os.path.split(source)[1] + '.png'
            convert_numpy_array_to_png_image(
                source_image, 
                self.get_output_dir(), 
                AlbertaColorMap(), 
                png_file_name,
                fig_width=self.get_param('fig_width', 10),
                fig_height=self.get_param('fig_height', 10),
            )
            # Update progress
            self.set_progress(step, nr_steps)