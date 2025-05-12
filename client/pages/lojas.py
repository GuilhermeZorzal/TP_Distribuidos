from os import stat
import sys
from typing import Self
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QMainWindow,
    QDoubleSpinBox,
    QMessageBox,
    QScrollArea,
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

# FIXME: TODAS AS REQUISIÇÕES DO CLIENTE ESTÃO SUJEITAS A SEREM FEITAS COM THREADS
from pages.erroAutenticacao import Erro
from requestAPI.moc_gpt import (
    apagar_servico,
    esta_logado,
    criar_loja,
    criar_anuncio,
    get_catalogo,
    get_categoria,
    get_minha_loja,
    get_servico,
    ocultar_servico,
    desocultar_servico,
    editar_servico,
)


class Base(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title = QLabel("Area Loja")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_cria_loja = QPushButton("Criar Anuncio de Serviço")
        self.button_cria_loja.clicked.connect(self.cria_servico)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        layout.addStretch()
        outer_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(outer_layout)

    def cria_servico(self):
        pass


class Servico(QWidget):
    def __init__(
        self, parent, id, descricao, categoria, tipo, quantidade, esta_visivel
    ):
        super().__init__(parent)
        self.parent = parent
        self.id = id
        self.descricao = QLabel(f"Descricao: {descricao}")
        self.descricao.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.categoria = QLabel(f"categoria: {categoria}")
        self.categoria.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tipo = QLabel(f"tipo: {tipo}")
        self.tipo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.quant = QLabel(f"quantidade: {quantidade}")
        self.quant.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.visibilidade = QCheckBox("Esta visivel")
        self.visibilidade.setChecked(esta_visivel)
        self.visibilidade.clicked.connect(self.atualiza_visibilidade)

        self.button_deletar = QPushButton("Outras ações")
        self.button_deletar.clicked.connect(self.deletar)

        # self.button_atualiza = QPushButton("Atualizar visibilidade")
        # self.button_atualiza.clicked.connect(self.atualiza_visibilidade)

        # layout = QVBoxLayout()
        # layout.addStretch()
        # layout.addWidget(self.descricao)
        # layout.addWidget(self.categoria)
        # layout.addWidget(self.tipo)
        # layout.addWidget(self.quant)
        # layout.addWidget(self.visibilidade)
        # layout.addWidget(self.button_atualiza)
        # layout.addWidget(self.button_deletar)
        # layout.addStretch()
        container = QWidget()
        container.setObjectName("cardServico")  # Agora é esse que recebe a borda
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.descricao)
        layout.addWidget(self.categoria)
        layout.addWidget(self.tipo)
        layout.addWidget(self.quant)
        layout.addWidget(self.visibilidade)
        # layout.addWidget(self.button_atualiza)
        layout.addWidget(self.button_deletar)
        layout.addStretch()
        container.setLayout(layout)

        self.setObjectName("cardServico")  # Nome único pra usar no CSS

        # Agora o estilo afeta só esse widget externo
        # QWidget {
        #     border: 1px solid #444;
        #     border-radius: 8px;
        #     padding: 8px;
        #     background-color: #f9f9f9;
        # }
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
            #cardServico {
                border: 1px solid #2c3e50;
                border-radius: 8px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)

        outer_layout = QHBoxLayout()
        layout.addStretch()
        # outer_layout.addLayout(layout)
        outer_layout.addWidget(container)
        layout.addStretch()
        self.setLayout(outer_layout)

    def atualiza_visibilidade(self):
        print("foi")
        estado = self.visibilidade.isChecked()
        if estado:
            ocultar_servico(self.id)
        if estado:
            desocultar_servico(self.id)

    def deletar(self):
        apagar_servico(self.id)
        self.parent.goto_editar_servico(self.id)


class GerenciarServicos(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        id = self.parent.get_id_loja()
        resp = get_catalogo(id)
        if not resp[0]:
            raise Exception(resp[1])

        self.title = QLabel("Meus serviços")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
            }
        """)

        self.setStyleSheet("""
            QVBoxLayout {
                background-color: #2c3e50;
            }
        """)

        content_layout = QVBoxLayout()

        self.button_voltar = QPushButton("Voltar para area da loja")
        self.button_voltar.clicked.connect(self.voltar)
        content_layout.addWidget(self.title)
        dados = resp[2]
        for dado in dados:
            idServico = dado["idServico"]
            desc = dado["descricao_servico"]
            categoria = dado["categoria"]
            tipo = dado["tipo_pagamento"]
            quant = dado["quantidade_pagamento"]
            esta_visivel = dado["esta_visivel"]

            servico = Servico(
                self, idServico, desc, categoria, tipo, quant, esta_visivel
            )
            content_layout.addWidget(servico)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        # ScrollArea setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.button_voltar)
        main_layout.addWidget(self.title)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def goto_editar_servico(self, id):
        self.parent.goto_editar_servico(id)

    def voltar(self):
        self.parent.goto_area_loja()


class EditarServico(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.id = None
        self.title = QLabel("Editando Servico!!!")

        self.nome = QLabel("Insira o novo nome do servico")
        self.input_nome = QLineEdit()

        self.desc = QLabel("Insira a nova descrição do servico")
        self.input_desc = QLineEdit()

        # TODO: talvez as categorias irão mudar
        self.categoria = QLabel("Escolha a categoria em que o serviço se enquadra")
        self.input_categoria = QComboBox()
        status, message, categorias = get_categoria()
        self.input_categoria.addItems(categorias)

        self.label_tipo = QLabel(
            "Insira em que elemento você quer ser pago (moedas, escamas de dragão, etc)"
        )
        self.input_tipo_pagamento = QLineEdit()

        self.quantidade = QLabel("Insira o quantidade de elementos cobrados por hora")
        self.input_quantidade = QDoubleSpinBox()
        self.input_quantidade.setRange(0, 10000.0)  # min and max
        self.input_quantidade.setDecimals(2)  # number of decimal digits
        self.input_quantidade.setSingleStep(0.1)  # step when using arrows

        self.button_atualizar = QPushButton("Atualizar anuncio de Serviço")
        self.button_atualizar.clicked.connect(self.atualizar)

        self.button_delete = QPushButton("Deletar Servico")
        self.button_delete.clicked.connect(self.deletar)

        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.button_voltar)
        layout.addWidget(self.title)
        layout.addWidget(self.nome)
        layout.addWidget(self.input_nome)
        layout.addWidget(self.desc)
        layout.addWidget(self.input_desc)
        layout.addWidget(self.categoria)
        layout.addWidget(self.input_categoria)
        layout.addWidget(self.label_tipo)
        layout.addWidget(self.input_tipo_pagamento)
        layout.addWidget(self.quantidade)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(self.button_atualizar)
        layout.addWidget(self.button_delete)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        layout.addStretch()
        outer_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(outer_layout)

    def voltar(self):
        self.parent.goto_area_loja()

    def load(self, id):
        resp = get_servico(id)
        if not resp[0]:
            raise Exception(resp[1])

        servico = resp[2]

        self.id = servico["idServico"]
        self.input_nome.setText(servico["nome_servico"])
        self.input_desc.setText(servico["descricao_servico"])
        self.input_categoria.setCurrentText(servico["categoria"])
        self.input_tipo_pagamento.setText(servico["tipo_pagamento"])
        self.input_quantidade.setValue(servico["quantidade_pagamento"])

        self.setStyleSheet("""
            QLineEdit {
                color: #2c3e50;
                font-size: 20px;
            }
            QDoubleSpinBox {
                color: #2c3e50;
                font-size: 20px;
            }
            QComboBox {
                color: #2c3e50;
                font-size: 20px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 20px;
            }
            QPushButton {
                background-color: #2c3e50;
                font-size: 20px;
                color: white;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 40px;
            }
        """)

    def atualizar(self):
        if not esta_logado()[0]:
            # if False:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                "Voce não está autenticado",
            )
            return
        nome = self.input_nome.text()
        desc = self.input_desc.text()
        categoria = self.input_categoria.currentText()
        quantidade = self.input_quantidade.value()
        tipo = self.input_tipo_pagamento.text()
        idServico = self.id
        if not (nome and desc and categoria and quantidade and tipo):
            QMessageBox.warning(
                self,
                "Erro",
                "Por favor, preencha todos os campos",
            )
            return
        status, mensagem = editar_servico(
            idServico, nome, desc, categoria, tipo, quantidade
        )
        if not status:
            QMessageBox.warning(
                self,
                "Erro criando servico",
                mensagem,
            )
            return
        QMessageBox.warning(
            self,
            "Parabens",
            "Servico criado com sucesso",
        )
        self.parent.goto_area_loja()

    def deletar(self):
        if not esta_logado()[0]:
            # if False:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                "Voce não está autenticado",
            )
            return

        status, mensagem = apagar_servico(self.id)

        if not status:
            QMessageBox.warning(
                self,
                "Erro criando servico",
                mensagem,
            )
            return

        QMessageBox.warning(
            self,
            "Parabens",
            "Servico deletado com sucesso",
        )
        return
        self.parent.goto_area_loja()

    def cria_servico(self):
        if not esta_logado()[0]:
            # if False:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                "Voce não está autenticado",
            )
            return
        nome = self.input_nome.text()
        desc = self.input_desc.text()
        categoria = self.input_categoria.currentText()
        quantidade = self.input_quantidade.value()
        tipo = self.input_tipo_pagamento.text()
        if not (nome and desc and categoria and quantidade and tipo):
            QMessageBox.warning(
                self,
                "Erro",
                "Por favor, preencha todos os campos",
            )
            return
        status, mensagem = criar_anuncio(nome, desc, categoria, tipo, quantidade)
        if not status:
            QMessageBox.warning(
                self,
                "Erro criando servico",
                mensagem,
            )
            return
        QMessageBox.warning(
            self,
            "Parabens",
            "Servico criado com sucesso",
        )
        self.parent.goto_area_loja()


class CriarServico(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title = QLabel("Novo serviço!!!")
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
            }
            QComboBox {
                font-size: 20px;
            }
            QDoubleSpinBox {
                font-size: 20px;
            }
            QLineEdit {
                font-size: 20px;
            }
            QPushButton {
                background-color: #2c3e50;
                font-size: 20px;
                color: white;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 40px;
            }
        """)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Digite o nome do serviço")

        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Dê uma breve descrição do serviço")

        # TODO: talvez as categorias irão mudar
        self.categoria = QLabel("Escolha a categoria em que o serviço se enquadra")
        self.input_categoria = QComboBox()
        status, message, categorias = get_categoria()
        self.input_categoria.addItems(categorias)

        self.label_tipo = QLabel(
            "Insira em que elemento você quer ser pago (moedas, escamas de dragão, etc)"
        )
        self.input_tipo_pagamento = QLineEdit()

        self.quantidade = QLabel("Insira o quantidade de elementos cobrados por hora")
        self.input_quantidade = QDoubleSpinBox()
        self.input_quantidade.setRange(0, 10000.0)  # min and max
        self.input_quantidade.setDecimals(2)  # number of decimal digits
        self.input_quantidade.setSingleStep(0.1)  # step when using arrows

        self.button_cria_loja = QPushButton("Criar Anuncio de Serviço")
        self.button_cria_loja.clicked.connect(self.cria_servico)

        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.button_voltar)
        layout.addWidget(self.title)
        layout.addWidget(self.input_nome)
        layout.addWidget(self.input_desc)
        layout.addWidget(self.categoria)
        layout.addWidget(self.input_categoria)
        layout.addWidget(self.label_tipo)
        layout.addWidget(self.input_tipo_pagamento)
        layout.addWidget(self.quantidade)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(self.button_cria_loja)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        layout.addStretch()
        outer_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(outer_layout)

    def voltar(self):
        self.parent.goto_area_loja()

    def cria_servico(self):
        if not esta_logado()[0]:
            # if False:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                "Voce não está autenticado",
            )
            return
        nome = self.input_nome.text()
        desc = self.input_desc.text()
        categoria = self.input_categoria.currentText()
        quantidade = self.input_quantidade.value()
        tipo = self.input_tipo_pagamento.text()
        if not (nome and desc and categoria and quantidade and tipo):
            QMessageBox.warning(
                self,
                "Erro",
                "Por favor, preencha todos os campos",
            )
            return
        status, mensagem = criar_anuncio(nome, desc, categoria, tipo, quantidade)
        if not status:
            QMessageBox.warning(
                self,
                "Erro criando servico",
                mensagem,
            )
            return
        QMessageBox.warning(
            self,
            "Parabens",
            "Servico criado com sucesso",
        )
        self.parent.goto_area_loja()


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
        self.input_nome_loja.setPlaceholderText("Digite o nome da sua loja")

        self.input_contato = QLineEdit()
        self.input_contato.setPlaceholderText(
            "Digite as informações de contato da sua loja"
        )

        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Dê uma breve descrição de sua loja")

        self.button_cria_loja = QPushButton("Criar Loja")
        self.button_cria_loja.clicked.connect(self.cria_loja)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.descricao)
        layout.addWidget(self.input_nome_loja)
        layout.addWidget(self.input_contato)
        layout.addWidget(self.input_desc)
        layout.addWidget(self.button_cria_loja)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        layout.addStretch()
        outer_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(outer_layout)

    def cria_loja(self):
        if not esta_logado()[0]:
            # if False:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                "Voce não está autenticado",
            )
            return
        loja = self.input_nome_loja.text()
        desc = self.input_desc.text()
        contato = self.input_contato.text()
        if not (loja and desc and contato):
            QMessageBox.warning(
                self,
                "Erro",
                "Por favor, preencha todos os campos",
            )
            return
        sucesso, message = criar_loja(loja, contato, desc)
        if not sucesso:
            QMessageBox.warning(
                self,
                "Erro criando loja",
                message,
            )
            return
        QMessageBox.warning(
            self,
            "Parabens",
            "Loja criada com sucesso",
        )
        self.parent.goto_area_loja()


class AreaLoja(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        status, message, dados = get_minha_loja()

        # print(dados)
        if not status:
            raise Exception(message)

        self.parent = parent
        self.image_label = QLabel(self)
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
            }
            QPushButton {
                color: white;
                font-size: 20px;
                background-color: #2c3e50;
            }
        """)

        # Por algum motivo esse troço carrega a imagem com path relativo ao arquivo interface, e não ao atual (apanhei pra descobrir viu)
        pixmap = QPixmap("./assets/banho.jpg")
        self.image_label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("Area Loja")
        self.title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.nome = QLabel(f"Nome da loja: {dados['nome']}")
        self.nome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.contato = QLabel(f"Contato: {dados['contato']}")
        self.contato.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.descricao = QLabel(f"Descrição: {dados['descricao']}")
        self.descricao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent.set_id_loja(dados["idLoja"])

        self.button_cria_loja = QPushButton("Criar Anuncio de Serviço")
        self.button_cria_loja.clicked.connect(self.cria_servico)

        self.button_ver_servico = QPushButton("Visualizar servicos")
        self.button_ver_servico.clicked.connect(self.ver_servicos)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.image_label)
        layout.addWidget(self.title)
        layout.addWidget(self.nome)
        layout.addWidget(self.contato)
        layout.addWidget(self.descricao)
        layout.addWidget(self.button_cria_loja)
        layout.addWidget(self.button_ver_servico)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        layout.addStretch()
        outer_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(outer_layout)

    def cria_servico(self):
        self.parent.goto_area_servico()

    def ver_servicos(self):
        print(f"type(self.parent): {type(self.parent)}")
        self.parent.goto_area_gerencia()


class LojaStack(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        response = get_minha_loja()

        self.cria_loja = CrieLoja(self)
        self.area_loja = AreaLoja(self)
        self.novo_servico = CriarServico(self)
        self.meus_servicos = GerenciarServicos(self)
        self.editar_servico = EditarServico(self)
        self.id_loja = ""

        self.addWidget(self.cria_loja)
        self.addWidget(self.area_loja)
        self.addWidget(self.novo_servico)
        self.addWidget(self.meus_servicos)
        self.addWidget(self.editar_servico)

        if not response[0]:
            # Não há loja criada
            self.setCurrentWidget(self.cria_loja)

        self.setCurrentWidget(self.area_loja)

    def goto_area_loja(self):
        self.setCurrentWidget(self.area_loja)

    def goto_editar_servico(self, id):
        self.editar_servico.load(id)
        self.setCurrentWidget(self.editar_servico)

    def goto_area_servico(self):
        self.setCurrentWidget(self.novo_servico)

    def goto_area_gerencia(self):
        self.setCurrentWidget(self.meus_servicos)

    def set_id_loja(self, id):
        self.id_loja = id

    def get_id_loja(self):
        return self.id_loja


class Lojas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = QLabel("Pagina de lojas")
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 40px;
            }
        """)
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
