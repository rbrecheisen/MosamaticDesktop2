import os
import time
import shutil
import pydicom

from mosamaticdesktop.tasks.task import Task, TaskStatus
from mosamaticdesktop.utils import is_dicom, is_jpeg2000_compressed


class CopyDicomFilesTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(CopyDicomFilesTask, self).__init__(input_dir, output_dir_name, params)

    def execute(self):
        files = os.listdir(self.input_dir())
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 

            # Copy source to target (if DICOM image). If DICOM image is compressed
            # and the 'decompress' parameter is True, decompress the image
            f = files[step]
            source = os.path.join(self.input_dir(), f)
            if is_dicom(source):
                target = os.path.join(self.output_dir(), f)
                if self.get_param('decompress', False):
                    p = pydicom.dcmread(source)
                    if is_jpeg2000_compressed(p):
                        p.decompress()
                    p.save_as(target)
                else:
                    shutil.copy(source, target)

            # Update progress
            self.set_progress(step, nr_steps)

            # Wait if delay was specified
            time.sleep(self.get_param('delay', 0))
