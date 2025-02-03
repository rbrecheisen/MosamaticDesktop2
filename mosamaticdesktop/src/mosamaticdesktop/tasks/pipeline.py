class Pipeline:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self):
        for i, task in enumerate(self.tasks):
            task.execute()
            if i < len(self.tasks):
                self.tasks[i+1].input_dir = task.output_dir