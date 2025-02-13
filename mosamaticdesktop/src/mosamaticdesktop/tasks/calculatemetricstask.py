import os
import shutil

from mosamaticdesktop.tasks.task import Task, TaskStatus


class CalculateMetricsTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(CalculateMetricsTask, self).__init__(input_dir, output_dir_name, params)

    def execute(self):
        seg_files = os.listdir(self.get_input_dir())
        img_files = os.listdir(self.get_param('image_dir', None))
        nr_steps = len(seg_files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 

            # Copy source to target
            f = seg_files[step]
            source = os.path.join(self.get_input_dir(), f)
            target = os.path.join(self.get_output_dir(), f)
            shutil.copy(source, target)

            # Update progress
            self.set_progress(step, nr_steps)