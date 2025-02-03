import yaml
import argparse

from mosamaticdesktop.tasks.pipeline import Pipeline
from mosamaticdesktop.tasks import TASK_REGISTRY


def load_pipeline(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)
    tasks = []
    for step in config['steps']:
        task_name = step['task']
        task_class = TASK_REGISTRY.get(task_name)
        if not task_class:
            raise ValueError(f'Task {task_name} not found in TASK_REGISTRY')
        tasks.append(task_class(step['input_dir'], step['output_dir']))
    return Pipeline(tasks)


def main():
    parser = argparse.ArgumentParser(description='Run an image processing pipeline.')
    parser.add_argument('pipeline_config', help='YAML file defining the pipeline steps')
    parser.add_argument('input_dir', help='Input directory')
    args = parser.parse_args()
    pipeline = load_pipeline(args.pipeline_config)
    pipeline.run(args.input_dir)


if __name__ == '__main__':
    main()