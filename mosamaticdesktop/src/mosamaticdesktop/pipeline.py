class Pipeline:
    def __init__(self, tasks):
        self._tasks = tasks

    def run(self):
        for task in self._tasks:
            task.run()