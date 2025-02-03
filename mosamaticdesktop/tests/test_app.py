import os

from mosamaticdesktop.data.datamanager import DataManager


def test_datamanager():
    manager = DataManager()
    f_path = os.path.join(os.environ['HOME'], 'castorclientid.txt')
    print(f_path)
    manager.create_file(f_path)
