from mosamaticdesktop.data.datamanager import DataManager


def test_datamanager():
    manager = DataManager()
    manager.create_file('/Users/ralph/castorclientsecret.txt')
