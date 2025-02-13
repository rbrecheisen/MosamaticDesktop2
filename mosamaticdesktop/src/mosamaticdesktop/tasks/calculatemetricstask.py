import os
import shutil

from mosamaticdesktop.tasks.task import Task, TaskStatus

MUSCLE, VAT, SAT = 1, 5, 7


class CalculateMetricsTask(Task):
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(CalculateMetricsTask, self).__init__(input_dir, output_dir_name, params)

    def collect_img_seg_pairs(self, img_files_dir, seg_files_dir):
        img_seg_pairs = []
        for f_img in os.listdir(img_files_dir):
            f_img_path = os.path.join(img_files_dir, f_img)            
            for f_seg in os.listdir(seg_files_dir):
                if f_seg.removesuffix('.seg.npy') == f_img:
                    f_seg_path = os.path.join(seg_files_dir, f_seg)
                    img_seg_pairs.append((f_img_path, f_seg_path))
        return img_seg_pairs
        
    def execute(self):
        img_seg_pairs = self.collect_img_seg_pairs(
            self.get_param('image_dir', None), self.get_input_dir())
        patient_heights_file = self.get_param('patient_heights_file', None)
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