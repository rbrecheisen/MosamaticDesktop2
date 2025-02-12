from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton


class TaskDialog(QDialog):
    def __init__(self, parent=None):
        super(TaskDialog, self).__init__(parent)
        self.setWindowTitle(self.__class__.__name__)
        self._params = None
        self._save_button = QPushButton('Save', self)
        self._save_button.clicked.connect(self.accept)
        self._cancel_button = QPushButton('Cancel', self)
        self._cancel_button.clicked.connect(self.reject)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self._save_button)
        button_layout.addWidget(self._cancel_button)
        layout = QVBoxLayout()
        child_layout = self.get_layout()
        if child_layout:
            layout.addLayout(self.get_layout())
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_layout(self):
        raise NotImplementedError('Implement in child dialog')
    
    def update_params(self):
        raise NotImplementedError('Implement in child dialog')
    
    def set_param(self, name, value):
        if self._params is None:
            self._params = {}
        self._params[name] = value
    
    def accept(self):
        self._params = self.update_params()
        super(CopyFilesTaskDialog, self).accept()

    def reject(self):
        self._params = None
        super(CopyFilesTaskDialog, self).reject()

    def get_params(self):
        return self._params