from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox


class TaskDialog(QDialog):
    def __init__(self, parent=None):
        super(TaskDialog, self).__init__(parent)
        self.setWindowTitle(self.__class__.__name__)
        self._params = {'clean_output': True}
        self._clean_output_checkbox = QCheckBox('Clean output', self)
        self._clean_output_checkbox.toggled.connect(self.handle_checkbox)
        self._clean_output_checkbox.setChecked(True)
        self._save_button = QPushButton('Save', self)
        self._save_button.clicked.connect(self.accept)
        self._cancel_button = QPushButton('Cancel', self)
        self._cancel_button.clicked.connect(self.reject)
        self._button_layout = QHBoxLayout()
        self._button_layout.addWidget(self._save_button)
        self._button_layout.addWidget(self._cancel_button)

    def init_ui(self):
        layout = QVBoxLayout()
        content_layout = self.get_content_layout()
        if content_layout:
            layout.addLayout(self.get_content_layout())
        layout.addWidget(self._clean_output_checkbox)
        layout.addLayout(self._button_layout)
        self.setLayout(layout)

    def get_content_layout(self):
        raise NotImplementedError('Implement in child dialog')
    
    def update_params(self):
        raise NotImplementedError('Implement in child dialog')
    
    def set_param(self, name, value):
        # if self._params is None:
        #     self._params = {}
        self._params[name] = value
    
    def accept(self):
        self.update_params()
        super(TaskDialog, self).accept()

    def reject(self):
        self._params = None
        super(TaskDialog, self).reject()

    def handle_checkbox(self, checked):
        self._params['clean_output'] = checked

    def get_params(self):
        return self._params