import os
import pandas as pd


def load_bc_metrics(f_path):
    metrics = pd.read_csv(f_path, sep=';')
    return metrics


def main():
    metrics_torch = load_bc_metrics('D:\\Mosamatic\\Mosamatic Desktop 2.0\\bc_metrics_torch.csv')
    # print(metrics_torch)
    metrics_tensorflow = load_bc_metrics('D:\\Mosamatic\\Mosamatic Desktop 2.0\\bc_metrics_tensorflow.csv')
    # print(metrics_tensorflow)

    for idx, row in metrics_torch.iterrows():
        
        muscle_area_torch = float(row['muscle_area'])
        muscle_area_tensorflow = float(metrics_tensorflow.loc[idx, 'muscle_area'])
        muscle_area_diff = muscle_area_tensorflow - muscle_area_torch

        sat_area_torch = float(row['vat_area'])
        sat_area_tensorflow = float(metrics_tensorflow.loc[idx, 'vat_area'])
        vat_area_diff = sat_area_tensorflow - sat_area_torch

        sat_area_torch = float(row['sat_area'])
        sat_area_tensorflow = float(metrics_tensorflow.loc[idx, 'sat_area'])
        sat_area_diff = sat_area_tensorflow - sat_area_torch

        muscle_ra_torch = float(row['muscle_ra'])
        muscle_ra_tensorflow = float(metrics_tensorflow.loc[idx, 'muscle_ra'])
        muscle_ra_diff = muscle_ra_tensorflow - muscle_ra_torch

        vat_ra_torch = float(row['vat_ra'])
        vat_ra_tensorflow = float(metrics_tensorflow.loc[idx, 'vat_ra'])
        vat_ra_diff = vat_ra_tensorflow - vat_ra_torch

        sat_ra_torch = float(row['sat_ra'])
        sat_ra_tensorflow = float(metrics_tensorflow.loc[idx, 'sat_ra'])
        sat_ra_diff = sat_ra_tensorflow - sat_ra_torch

        print(f'{idx}: muscle_area: {muscle_area_diff}, vat_area: {vat_area_diff}, sat_area: {sat_area_diff}, muscle_ra: {muscle_ra_diff}, vat_ra: {vat_ra_diff}. sat_ra: {sat_ra_diff}')


if __name__ == '__main__':
    main()