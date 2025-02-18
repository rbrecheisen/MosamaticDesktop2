import os
import time
import shutil

from mosamaticdesktop.tasks.task import Task, TaskStatus


class CopyFilesTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(CopyFilesTask, self).__init__(input_dir, output_dir_name, params)

    def execute(self):
        files = os.listdir(self.get_input_dir())
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 
            # Copy source to target
            f = files[step]
            source = os.path.join(self.get_input_dir(), f)
            target = os.path.join(self.get_output_dir(), f)
            shutil.copy(source, target)
            # Update progress
            self.set_progress(step, nr_steps)
            # Wait if delay was specified
            time.sleep(self.get_param('delay', 0))
