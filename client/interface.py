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

from pages.auth import Auth
from pages.paginaInicial import PaginaInicial
from pages.catalogo import Catalogo
from pages.lojas import Lojas
from pages.pedidos import Pedidos
from pages.ajuda import Ajuda
from pages.settings import Settings
from pages.erroAutenticacao import Erro


paginas = [PaginaInicial, Auth, Catalogo, Lojas, Pedidos, Settings, Ajuda]


class BarraLateral(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setFixedWidth(200)
        self.main = parent
        self.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                margin: 0;
                padding: 5px;
                border: none;  /* Optional: removes default borders */
            }
            QPushButton {
                font-size: 25px;
                color: white;
                background-color: #2c3e50;
                margin: 10px;
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
        self.buttons = {
            "home": QPushButton("Home"),
            "auth": QPushButton("Auth"),
            "catalogo": QPushButton("Catalogo"),
            "lojas": QPushButton("Lojas"),
            "pedidos": QPushButton("Pedidos"),
            "settings": QPushButton("Settings"),
            "ajuda": QPushButton("Ajuda"),
        }

        for name, btn in self.buttons.items():
            btn.clicked.connect(lambda _, n=name: self.main.navigate_to(n))
            layout.addWidget(btn)

        # self.button_home = QPushButton("Home")
        # self.button_auth = QPushButton("Auth")
        # self.button_catalogo = QPushButton("Catalogo")
        # self.button_lojas = QPushButton("Lojas")
        # self.button_pedidos = QPushButton("Pedidos")
        # self.button_settings = QPushButton("Settings")
        # self.button_ajuda = QPushButton("Ajuda")
        #
        # layout.addWidget(self.button_home)
        # layout.addWidget(self.button_auth)
        # layout.addWidget(self.button_catalogo)
        # layout.addWidget(self.button_lojas)
        # layout.addWidget(self.button_pedidos)
        # layout.addWidget(self.button_settings)
        # layout.addWidget(self.button_ajuda)
        layout.addStretch()

        self.setLayout(layout)


class Paginas(QStackedWidget):
    # area que contem todos as paginas
    def __init__(self, parent=None):
        super().__init__(parent)

        self.paginaErro = Erro()

        self.addWidget(self.paginaErro)
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

        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        self.sidebar = BarraLateral(self)
        layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.page_home = PaginaInicial()
        self.page_auth = Auth()
        self.page_catalogo = Catalogo()
        self.page_lojas = Lojas()
        self.page_pedidos = Pedidos()
        self.page_settings = Settings()
        self.page_ajuda = Ajuda()
        self.page_erro = Erro()

        # Add pages to stack and track their names
        self.pages = {
            "home": self.page_home,
            "auth": self.page_auth,
            "catalogo": self.page_catalogo,
            "lojas": self.page_lojas,
            "pedidos": self.page_pedidos,
            "settings": self.page_settings,
            "ajuda": self.page_ajuda,
            "erro": self.page_erro,
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        self.stack.setCurrentWidget(self.page_home)

        # Set which pages require authentication
        self.protected_routes = {"catalogo", "lojas", "pedidos", "settings"}

    def navigate_to(self, page_name):
        token = self.page_auth.getToken()
        if page_name in self.protected_routes and not token:
            self.stack.setCurrentWidget(self.pages["erro"])
        else:
            self.stack.setCurrentWidget(self.pages[page_name])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: Set global palette or theme here if needed
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#ecf0f1"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
