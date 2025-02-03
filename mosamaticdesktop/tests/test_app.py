import os
import pathlib

from mosamaticdesktop.data.datamanager import DataManager


def test_datamanager():
    manager = DataManager()
    manager.create_file(
        os.path.join(pathlib.Path.home(), 'castorclientid.txt')
    )
