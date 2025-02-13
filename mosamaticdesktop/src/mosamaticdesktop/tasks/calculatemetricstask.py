import os
import shutil

from mosamaticdesktop.tasks.task import Task, TaskStatus


class CalculateMetricsTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(CalculateMetricsTask, self).__init__(input_dir, output_dir_name, params)

    def collect_img_seg_pairs(img_files, seg_files):
        for img_f in img_files:
            print(img_f)

    def execute(self):
        seg_files = os.listdir(self.get_input_dir())
        img_files = os.listdir(self.get_param('image_dir', None))
        img_seg_pairs = self.collect_img_seg_pairs(img_files, seg_files)

        nr_steps = len(img_seg_pairs)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return 

            # f = seg_files[step]
            # source = os.path.join(self.get_input_dir(), f)
            # target = os.path.join(self.get_output_dir(), f)
            # shutil.copy(source, target)

            # Update progress
            self.set_progress(step, nr_steps)