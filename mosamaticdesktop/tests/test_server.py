import requests


def test_server():
    response = requests.post('http://localhost:5000/pipeline', json={
        'input_dir': 'D:\\Mosamatic\\Mosamatic Desktop 2.0\\input',
        'config_file_path': 'D:\\SoftwareDevelopment\\GitHub\\MosamaticDesktop2\\pipeline_windows.yaml',
    })
    assert response.status_code == 200, response.status_code