class Pipeline:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self, input_dir):
        for i, task in enumerate(self.tasks):
            if i == 0:
                task.input_dir = input_dir
            task.execute()
            if i < len(self.tasks):
                self.tasks[i+1].input_dir = task.output_dir