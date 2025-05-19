import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QListWidgetItem,
    QComboBox,
    QApplication,
    QLineEdit,
    QMessageBox,
    QScrollArea,
    QGridLayout,
    QMainWindow,
    QSpinBox,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QStackedWidget,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


from client.client import criar_pedido, get_catalogo, get_categoria, get_servico


class CardServico(QWidget):
    def __init__(self, service):
        super().__init__()

        # Widget interno com nome para o estilo
        container = QWidget()
        container.setObjectName("cardServico")

        layout = QVBoxLayout(container)

        self.title = QLabel(service["nome_servico"])
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
        """)

        self.desc = QLabel(service["descricao_servico"])
        self.categoria = QLabel(f"Categoria: {service['categoria']}")
        self.pagamento = QLabel(
            f"Pagamento: {service['quantidade']} {service['tipo_pagamento']}"
        )

        layout.addWidget(self.title)
        layout.addWidget(self.desc)
        layout.addWidget(self.categoria)
        layout.addWidget(self.pagamento)

        container.setLayout(layout)

        outer_layout = QHBoxLayout()
        outer_layout.addWidget(container)
        self.setLayout(outer_layout)

        # Aplica estilo usando o ID do container
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
            QCheckBox {
                font-size: 15px;
            }
            #cardServico {
                border: 1px solid #2c3e50;
                border-radius: 8px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)


class CatalogoLista(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.current_page = 0

        self.setStyleSheet("""
            QListWidgetItem:selected {
                background-color: #000066;
            }
            QComboBox {
                font-size: 20px;
            }
            QComboBox:selected {
                background-color: #2c3e50;
                font-size: 20px;
                color: white;
            }
            QLabel {
                font-size: 20px;
                color: #2c3e50;
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

        self.main_layout = QVBoxLayout()
        self.filtro_categoria = QComboBox()
        self.filtro_categoria.currentIndexChanged.connect(self.filtrando)

        self.lista = QListWidget()
        self.load_more_button = QPushButton("Carregar mais")
        self.load_more_button.clicked.connect(self.load_services)

        self.main_layout.addWidget(self.filtro_categoria)
        self.main_layout.addWidget(self.lista)
        self.main_layout.addWidget(self.load_more_button)
        self.setLayout(self.main_layout)

        self.lista.itemClicked.connect(self.goto_servico)

    def filtrando(self):
        self.current_page = 0
        self.lista.clear()
        self.load_services()

    def goto_servico(self, item):
        id = item.data(Qt.ItemDataRole.UserRole)
        self.parent.goto_servico(id)

    def load_services(self):
        try:
            categoria = self.filtro_categoria.currentText()
            resp = get_catalogo(categorias=[categoria], page=self.current_page)
            # resp = get_catalogo(page=self.current_page)
            print("Catalogo:", resp)
            if not resp[0]:
                QMessageBox.warning(self, "Erro", str(resp[1]))
                return

            services = resp[2]

            for service in services:
                item = QListWidgetItem()
                widget = CardServico(service)
                item.setSizeHint(widget.sizeHint())
                item.setData(Qt.ItemDataRole.UserRole, service["idServico"])
                self.lista.addItem(item)
                self.lista.setItemWidget(item, widget)

            if services:
                self.current_page += 1
            else:
                # Nada mais a carregar, desativa botão
                self.load_more_button.setEnabled(False)
                self.load_more_button.setText("Tudo carregado")

        except Exception as e:
            print(f"Erro ao carregar serviços: {e}")
        finally:
            self.is_loading = False

    def load(self):
        self.lista.clear()
        self.current_page = 0
        try:
            resp = get_categoria()
            if not resp[0]:
                QMessageBox.warning(self, "Erro", str(resp[1]))
                return
            categoria = resp[2]

            self.filtro_categoria.addItems(categoria)
            resp = get_catalogo(page=self.current_page)
            print("Catalogo:", resp)
            if not resp[0]:
                QMessageBox.warning(self, "Erro", str(resp[1]))
                return

            services = resp[2]

            for service in services:
                item = QListWidgetItem()
                widget = CardServico(service)
                item.setSizeHint(widget.sizeHint())
                item.setData(Qt.ItemDataRole.UserRole, service["idServico"])
                self.lista.addItem(item)
                self.lista.setItemWidget(item, widget)

            if services:
                self.current_page += 1
            else:
                # Nada mais a carregar, desativa botão
                self.load_more_button.setEnabled(False)
                self.load_more_button.setText("Tudo carregado")

        except Exception as e:
            print(f"Erro ao carregar serviços: {e}")


#
# class CatalogoLista(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.parent = parent
#
#         self.current_page = 0
#         self.page_size = 10
#         self.is_loading = False
#
#         self.setStyleSheet("""
#             QListWidgetItem:selected {
#                 background-color: #000066;
#             }
#             QComboBox {
#                 font-size: 20px;
#             }
#             QComboBox:selected {
#                 background-color: #2c3e50;
#                 font-size: 20px;
#                 color: white;
#             }
#             QLabel {
#                 font-size: 20px;
#                 color: #2c3e50;
#             }
#             QCheckBox {
#                 font-size: 15px;
#             }
#             QPushButton {
#                 color: white;
#                 font-size: 15px;
#                 background-color: #2c3e50;
#             }
#         """)
#         self.main_layout = QVBoxLayout()
#         self.lista = QListWidget()
#
#         self.filtro_categoria = QComboBox()
#         self.filtro_categoria.currentIndexChanged.connect(self.filter_services)
#
#         self.main_layout.addWidget(self.filtro_categoria)
#         self.main_layout.addWidget(self.lista)
#         self.setLayout(self.main_layout)
#
#         self.lista.itemClicked.connect(self.goto_servico)
#         # Connect scroll after user_list is created
#         self.lista.verticalScrollBar().valueChanged.connect(self.check_scroll_position)
#
#         # self.load_services()
#
#     def filter_services(self):
#         self.current_page = 0
#         self.load_services(
#             filter_text=self.filtro_categoria.currentText(), append=False
#         )
#
#     def goto_servico(self, item):
#         id = item.data(Qt.ItemDataRole.UserRole)
#         self.parent.goto_servico(id)
#
#     def load(self, filter_text="", append=False):
#         resp = get_categoria()
#         if not resp[0]:
#             raise Exception(resp[1])
#         categorias = resp[2]
#         if self.filtro_categoria.count() == 0:
#             self.filtro_categoria.addItems(sorted(categorias))
#         # self.filtro_categoria.addItems(categorias)
#         print("load_services")
#
#         if self.is_loading:
#             return
#
#         self.is_loading = True
#         try:
#             resp = get_catalogo()
#             print("Catalogo", resp)
#             if not resp[0]:
#                 QMessageBox.warning(self, "Erro", str(resp[1]))
#                 return
#             services = resp[2]
#
#             if not append:
#                 self.lista.clear()
#
#             for service in services:
#                 item = QListWidgetItem()
#                 widget = CardServico(service)
#                 item.setSizeHint(widget.sizeHint())
#                 item.setData(Qt.ItemDataRole.UserRole, service["idServico"])
#                 self.lista.addItem(item)
#                 self.lista.setItemWidget(item, widget)
#
#             if services:
#                 self.current_page += 1
#
#         except Exception as e:
#             print(f"Erro ao carregar serviços: {e}")
#         finally:
#             self.is_loading = False
#
#     def load_services(self, filter_text="", append=False):
#         resp = get_categoria()
#         if not resp[0]:
#             QMessageBox.warning(self, "erro carregando categorias", resp[1])
#             return
#
#         categorias = resp[2]
#
#         if self.filtro_categoria.count() == 0:
#             # self.filtro_categoria.addItems(list(categorias).sort())
#             self.filtro_categoria.addItems(sorted(categorias))
#         print("load_services")
#
#         if self.is_loading:
#             return
#
#         self.is_loading = True
#         try:
#             resp = get_catalogo(categorias=[filter_text])
#             print("Catalogo", resp)
#             if not resp[0]:
#                 QMessageBox.warning(self, "Erro", str(resp[1]))
#                 return
#             services = resp[2]
#
#             if not append:
#                 self.lista.clear()
#
#             for service in services:
#                 item = QListWidgetItem()
#                 widget = CardServico(service)
#                 item.setSizeHint(widget.sizeHint())
#                 item.setData(Qt.ItemDataRole.UserRole, service["idServico"])
#                 self.lista.addItem(item)
#                 self.lista.setItemWidget(item, widget)
#
#             if services:
#                 self.current_page += 1
#
#         except Exception as e:
#             print(f"Erro ao carregar serviços: {e}")
#         finally:
#             self.is_loading = False
#
#     def check_scroll_position(self):
#         scroll_bar = self.lista.verticalScrollBar()
#         if scroll_bar.value() >= scroll_bar.maximum() - 50:
#             self.load_services(
#                 filter_text=self.filtro_categoria.currentText(), append=True
#             )
#


class ServicoEspecifico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QVBoxLayout {
                font-size: 20px;
                margin: 12px;
            }
            QCheckBox {
                font-size: 15px;
            }
            QPushButton {
                color: white;
                font-size: 15px;
                background-color: #2c3e50;
            }
            QPushButton {
                color: white;
                font-size: 15px;
                background-color: #2c3e50;
            }
        """)
        self.id = ""
        self.title = QLabel()
        self.desc = QLabel()
        self.categoria = QLabel()
        self.pagamento = QLabel()

        self.quantidade = QSpinBox()
        self.quantidade.setMinimum(0)
        self.quantidade.setMaximum(1000)
        self.quantidade.setValue(1)

        self.button_comprar = QPushButton("Adicionar pedido")
        self.button_comprar.clicked.connect(self.criar_pedido)
        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)

        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.categoria.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pagamento.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.button_voltar)
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.desc)
        layout.addWidget(self.categoria)
        layout.addWidget(self.pagamento)
        layout.addWidget(self.quantidade)
        layout.addWidget(self.button_comprar)
        layout.addStretch()

        self.setLayout(layout)

    def load(self, id):
        resp = get_servico(id)
        if not resp[0]:
            QMessageBox.warning(self, "Erro na criação do pedido", str(resp[1]))
            return
        servico = resp[2]

        self.quantidade.setValue(1)
        self.id = servico["idServico"]
        self.title.setText(f"Nome do servico: {servico['nome_servico']}")
        self.desc.setText(f"Descrição: {servico['descricao_servico']}")
        self.categoria.setText(f"Categoria de servico: {servico['categoria']}")
        self.pagamento.setText(
            f"Pagamento: {servico['quantidade']} {servico['tipo_pagamento']}"
        )

    def criar_pedido(self):
        quantidade = self.quantidade.value()
        resp = criar_pedido(self.id, quantidade)
        if not resp[0]:
            QMessageBox.warning(self, "Erro na criação do pedido", str(resp[1]))
            return
        QMessageBox.information(self, "Parabens", "Seu pedido foi efetuado com sucesso")
        self.voltar()

    def voltar(self):
        self.parent.goto_catalogo()


class Catalogo(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
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

        self.servico = ServicoEspecifico(self)
        self.catalogo = CatalogoLista(self)
        self.addWidget(self.servico)
        self.addWidget(self.catalogo)

        self.setCurrentWidget(self.catalogo)

    def goto_catalogo(self):
        self.setCurrentWidget(self.catalogo)

    def goto_servico(self, id):
        self.servico.load(id)
        self.setCurrentWidget(self.servico)

    def load(self):
        print("Carregando catalogo")
        self.catalogo.load()
