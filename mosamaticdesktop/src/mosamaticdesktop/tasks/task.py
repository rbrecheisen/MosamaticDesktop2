import os
import uuid


class Task:
    def __init__(self, input_dir, output_dir, params=None):
        self.task_id = str(uuid.uuid4())
        self.params = params
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def execute(self):
        raise NotImplementedError('Subclasses must implement "run()"')

    def run(self):
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f'Input directory {self.input_dir} not found')        
        self.execute()
        print(f'Task {self.__class__.__name__} completed. Output at {self.output_dir}')