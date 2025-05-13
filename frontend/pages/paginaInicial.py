import sys
import os
from PyQt6.QtGui import QPixmap
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

FILE = "../assets/shrek.jpg"


class PaginaInicial(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-style: italic;
                background-color: #ecf0f1;
                padding: 10px;
            }
        """)

        # Titulo
        title = QLabel("O Oco do Ogro")
        title.setStyleSheet("""
            QLabel {
                font-size: 50px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slogan
        slogan = QLabel("Tão Tão Perto de Você")
        slogan.setStyleSheet("""
            QLabel {
                font-size: 35px;
            }
        """)
        slogan.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Descrição
        text = QLabel(
            "O oco do ogro é seu centro de aluguel de serviços preferido.\n"
            "Venha conosco encontrar os melhores serviços para você"
        )
        text.setStyleSheet("""
            QLabel {
                font-size: 20px;
            }
        """)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label = QLabel(self)

        # Por algum motivo esse troço carrega a imagem com path relativo ao arquivo interface, e não ao atual (apanhei pra descobrir viu)
        pixmap = QPixmap("./assets/images.jpg")
        image_label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(image_label)
        content_layout.addWidget(title)
        content_layout.addWidget(slogan)
        content_layout.addWidget(text)

        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(content_layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)
