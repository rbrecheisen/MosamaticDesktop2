import os


class Task:
    def __init__(self, input_dir: str, output_dir: str) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self):
        raise NotImplementedError('Subclasses must implement "run()"')

    def execute(self):
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f'Input directory {self.input_dir} not found')
        self.run()
        print(f'Task {self.__class__.__name__} completed. Output at {self.output_dir}')