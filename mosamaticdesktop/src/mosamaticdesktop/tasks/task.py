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

    """
    Initializes task instance.

    Parameters
    ----------
    input_dir : str
        Input directory from which to read files.
    output_dir_name : str 
        Name of output directory where output results will be
        written. Output directory will be created at same level as input directory.
        If output directory already exists, a sequence number will be appended.
    params : dict
        Task parameter dictionary.

    Returns
    -------
    None
    """
    def __init__(self, input_dir, output_dir_name=None, params=None):
        super(Task, self).__init__()
        self._input_dir = input_dir
        if output_dir_name is None:
            output_dir_name = self.__class__.__name__.lower()
        self._output_dir = os.path.join(str(Path(self._input_dir).parent), output_dir_name)
        self._params = params
        self._canceled = False
        output_dir = self._output_dir
        i = 1
        while os.path.exists(output_dir):
            output_dir = self._output_dir + f'_{i}'
            i += 1
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=False)

    """
    Returns task's input directory.

    Returns
    -------
    str
        Input directory.
    """
    def get_input_dir(self):
        return self._input_dir
    
    """
    Returns task's output directory.

    Returns
    -------
    str
        Output directory.
    """
    def get_output_dir(self):
        return self._output_dir
    
    """
    Checks if task has a given parameter.

    Parameters
    ----------
    name : str
        Name of parameter.

    Returns
    -------
    bool 
        True or false.
    """
    def has_param(self, name):
        if self._params is not None:
            return name in self._params.keys()
        return False
    
    """
    Returns task's parameters.

    Returns
    -------
    dict
        Parameter dictionary.
    """
    def get_params(self):
        return self._params
    
    """
    Returns specific task parameter value or a default.

    Parameters
    ----------
    name : str
        Name of parameter.
    default : Any
        Default value for parameter value if parameter does not exist.

    Returns
    -------
    Any
        Parameter value (can be default).
    """
    def get_param(self, name, default=None):
        if self.has_param(name):
            return self._params[name]
        return default
    
    """
    Checks if task has been canceled.

    Returns
    -------
    bool
        True or false.
    """
    def is_canceled(self):
        return self._canceled

    """
    Executes task instance.
    """
    def execute(self):
        for i in range(5):
            if self._canceled:
                self.set_status(TaskStatus.CANCELED)
                return 
            time.sleep(1)
            self.set_progress(i, 5)

    """
    Runs task instance. Can be called directly or through QThread's
    start() method.
    """
    def run(self):
        self.set_status(TaskStatus.RUNNING)
        try:
            print(f'Input directory: {self.get_input_dir()}')
            print(f'Output directory: {self.get_output_dir()}')
            print('Parameters:')
            print(json.dumps(self.get_params(), indent=2))
            self.execute()
            if not self.is_canceled():
                self.set_status(TaskStatus.COMPLETED)
        except Exception as e:
            print(f'ERROR: Task failed ({e})')
            self.set_status(TaskStatus.FAILED)

    """
    Cancels task instance. Sets self._canceled boolean to True so
    that the task picks it up on the next iteration and stops.
    """
    def cancel(self):
        self._canceled = True

    """
    Sets progress of the task depending on the number of steps needed
    and the current step.

    Parameters
    ----------
    step : int
        Index of the current iteration.
    nr_steps : int
        Total number of steps for this task.
    """
    def set_progress(self, step, nr_steps):
        progress = int(((step + 1) / (nr_steps)) * 100)
        print(f'Progress task {self.__class__.__name__}: {progress}')
        self.progress.emit(progress)

    """
    Sets task status. 

    Parameters
    ----------
    status : TaskStatus
        Current status of task instance to be broadcast to application.
    """
    def set_status(self, status):
        print(f'Status task {self.__class__.__name__}: {status.value}')
        self.status.emit(status.value)