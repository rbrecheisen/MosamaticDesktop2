from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton


class LogDialog(QDialog):
    def __init__(self, parent=None):
        super(LogDialog, self).__init__(parent)
        self.setWindowTitle('Logging')
        self.setGeometry(100, 100, 600, 400)
        self._text_panel = QTextEdit(self)
        self._text_panel.setReadOnly(True)
        self._clear_button = QPushButton('Clear log', self)
        self._clear_button.clicked.connect(self.clear_log)
        self._close_button = QPushButton('Close', self)
        self._close_button.clicked.connect(self.close)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self._clear_button)
        button_layout.addWidget(self._close_button)
        layout = QVBoxLayout()
        layout.addWidget(self._text_panel)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def clear_log(self):
        self._text_panel.clear()

    def append_log(self, message):
        self._text_panel.append(message)
