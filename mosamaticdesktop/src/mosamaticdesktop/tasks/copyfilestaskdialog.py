from PySide6.QtWidgets import QSpinBox, QVBoxLayout

from mosamaticdesktop.tasks.taskdialog import TaskDialog


class CopyFilesTaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(CopyFilesTaskDialog, self).__init__(parent)
        self._delay_spinbox = QSpinBox(self, minimum=0, singleStep=1)

    def get_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self._delay_spinbox)
        return layout
    
    def update_params(self):
        self.set_param('delay', self._delay_spinbox.value())