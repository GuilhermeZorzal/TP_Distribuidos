import sys
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

# Paginas
# from pages.barraLateral import BarraLateral

# from pages.auth import Auth
from pages.paginaInicial import PaginaInicial
from pages.catalogo import Catalogo
from pages.lojas import Lojas
from pages.pedidos import Pedidos
from pages.ajuda import Ajuda


class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings"))
        self.setLayout(layout)


paginas = [PaginaInicial, Settings, Catalogo, Lojas, Pedidos, Ajuda]


class BarraLateral(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFixedWidth(200)
        self.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                margin: 0;
                padding: 5px;
                border: none;  /* Optional: removes default borders */
            }
            QPushButton {
                background-color: #34495e;
                color: white;
            }
            QPushButton:hover {
                background-color: #3d566e;
            }
        """)
        # border: none;
        # padding: 10px;
        # text-align: left;

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # Also remove space between widgets

        # TODO: se possivel modularizar, mas na pressa vou fazer o jeito paia
        # self.buttons = []
        # for i in range(len(paginas)):
        #     self.buttons.append(QPushButton("Nome provisorio"))
        #     layout.addWidget(self.buttons[i])

        self.button_home = QPushButton("Home")
        self.button_settings = QPushButton("Settings")
        self.button_catalogo = QPushButton("Catalogo")
        self.button_lojas = QPushButton("Lojas")
        self.button_pedidos = QPushButton("Pedidos")
        self.button_ajuda = QPushButton("Ajuda")

        layout.addWidget(self.button_home)
        layout.addWidget(self.button_settings)
        layout.addWidget(self.button_catalogo)
        layout.addWidget(self.button_lojas)
        layout.addWidget(self.button_pedidos)
        layout.addWidget(self.button_ajuda)
        layout.addStretch()

        self.setLayout(layout)


class Paginas(QStackedWidget):
    # area que contem todos as paginas
    def __init__(self, parent=None):
        super().__init__(parent)

        for page in paginas:
            self.addWidget(page())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Componente que segura todo o resto
        central_widget = QWidget()
        self.setWindowTitle("O Oco do Ogro")
        self.resize(800, 600)
        self.setCentralWidget(central_widget)

        # Layout é o baguio que segura tudo no lugar
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Side menu and content area
        self.barra_lateral = BarraLateral()
        self.content_area = Paginas()

        main_layout.addWidget(self.barra_lateral)
        main_layout.addWidget(self.content_area)

        # Connect buttons
        self.barra_lateral.button_home.clicked.connect(
            lambda: self.content_area.setCurrentIndex(0)
        )
        self.barra_lateral.button_settings.clicked.connect(
            lambda: self.content_area.setCurrentIndex(1)
        )
        self.barra_lateral.button_catalogo.clicked.connect(
            lambda: self.content_area.setCurrentIndex(2)
        )
        self.barra_lateral.button_lojas.clicked.connect(
            lambda: self.content_area.setCurrentIndex(3)
        )
        self.barra_lateral.button_pedidos.clicked.connect(
            lambda: self.content_area.setCurrentIndex(4)
        )
        self.barra_lateral.button_ajuda.clicked.connect(
            lambda: self.content_area.setCurrentIndex(5)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: Set global palette or theme here if needed
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#ecf0f1"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
