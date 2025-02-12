from mosamaticdesktop.tasks.taskdialog import TaskDialog


class RescaleDicomFilesTaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(RescaleDicomFilesTaskDialog, self).__init__(parent)

    def get_layout(self):
        return None
    
    def update_params(self):
        pass