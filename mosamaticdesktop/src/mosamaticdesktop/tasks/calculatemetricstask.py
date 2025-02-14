import os
import csv
import pydicom
import pydicom.errors
import pandas as pd
import numpy as np

from mosamaticdesktop.tasks.task import Task, TaskStatus
from mosamaticdesktop.utils import (
    calculate_area, calculate_index, calculate_mean_radiation_attenuation, get_pixels_from_dicom_object
)

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
    
    def load_patient_heights(self, f):
        with open(f, mode='r', encoding='utf-8') as f_obj:
            reader = csv.DictReader(f_obj)
            return [row for row in reader]
        
    def get_patient_height(self, file_name, patient_heights):
        for row in patient_heights:
            if row['file'] in file_name:
                return float(row['height'])
        return None
    
    def load_image(self, f):
        try:
            p = pydicom.dcmread(f)
            pixels = get_pixels_from_dicom_object(p, normalize=True)
            return pixels, p.PixelSpacing
        except pydicom.errors.InvalidDicomError:
            return None, None

    def load_segmentation(self, f):
        return np.load(f)
        
    def execute(self):
        img_seg_pairs = self.collect_img_seg_pairs(
            self.get_param('image_dir', None), self.get_input_dir())
        
        patient_heights = None
        patient_heights_file = self.get_param('patient_heights_file', None)
        if patient_heights_file:
            patient_heights = self.load_patient_heights(patient_heights_file)
            print(f'Patient heights: {patient_heights}')

        data = {
            'file': [], 
            'muscle_area': [], 'muscle_idx': [], 'muscle_ra': [],
            'vat_area': [], 'vat_idx': [], 'vat_ra': [],
            'sat_area': [], 'sat_idx': [], 'sat_ra': []
        }

        nr_steps = len(img_seg_pairs)
        for step in range(nr_steps):
            if self.is_canceled():
                self.set_status(TaskStatus.CANCELED)
                return
            
            # Load DICOM image
            image, pixel_spacing = self.load_image(img_seg_pairs[step][0])
            if image is None:
                self.set_status(TaskStatus.FAILED, f'Could not load DICOM image for file {img_seg_pairs[step][0]}')
                return
            
            # load segmentation mask
            segmentation = self.load_segmentation(img_seg_pairs[step][1])
            if segmentation is None:
                self.set_status(TaskStatus.FAILED, f'Could not load segmentation for file {img_seg_pairs[step][1]}')
                return
            
            # Calculate metrics
            file_name = os.path.split(img_seg_pairs[step][0])[1]

            muscle_area = calculate_area(segmentation, MUSCLE, pixel_spacing)
            muscle_idx = 0
            if patient_heights:
                muscle_idx = calculate_index(muscle_area, self.get_patient_height(file_name, patient_heights))
            muscle_ra = calculate_mean_radiation_attenuation(image, segmentation, MUSCLE)

            vat_area = calculate_area(segmentation, VAT, pixel_spacing)
            vat_idx = 0
            if patient_heights:
                vat_idx = calculate_index(vat_area, self.get_patient_height(file_name, patient_heights))
            vat_ra = calculate_mean_radiation_attenuation(image, segmentation, VAT)

            sat_area = calculate_area(segmentation, SAT, pixel_spacing)
            sat_idx = 0
            if patient_heights:
                sat_idx = calculate_index(sat_area, self.get_patient_height(file_name, patient_heights))
            sat_ra = calculate_mean_radiation_attenuation(image, segmentation, SAT)

            print(f'file: {file_name}, ' +
                  f'muscle_area: {muscle_area}, muscle_idx: {muscle_idx}, muscle_ra: {muscle_ra}, ' +
                  f'vat_area: {vat_area}, vat_idx: {vat_idx}, vat_ra: {vat_ra}, ' +
                  f'sat_area: {sat_area}, sat_idx: {sat_idx}, sat_ra: {sat_ra}')

            # Update dataframe data
            data['file'].append(file_name)
            data['muscle_area'].append(muscle_area)
            data['muscle_idx'].append(muscle_idx)
            data['muscle_ra'].append(muscle_ra)
            data['vat_area'].append(vat_area)
            data['vat_idx'].append(vat_idx)
            data['vat_ra'].append(vat_ra)
            data['sat_area'].append(sat_area)
            data['sat_idx'].append(sat_idx)
            data['sat_ra'].append(sat_ra)

            # Update progress
            self.set_progress(step, nr_steps)

        # Build dataframe
        csv_file_path = os.path.join(self.get_output_dir(), 'bc_metrics.csv')
        df = pd.DataFrame(data=data)
        df.to_csv(csv_file_path, index=False, sep=';')
        print(f'Saved CSV with body composition metrics in {csv_file_path}')