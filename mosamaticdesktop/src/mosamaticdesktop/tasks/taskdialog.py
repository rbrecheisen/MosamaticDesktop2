from PySide6.QtWidgets import QDialog


class TaskDialog(QDialog):
    def __init__(self, parent=None):
        super(TaskDialog, self).__init__(parent)