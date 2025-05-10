import sys
from typing import Self
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QStackedLayout,
    QLineEdit,
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

from requestAPI.req_loja import criaLoja as req_criaLoja


class CrieLoja(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title = QLabel("Criar Loja")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.descricao = QLabel(
            "Parece que voce não ainda não tem nenhuma loja.\nPreencha os dados abaixo para criar"
        )
        self.descricao.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_nome_loja = QLineEdit()
        self.input_nome_loja.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_nome_loja.setPlaceholderText("Digite o nome da sua loja")

        self.input_info = QLineEdit()
        self.input_info.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_info.setPlaceholderText(
            "Digite algumas informações importantes sobre sua loja"
        )

        self.input_desc = QLineEdit()
        self.input_desc.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_desc.setPlaceholderText("Dê uma breve descrição de sua loja")

        self.button_cria_loja = QPushButton("Criar Loja")
        self.button_cria_loja.clicked.connect(self.cria_loja)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.descricao)
        layout.addWidget(self.input_nome_loja)
        layout.addWidget(self.input_info)
        layout.addWidget(self.input_desc)
        layout.addWidget(self.button_cria_loja)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        layout.addStretch()
        outer_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(outer_layout)

    def cria_loja(self):
        token = self.parent.get_token()
        print(token)
        # TODO: trocar
        # if not token:
        if False:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                "Voce não está autenticado",
            )
            return
        loja = self.input_nome_loja.text()
        desc = self.input_desc.text()
        info = self.input_info.text()
        if not (loja and desc and info):
            QMessageBox.warning(
                self,
                "Erro",
                "Por favor, preencha todos os campos",
            )
            return
        sucesso, message = req_criaLoja(token, loja, desc, info)
        if not sucesso:
            QMessageBox.warning(
                self,
                "Erro criando loja",
                message,
            )
            return
        self.parent.goto_area_loja()


class AreaLoja(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title = QLabel("Area Loja")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.descricao = QLabel(
            "Parece que voce não ainda não tem nenhuma loja.\nPreencha os dados abaixo para criar"
        )
        self.descricao.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_nome_loja = QLineEdit()
        self.input_nome_loja.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_nome_loja.setPlaceholderText("nada")

        self.input_info = QLineEdit()
        self.input_info.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_info.setPlaceholderText("nada")

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.descricao)
        layout.addWidget(self.input_nome_loja)
        layout.addWidget(self.input_info)
        layout.addWidget(self.input_desc)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        layout.addStretch()
        outer_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(outer_layout)


class LojaStack(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.criaLoja = CrieLoja(self)
        self.areaLoja = AreaLoja(self)

        self.addWidget(self.criaLoja)
        self.addWidget(self.areaLoja)

        self.setCurrentWidget(self.criaLoja)

    def get_token(self):
        return self.parent.get_token()

    def goto_area_loja(self):
        self.setCurrentWidget(self.areaLoja)


class Lojas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.text = QLabel("Pagina de lojas")
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paginas = LojaStack(parent)

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.paginas)

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)
