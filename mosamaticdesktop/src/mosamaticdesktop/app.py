import toga

from toga.style import Pack

from mosamaticdesktop.tasks.copyfilestask import CopyFilesTask
from mosamaticdesktop.tasks.pipeline import Pipeline


class MosamaticDesktop(toga.App):
    def __init__(self):
        super(MosamaticDesktop, self).__init__()
        self.task = None
        self.pipeline = Pipeline([
            CopyFilesTask(
                'D:\\Mosamatic\\Mosamatic Desktop 2.0\\input', 
                'D:\\Mosamatic\\Mosamatic Desktop 2.0\\copyfilestask1',
                params={'delay': 1},
            ),
            CopyFilesTask(
                'D:\\Mosamatic\\Mosamatic Desktop 2.0\\copyfilestask1', 
                'D:\\Mosamatic\\Mosamatic Desktop 2.0\\copyfilestask2',
            ),
        ])

    def startup(self):
        button1 = toga.Button('Run task', on_press=self.run_task, style=Pack(padding=10))
        button2 = toga.Button('Run pipeline', on_press=self.run_pipeline, style=Pack(padding=10))
        button3 = toga.Button('Cancel task', on_press=self.cancel_task, style=Pack(padding=10))

        main_box = toga.Box()
        main_box.add(button1)
        main_box.add(button2)
        main_box.add(button3)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def run_task(self, widget):
        print('Running task...')
        self.task = CopyFilesTask(
            'D:\\Mosamatic\\Mosamatic Desktop 2.0\\input', 
            'D:\\Mosamatic\\Mosamatic Desktop 2.0\\copyfilestask1',
            params={'delay': 1},
        )
        self.task.start()
        print('Task completed')

    def cancel_task(self, widget):
        print('Canceling task...')
        if self.task and self.task.is_alive():
            self.task.terminate()
            self.task.join()
        print('Task canceled')

    def run_pipeline(self, widget):
        print('Running pipeline...')
        self.pipeline.run()
        print('Pipeline finished')



def main():
    return MosamaticDesktop()
