import os
import uuid
import shutil
import multiprocessing

from flask import Flask, request, jsonify


app = Flask()


class TaskRegistry:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.task_id] = task

    def remove_task(self, task_id):
        del self.tasks[task_id]
    
    def get_task(self, task_id):
        return self.tasks[task_id]
    
    def run_task(self, task_id, params):
        self.tasks[task_id].execute(params)


class Task(multiprocessing.Process):
    def __init__(self, task_id, input_dir, output_dir):
        super(Task, self).__init__()
        self.task_id = str(uuid.uuid4())
        self.status = 'init'
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, params=None):
        raise NotImplementedError('Method run() has to be implemented in child class')
    
    def execute(self, params=None):
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f'Input directory {self.input_dir} not found')
        self.run()
        print(f'Task {self.__class__.__name__} completed. Output at {self.output_dir}')


class CopyFilesTask(Task):
    def run(self, params=None):
        for f in os.listdir(self.input_dir):
            source = os.path.join(self.input_dir, f)
            target = os.path.join(self.output_dir, f)
            shutil.copy(source, target)


registry = TaskRegistry()


@app.route('/start_task', methods=['POST'])
def start_task():
    data = request.json
    task_id = registry.add_task(CopyFilesTask())