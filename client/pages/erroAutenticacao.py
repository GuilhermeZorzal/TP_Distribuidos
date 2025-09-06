from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class Erro(QWidget):
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
        title = QLabel("Você não está autenticado!!!")
        title.setStyleSheet("""
            QLabel {
                font-size: 25px;
                color: red;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slogan
        text = QLabel(
            'Por favor, dirija-se a aba "Auth" para realizar sua autenticação'
        )
        text.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
        """)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label = QLabel(self)
        # Por algum motivo esse troço carrega a imagem com path relativo ao arquivo interface, e não ao atual (apanhei pra descobrir viu)
        pixmap = QPixmap("./assets/assustado.jpg")
        image_label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(image_label)
        content_layout.addWidget(title)
        content_layout.addWidget(text)

        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(content_layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)
