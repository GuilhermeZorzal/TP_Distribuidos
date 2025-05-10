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


class BarraLateral(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFixedWidth(200)
        self.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                font-size: 25px;
            }
            QPushButton {
                font-size: 25px;
                color: red;
                margin: 19px;
            }
            QPushButton:hover {
                background-color: #3d566e;
            }
        """)

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = []
        self.button_home = QPushButton("Home")
        self.button_settings = QPushButton("Settings")
        self.button_ajuda = QPushButton("Ajuda")

        layout.addWidget(self.button_home)
        layout.addWidget(self.button_settings)
        layout.addWidget(self.button_ajuda)
        layout.addStretch()

        self.setLayout(layout)
