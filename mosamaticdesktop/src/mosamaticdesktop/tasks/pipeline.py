import yaml
import importlib


class Pipeline:
    def __init__(self, config_file):
        self._input_dir, self._tasks = None, []
        self.load_config(config_file)

    def load_config(self, config_file):
        
        # Load YAML file
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

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