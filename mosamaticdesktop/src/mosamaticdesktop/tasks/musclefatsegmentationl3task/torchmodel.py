import os
import json
import torch
import cv2
import numpy as np

from models import UNet
from torch.nn import MaxPool2d, Sequential, Conv2d, PReLU, BatchNorm2d, Dropout, ConvTranspose2d

from mosamaticdesktop.utils import (
    get_pixels_from_dicom_object, normalize_between, convert_labels_to_157,
    current_time_in_seconds, elapsed_time_in_seconds, load_dicom, LOGGER
)


class TorchModel:
    def __init__(self):
        pass

    def load(self, model_dir):
        model, contour_model, params = None, None, None
        for f in os.listdir(model_dir):
            f_path = os.path.join(model_dir, f)
            with torch.serialization.safe_globals([UNet, MaxPool2d, Sequential, Conv2d, PReLU, BatchNorm2d, Dropout, ConvTranspose2d]):
                if f.startswith('model'):
                    # start_time_model = current_time_in_seconds()
                    model = torch.load(f_path, map_location=torch.device('cpu'))
                    model.to('cpu')
                    model.eval()
                    # elapsed_time_model = elapsed_time_in_seconds(start_time_model)
                    # print(f'load_model_files() Elapsed loading model: {elapsed_time_model} seconds')
                elif f.startswith('contour_model'):
                    # start_time_contour_model = current_time_in_seconds()
                    contour_model = torch.load(f_path, map_location=torch.device('cpu'))
                    contour_model.to('cpu')
                    contour_model.eval()
                    # elapsed_time_contour_model = elapsed_time_in_seconds(start_time_contour_model)
                    # print(f'load_model_files() Elapsed loading contour model: {elapsed_time_contour_model} seconds')
                elif f == 'params.json':
                    with open(f_path, 'r') as obj:
                        params = json.load(obj)
                else:
                    pass
        # elapsed_time_total = elapsed_time_in_seconds(start_time_total)
        # print(f'load_model_files() Elapsed total: {elapsed_time_total}')
        return model, contour_model, params

    def predict_contour(self, image, contour_model, params):
        # start_time_total = current_time_in_seconds()
        # start_time_normalization = current_time_in_seconds()
        ct = np.copy(image)
        ct = normalize_between(ct, params['min_bound_contour'], params['max_bound_contour'])
        # elapsed_time_normalization = elapsed_time_in_seconds(start_time_normalization)
        # print(f'predict_contour() Elapsed time normalization: {elapsed_time_normalization}')        
        # start_time_resize = current_time_in_seconds()
        target_shape = (512, 512)  
        ct_resized = cv2.resize(ct, target_shape, interpolation=cv2.INTER_LINEAR)
        # elapsed_time_resize = elapsed_time_in_seconds(start_time_resize)
        # print(f'predict_contour() Elapsed time resize: {elapsed_time_resize}')
        # start_time_upload_tensor = current_time_in_seconds()
        ct_resized_tensor = torch.tensor(ct_resized, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to('cpu')
        # elapsed_time_upload_tensor = elapsed_time_in_seconds(start_time_upload_tensor)
        # print(f'predict_contour() Elapsed time upload tensor: {elapsed_time_upload_tensor}')
        # start_time_predict = current_time_in_seconds()
        with torch.no_grad():
            pred = contour_model(ct_resized_tensor).cpu().numpy()
        pred_max = pred.argmax(axis=1)
        # elapsed_time_predict = elapsed_time_in_seconds(start_time_predict)
        mask = np.uint8(pred_max)
        # print(f'predict_contour() Elapsed time predict: {elapsed_time_predict}')
        # elapsed_time_total = elapsed_time_in_seconds(start_time_total)
        # print(f'predict_contour() Elapsed time total: {elapsed_time_total}')
        return mask

    def predict(self, model, image):
        # start_time_upload_tensor = current_time_in_seconds()
        img1_tensor = torch.tensor(image, dtype=torch.float32).unsqueeze(0).to('cpu')
        # elapsed_time_upload_tensor = elapsed_time_in_seconds(start_time_upload_tensor)
        # print(f'process_file() Elapsed time upload tensor: {elapsed_time_upload_tensor}')
        # start_time_predict = current_time_in_seconds()
        with torch.no_grad():
            pred = model(img1_tensor).cpu().numpy()
        pred_squeeze = np.squeeze(pred)
        pred_max = pred_squeeze.argmax(axis=0)
        return pred_max