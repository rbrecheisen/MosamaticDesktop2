from PySide6.QtWidgets import QLabel, QSpinBox, QVBoxLayout

from mosamaticdesktop.tasks.taskdialog import TaskDialog


class CreatePngsFromSegmentationsTaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(CreatePngsFromSegmentationsTaskDialog, self).__init__(parent)
        self._fig_width_label = QLabel('Figure width', self)
        self._fig_height_label = QLabel('Figure height', self)
        self._fig_width_spinbox = QSpinBox(self, minimum=0, singleStep=1, value=10)
        self._fig_height_spinbox = QSpinBox(self, minimum=0, singleStep=1, value=10)
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._fig_width_label)
        self._layout.addWidget(self._fig_width_spinbox)
        self._layout.addWidget(self._fig_height_label)
        self._layout.addWidget(self._fig_height_spinbox)
        self.init_ui()

    def get_content_layout(self):
        return self._layout
    
    def update_params(self):
        self.set_param('fig_width', self._fig_width_spinbox.value())
        self.set_param('fig_height', self._fig_height_spinbox.value())