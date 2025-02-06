import os
import time
import shutil

from mosamaticdesktop.tasks.task import Task, TaskStatus


class CopyFilesTask(Task):
    def __init__(self, input_dir, output_dir, params=None):
        super(CopyFilesTask, self).__init__(input_dir, output_dir, params)

    def execute(self):
        files = os.listdir(self._input_dir)
        nr_steps = len(files)
        for step in range(nr_steps):
            if self._canceled:
                self.set_status(TaskStatus.CANCELED)
                return 
            f = files[step]
            source = os.path.join(self._input_dir, f)
            target = os.path.join(self._output_dir, f)
            shutil.copy(source, target)
            print(f'Copied {source} to {target}')
            self.progress.emit(int(((step + 1) / (nr_steps)) * 100))
            if self._params and 'delay' in self._params.keys():
                time.sleep(self._params['delay'])