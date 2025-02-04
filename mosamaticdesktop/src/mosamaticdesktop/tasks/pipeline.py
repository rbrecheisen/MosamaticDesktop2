class Pipeline:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self):
        for task in self.tasks:
            task.start()
            task.join()