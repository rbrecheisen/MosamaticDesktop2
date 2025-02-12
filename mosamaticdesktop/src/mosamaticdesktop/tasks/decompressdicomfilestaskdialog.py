from mosamaticdesktop.tasks.taskdialog import TaskDialog


class DecompressDicomFilesTaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(DecompressDicomFilesTaskDialog, self).__init__(parent)

    def get_layout(self):
        return None
    
    def update_params(self):
        pass