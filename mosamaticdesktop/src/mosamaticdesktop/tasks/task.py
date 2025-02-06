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

    def __init__(self, params=None, parent=None):
        super(Task, self).__init__(parent)
        self._params = params
        self._status = TaskStatus.IDLE
        self._running = True

    def execute(self, params):
        print(f'WARNING: execute() should be reimplemented in the child class. This is just a demo execution.')
        for i in range(5):
            if not self._running:
                self.set_status(TaskStatus.CANCELED)
                return 
            time.sleep(1)
            self.set_progress((i+1) * 20)

    def run(self):
        self.set_status(TaskStatus.RUNNING)
        try:
            self.execute(self._params)
            if self._running:
                self.set_status(TaskStatus.COMPLETED)
        except Exception as e:
            self.set_status(TaskStatus.FAILED)

    def cancel(self):
        self._running = False

    def set_progress(self, progress):
        self.progress.emit(progress)

    def set_status(self, status):
        self.status.emit(status.value)