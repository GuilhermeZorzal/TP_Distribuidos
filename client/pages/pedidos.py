import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class Pedidos(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        text = QLabel("Pagina de Pedidos")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text)
        self.setLayout(layout)
