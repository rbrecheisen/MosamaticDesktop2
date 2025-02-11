import yaml
import importlib


class Pipeline:

    """
    Initializes pipeline by loading given pipeline configuration YAML
    file and populating list of task instances.

    Parameters
    ----------
    config_file : str
        Path to pipeline configuration file.
    """
    def __init__(self, config_file):
        self._tasks = self.load_tasks_from_config(config_file)

    """
    Loads tasks from pipeline configuration YAML file.

    Parameters
    ----------
    config_file : str
        Path to pipeline configuration file.

    Returns
    -------
    list
        List of task instances.
    """
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
            output_dir_name = task_config['output_dir_name']
            params = task_config['params']
            module = importlib.import_module(module_name)
            task_class = getattr(module, class_name)
            task = task_class(input_dir, output_dir_name, params)
            tasks.append(task)
        return tasks

    """
    Runs pipeline by iterating over each task and running it.
    """
    def run(self):
        for i in range(len(self._tasks)):
            self._tasks[i].run()
            if i < len(self._tasks) - 1:
                self._tasks[i+1]._input_dir = self._tasks[i]._output_dir