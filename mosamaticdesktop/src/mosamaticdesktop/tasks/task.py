import os
import time
import json

from pathlib import Path
from enum import Enum
from PySide6.QtCore import QThread, Signal


class TaskStatus(Enum):
    IDLE = 'idle'
    RUNNING = 'running'
    CANCELED = 'canceled'
    FAILED = 'failed'
    COMPLETED = 'completed'


class Task(QThread):
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(Task, self).__init__()
        self._input_dir = input_dir
        if output_dir_name is None:
            output_dir_name = self.__class__.__name__.lower()
        self._output_dir = os.path.join(str(Path(self._input_dir).parent), output_dir_name)
        self._params = params
        self._canceled = False
        os.makedirs(self._output_dir, exist_ok=True)

    def get_input_dir(self):
        return self._input_dir
    
    def get_output_dir(self):
        return self._output_dir
    
    def has_param(self, name):
        if self._params is not None:
            return name in self._params.keys()
        return False
    
    def get_params(self):
        return self._params
    
    def get_param(self, name, default=None):
        if self.has_param(name):
            return self._params[name]
        return default
    
    def is_canceled(self):
        return self._canceled

    def execute(self):
        for i in range(5):
            if self._canceled:
                self.set_status(TaskStatus.CANCELED)
                return 
            time.sleep(1)
            self.set_progress(i, 5)

    def run(self):
        self.set_status(TaskStatus.RUNNING)
        try:
            print('Parameters:')
            print(json.dumps(self.get_params(), indent=2))
            self.execute()
            if not self.is_canceled():
                self.set_status(TaskStatus.COMPLETED)
        except Exception as e:
            print(f'ERROR: Task failed ({e})')
            self.set_status(TaskStatus.FAILED)

    def cancel(self):
        self._canceled = True

    def set_progress(self, step, nr_steps):
        progress = int(((step + 1) / (nr_steps)) * 100)
        print(f'Progress task {self.__class__.__name__}: {progress}')
        self.progress.emit(progress)

    def set_status(self, status):
        print(f'Status task {self.__class__.__name__}: {status.value}')
        self.status.emit(status.value)