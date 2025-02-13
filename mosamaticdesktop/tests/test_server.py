import sys
import requests


def test_server():
    response = requests.post('http://127.0.0.1:5000/pipeline', json={
        'input_dir': 'D:\\Mosamatic\\Mosamatic Desktop 2.0\\input' \
            if sys.platform.startswith('win') \
            else '/Users/ralph/Desktop/downloads/mosamaticdesktop/input',
        'config_file_path': 'D:\\SoftwareDevelopment\\GitHub\\MosamaticDesktop2\\pipeline_windows.yaml' \
            if sys.platform.startswith('win') \
            else '/Users/ralph/dev/tools/MosamaticDesktop2/pipeline_unix.yaml',
    })
    assert response.status_code == 200, response.status_code