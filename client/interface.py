import json
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from client import funcao_generica
from interface_socket.interface_socket import sendMessage


class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cliente PyQt")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("Digite seu nome:")
        self.layout.addWidget(self.label)

        self.input_nome = QLineEdit(self)
        self.layout.addWidget(self.input_nome)

        self.botao = QPushButton("Enviar")
        self.botao.clicked.connect(self.funcao_generica)
        self.layout.addWidget(self.botao)

        self.resposta_label = QLabel("")
        self.layout.addWidget(self.resposta_label)

        self.setLayout(self.layout)

    def funcao_generica(self):
        nome = self.input_nome.text()
        
        if nome:
            resposta = funcao_generica(nome)

            try:
                resposta_dict = json.loads(resposta)
            except Exception as e:
                self.resposta_label.setText(f"Erro ao converter resposta: {e}")
                return
            
            dados = ''
            for key, value in resposta_dict.items():
                dados += f"{key}: {value}\n"
                
            self.resposta_label.setText(dados)


app = QApplication(sys.argv)
janela = Interface()
janela.show()
sys.exit(app.exec())
