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


class Ajuda(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        text = QLabel("Ajuda")
        text.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 35px;
            }
        """)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc = QLabel("""
        Esse aplicativo é o aplicativo resultante da implementação
        Do trabalho prático de Sistemas Distribuidos. 

        Em caso de dúvidas, contate os desenvolvedores:
        - Guilherme Broedel Zorzal
        - Maria Eduarda de Pinho Braga
        - Arthur Ataíde de Melo Saraiva
        """)
        desc.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
            }
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addWidget(text)
        layout.addWidget(desc)
        layout.addStretch()
        self.setLayout(layout)
