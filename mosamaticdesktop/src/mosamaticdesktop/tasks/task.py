import os
import time

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

    def __init__(self, input_dir, output_dir, params=None):
        super(Task, self).__init__()
        self._input_dir = input_dir
        self._output_dir = output_dir
        self._params = params
        self._canceled = False
        os.makedirs(output_dir, exist_ok=True)

    def execute(self):
        for i in range(5):
            if self._canceled:
                self.set_status(TaskStatus.CANCELED)
                return 
            time.sleep(1)
            self.set_progress((i+1) * 20)

    def run(self):
        self.set_status(TaskStatus.RUNNING)
        try:
            self.execute()
            if not self._canceled:
                self.set_status(TaskStatus.COMPLETED)
        except Exception as e:
            print(f'ERROR: Task failed ({e})')
            self.set_status(TaskStatus.FAILED)

    def cancel(self):
        self._canceled = True

    def set_progress(self, progress):
        print(f'Progress task {self.__class__.__name__}: {progress}')
        self.progress.emit(progress)

    def set_status(self, status):
        print(f'Status task {self.__class__.__name__}: {status.value}')
        self.status.emit(status.value)