from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class Settings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings"))
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
