import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread, pyqtSignal
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
from pages.auth import Auth
from pages.paginaInicial import PaginaInicial
from pages.catalogo import Catalogo
from pages.lojas import Lojas
from pages.pedidos import Pedidos
from pages.ajuda import Ajuda
from pages.settings import Settings
from pages.erroAutenticacao import Erro

# from requestAPI.moc_gpt import esta_logado
from client.client import esta_logado

import threading

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
                font-size: 35px;
                color: white;
                background-color: #2c3e50;
                margin: 10px;
                padding: 10px;
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
            "loja": QPushButton("Loja"),
            "pedidos": QPushButton("Pedidos"),
            # "settings": QPushButton("Settings"),
            "ajuda": QPushButton("Ajuda"),
        }

        for name, btn in self.buttons.items():
            btn.clicked.connect(lambda _, n=name: self.main.navigate_to(n))
            layout.addWidget(btn)

        layout.addStretch()

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Componente que segura todo o resto
        central_widget = QWidget()
        self.setWindowTitle("O Oco do Ogro")
        self.resize(1000, 800)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # Also remove space between widgets
        central_widget.setLayout(layout)

        self.sidebar = BarraLateral(self)
        layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.page_home = PaginaInicial(self)
        self.page_auth = Auth(self)
        self.page_catalogo = Catalogo(self)
        self.page_lojas = Lojas(self)
        self.page_pedidos = Pedidos(self)
        # self.page_settings = Settings(self)
        self.page_ajuda = Ajuda(self)
        self.page_erro = Erro(self)

        # Add pages to stack and track their names
        self.pages = {
            "home": self.page_home,
            "auth": self.page_auth,
            "catalogo": self.page_catalogo,
            "loja": self.page_lojas,
            "pedidos": self.page_pedidos,
            # "settings": self.page_settings,
            "ajuda": self.page_ajuda,
            "erro": self.page_erro,
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        # inicia na Home
        self.stack.setCurrentWidget(self.page_home)

        # Listas de paginas que requerem autenticacao
        # self.protected_routes = {"catalogo", "loja", "pedidos", "settings"}
        self.protected_routes = {"catalogo", "loja", "pedidos"}

    def navigate_to(self, page_name):
        print("LOGADO", esta_logado()[0])
        if page_name in self.protected_routes and not esta_logado()[0]:
            self.stack.setCurrentWidget(self.pages["erro"])
        else:
            if page_name == "loja":
                self.page_lojas.load()
            if page_name == "catalogo":
                self.page_catalogo.load()
            # if page_name == "pedidos":
            #     self.page_pedidos.load()

            self.stack.setCurrentWidget(self.pages[page_name])
            # self.page_catalogo.load()
            # self.page_pedidos.load()

    def loadPages(self):
        pass
        # self.page_catalogo.load()
        # self.page_lojas.load()
        # self.page_pedidos.load()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Paleta de cores do aplicativo
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#ecf0f1"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
