import sys
import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QMessageBox,
    QApplication,
    QMainWindow,
    QTextEdit,
    QCheckBox,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QStackedWidget,
    QFrame,
)
from PyQt6.QtCore import QSaveFile, Qt
from PyQt6.QtGui import QPalette, QColor

# from requestAPI.moc_gpt import cadastrar, autenticar, esta_logado, logout
from client.client import cadastrar, autenticar, esta_logado, logout

FILE = "../assets/shrek.jpg"


class Cadastro(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title = QLabel("Área de Cadastro")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #2c3e50;
            }
        """)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Digite seu nome")

        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #2c3e50;
            }
            QLineEdit {
                font-size: 20px;
            }
            QCheckBox {
                font-size: 15px;
            }
            QPushButton {
                color: white;
                font-size: 15px;
                background-color: #2c3e50;
            }
        """)

        self.input_apelido = QLineEdit()
        self.input_apelido.setPlaceholderText("Digite seu apelido")

        self.input_ccm = QLineEdit()
        self.input_ccm.setPlaceholderText(
            "Digite seu CCM (Cadastro de Criatura Mágica)"
        )

        # self.input_contato = QTextEdit()
        self.input_contato = QLineEdit()
        self.input_contato.setPlaceholderText("Digite suas informações de contato")

        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_senha.setPlaceholderText("Digite sua senha")

        self.termos = QCheckBox(
            "Eu aceito o uso das minhas informações mágicas para uso no site"
        )

        self.button_cadastrar = QPushButton("Cadastrar")
        self.button_cadastrar.clicked.connect(lambda _, n=parent: self.submit_form(n))

        self.redireciona = QLabel(
            "Caso já possua um cadastro, vá para a página de login:"
        )
        self.redireciona.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_redireciona = QPushButton("Login")
        self.button_redireciona.clicked.connect(lambda _, n=parent: self.go_login(n))

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.input_nome)
        layout.addWidget(self.input_apelido)
        layout.addWidget(self.input_contato)
        layout.addWidget(self.input_ccm)
        layout.addWidget(self.input_senha)
        layout.addWidget(self.termos)
        layout.addWidget(self.button_cadastrar)
        layout.addWidget(self.redireciona)
        layout.addWidget(self.button_redireciona)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def go_login(self, parent):
        parent.go_login()

    def submit_form(self, parent):
        nome = self.input_nome.text()
        apelido = self.input_apelido.text()
        # contato = self.input_contato.toPlainText()
        contato = self.input_contato.text()
        ccm = self.input_ccm.text()
        senha = self.input_senha.text()
        termos = self.termos.isChecked()

        if not (nome and apelido and contato and ccm and senha):
            QMessageBox.warning(
                self, "Cadastro incompleto", "Por favor, preencha todos os campos"
            )
            return

        if not termos:
            QMessageBox.warning(
                self,
                "Termos de Uso",
                "Atenção!! Voce deve aceitar nossos termos de uso",
            )
            return
        parent.cadastro(nome, apelido, contato, ccm, senha)


class Login(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title = QLabel("Área de Login")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #2c3e50;
            }
        """)
        self.input_ccm = QLineEdit()
        self.input_ccm.setPlaceholderText(
            "Digite seu CCM (Cadastro de Criatura Mágica)"
        )

        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #2c3e50;
            }
            QLineEdit {
                font-size: 20px;
            }
            QCheckBox {
                font-size: 15px;
            }
            QPushButton {
                color: white;
                font-size: 15px;
                background-color: #2c3e50;
            }
        """)

        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_senha.setPlaceholderText("Digite sua senha")

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(lambda _, n=parent: self.submit_form(n))

        self.redireciona = QLabel("Caso não possua um cadastro, crie aqui")
        self.redireciona.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_redireciona = QPushButton("Criar cadastro")
        self.button_redireciona.clicked.connect(lambda _, n=parent: self.go_cadastro(n))

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.input_ccm)
        layout.addWidget(self.input_senha)
        layout.addWidget(self.button_login)
        layout.addWidget(self.redireciona)
        layout.addWidget(self.button_redireciona)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def go_cadastro(self, parent):
        parent.go_cadastro()

    def submit_form(self, parent):
        ccm = self.input_ccm.text()
        senha = self.input_senha.text()

        if not (ccm and senha):
            QMessageBox.warning(
                self, "Cadastro incompleto", "Por favor, preencha todos os campos"
            )
            return

        parent.login(ccm, senha)


class Logout(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title = QLabel("Fazer Logout")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                color: #2c3e50;
            }
        """)
        self.desc = QLabel("Que pena que voce já vai")
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_login = QPushButton("Logout")
        self.button_login.clicked.connect(lambda _, n=parent: self.logout(n))

        image_label = QLabel(self)

        # Por algum motivo esse troço carrega a imagem com path relativo ao arquivo interface, e não ao atual (apanhei pra descobrir viu)
        pixmap = QPixmap("./assets/gato.jpg")
        image_label.setPixmap(pixmap)
        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #2c3e50;
            }
            QPushButton {
                color: white;
                font-size: 15px;
                background-color: #2c3e50;
            }
        """)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(image_label)
        layout.addWidget(self.title)
        layout.addWidget(self.desc)
        layout.addWidget(self.button_login)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def logout(self, parent):
        parent.call_logout()


class Auth(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.page_login = Login(self)
        self.page_cadastro = Cadastro(self)
        self.page_logout = Logout(self)

        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #2c3e50;
            }
        """)

        self.pages = {
            "cadastro": self.page_cadastro,
            "login": self.page_login,
            "logout": self.page_logout,
        }

        for page in self.pages.values():
            self.addWidget(page)

        log = esta_logado()[0]
        if not log:
            self.setCurrentWidget(self.page_login)
        else:
            self.setCurrentWidget(self.page_logout)

    def cadastro(self, nome, apelido, senha, ccm, contato):
        resp = cadastrar(nome, apelido, senha, ccm, contato)
        if not resp[0]:
            QMessageBox.warning(self, "Erro no cadastro", str(resp[1]))
        else:
            self.setCurrentWidget(self.page_login)

    def login(self, ccm, senha):
        resp = autenticar(ccm, senha)
        print("RESP", resp)
        self.setCurrentWidget(self.page_login)
        if not resp[0]:
            QMessageBox.warning(self, "Erro no login", str(resp[1]))
        else:
            self.setCurrentWidget(self.page_logout)
            self.parent.loadPages()
            # thread = threading.Thread(target=self.parent.loadPages)
            # print("Executando thread:")
            # thread.start()
            # thread.join()

    def call_logout(self):
        logout()
        self.setCurrentWidget(self.page_login)

    def go_login(self):
        self.setCurrentWidget(self.page_login)

    def go_cadastro(self):
        self.setCurrentWidget(self.page_cadastro)
