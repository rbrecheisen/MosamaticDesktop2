class Pipeline:
    def __init__(self, tasks):
        self.tasks = tasks
        self.current_task = None

    def run(self):
        for i, task in enumerate(self.tasks):
            self.current_task = task
            self.current_task.start()
            self.current_task.join()

    def cancel_current_task(self):
        if self.current_task and self.current_task.is_alive():
            self.current_task.terminate()
            self.current_task.join()