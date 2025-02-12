import yaml
import importlib


class Pipeline:
    def __init__(self, config_file):
        self._tasks = self.load_tasks_from_config(config_file)

    def load_tasks_from_config(self, config_file):
        
        # Load YAML file
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # Load task instances. When we run tasks through the pipeline the 
        # output directory names will be prepended with an index
        tasks = []
        i = 1
        for task_config in config['tasks']:
            class_name = task_config['class']
            module_name = f'mosamaticdesktop.tasks.{class_name.lower()}'
            input_dir = task_config['input_dir']
            output_dir_name = f'{i:02d}_' + task_config['output_dir_name'] # Prepend index
            params = task_config['params']
            module = importlib.import_module(module_name)
            task_class = getattr(module, class_name)
            task = task_class(input_dir, output_dir_name, params)
            tasks.append(task)
            i += 1
        return tasks

    def run(self):
        for i in range(len(self._tasks)):
            self._tasks[i].run()
            if i < len(self._tasks) - 1:
                self._tasks[i+1]._input_dir = self._tasks[i]._output_dir