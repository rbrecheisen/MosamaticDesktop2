import os
import shutil
import pydicom

from mosamaticdesktop.tasks.task import Task, TaskStatus
from mosamaticdesktop.utils import is_dicom, is_jpeg2000_compressed


class DecompressDicomFilesTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(DecompressDicomFilesTask, self).__init__(input_dir, output_dir_name, params)

    def execute(self):
        files = os.listdir(self.get_input_dir())
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 

            # Copy source to target (if DICOM image). If DICOM image is compressed
            # decompress the image and save it. If not, just copy the file.
            f = files[step]
            source = os.path.join(self.get_input_dir(), f)
            if is_dicom(source):
                target = os.path.join(self.get_output_dir(), f)
                p = pydicom.dcmread(source)
                if is_jpeg2000_compressed(p):
                    p.decompress()
                    p.save_as(target)
                else:
                    shutil.copy(source, target)

            # Update progress
            self.set_progress(step, nr_steps)