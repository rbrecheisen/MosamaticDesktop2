import os
import yaml
import importlib

from mosamaticdesktop.tasks.taskregistry import TASK_REGISTRY


class Pipeline:
    def __init__(self, config_file):
        self._input_dir, self._tasks = None, []
        self.load_config(config_file)

    def check_config(self, config):
        errors = []
        if 'input_dir' not in config.keys():
            errors.append('Entry "input_dir" missing')
            return errors
        input_dir = config['input_dir']
        if not os.path.exists(input_dir):
            errors.append(f'Input directory {input_dir} does not exist')
            return errors
        # Check there are tasks defined in the pipeline                
        if 'tasks' not in config.keys():
            errors.append('Entry "tasks" missing')
            return errors
        # Check each task's configuration
        for task_config in config['tasks']:            
            if 'class' not in task_config.keys():
                errors.append(f'Task "class" entry missing ({task_config})')
                continue
            class_name = task_config['class']
            if class_name not in TASK_REGISTRY.keys():
                errors.append(f'Task {class_name} not in TASK_REGISTRY')
                continue
            if 'input_dir' not in task_config.keys():
                errors.append(f'Task {class_name} "input_dir" entry missing (can be empty so it is set to the pipeline input directory)')
                continue
            if 'output_dir_name' not in task_config.keys():
                errors.append(f'Task {class_name} "output_dir_name" entry missing')
                continue
            if 'params' not in task_config.keys():
                errors.append(f'Task {class_name} "params" entry missing (can be empty)')
                continue
        return errors

    def load_config(self, config_file):
        # Load YAML file
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        # Check contents (especially existence of directories)
        errors = self.check_config(config)
        if len(errors) > 0:
            print(f'ERROR: configuration file has errors:')
            for error in errors:
                print(f' - {error}')
            return
        # Get input directory for pipeline
        self._input_dir = config['input_dir']
        if not self._input_dir:
            raise RuntimeError(f'Pipeline has no input directory!')
        # Load task instances. When we run tasks through the pipeline the 
        # output directory names will be prepended with an index
        self._tasks = []
        i = 1
        for task_config in config['tasks']:
            class_name = task_config['class']
            module_name = f'mosamaticdesktop.tasks.{class_name.lower()}'
            input_dir = task_config['input_dir']
            # The first task may not have an input directory. In that case, take the main
            # pipeline input directory
            if not input_dir:
                print(f'Pipeline.load_config() task {class_name} has no input directory. Using pipeline input directory...')
                input_dir = self._input_dir
            output_dir_name = task_config['output_dir_name']
            params = task_config['params']
            module = importlib.import_module(module_name)
            task_class = getattr(module, class_name)
            task = task_class(input_dir, output_dir_name, params)
            self._tasks.append(task)
            i += 1

    def run(self):
        for i in range(len(self._tasks)):
            self._tasks[i].run()

    def update_input_dir(self, input_dir):
        self._input_dir = input_dir
        self._tasks[0]._input_dir = self._input_dir