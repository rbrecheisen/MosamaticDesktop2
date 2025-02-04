import os
import time
import shutil

from mosamaticdesktop.tasks.task import Task


class CopyFilesTask(Task):
    def execute(self):
        for f in os.listdir(self.input_dir):
            source = os.path.join(self.input_dir, f)
            target = os.path.join(self.output_dir, f)
            shutil.copy(source, target)
            if self.params:
                if 'delay' in self.params.keys():
                    delay = int(self.params['delay'])
                    time.sleep(delay)