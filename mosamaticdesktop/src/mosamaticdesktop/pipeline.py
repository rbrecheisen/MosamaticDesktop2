import yaml
import importlib


class Pipeline:
    def __init__(self, config_file):
        self._tasks = self.load_tasks_from_config(config_file)

    def load_tasks_from_config(self, config_file):

        # Load YAML file
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # Load task instances 
        tasks = []
        for task_config in config['tasks']:
            class_name = task_config['class']
            module_name = f'mosamaticdesktop.tasks.{class_name.lower()}'
            input_dir = task_config['input_dir']
            output_dir = task_config['output_dir']
            params = task_config['params']
            module = importlib.import_module(module_name)
            task_class = getattr(module, class_name)
            task = task_class(input_dir, output_dir, params)
            tasks.append(task)
        return tasks

    def run(self):
        for task in self._tasks:
            task.run()