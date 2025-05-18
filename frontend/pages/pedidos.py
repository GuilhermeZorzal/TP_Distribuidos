import sys
from PyQt6.QtWidgets import (
    QListWidget,
    QDialog,
    QListWidgetItem,
    QMessageBox,
    QScrollArea,
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
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

import qrcode
from io import BytesIO

# from requestAPI.moc_gpt import (
from client.client import (
    cancelar_pedido,
    get_pedido,
    get_pedidos,
    get_pedidos_minha_loja,
    pagar_pedido,
)


class QRCodePopup(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QR Code")
        self.setMinimumSize(300, 300)

        layout = QVBoxLayout()

        # Generate QR code as image
        qr = qrcode.make(data)
        buf = BytesIO()
        qr.save(buf, format="png")
        qimage = QImage.fromData(buf.getvalue())
        pixmap = QPixmap.fromImage(qimage)

        self.label = QLabel()
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.close_button = QPushButton("Fechar")
        self.close_button.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.close_button)

        self.setLayout(layout)


# TODO:
# - Adicionar a opção de confirmar o pedido
# - Trocar a implementação da lista pra usar QList


def remove_layout(widget: QWidget):
    old_layout = widget.layout()
    if old_layout is not None:
        # Remove all widgets from the layout
        while old_layout.count():
            item = old_layout.takeAt(0)
            child_widget = item.widget()
            if child_widget:
                child_widget.setParent(None)
        # Delete the layout from the widget
    QWidget().setLayout(old_layout)  # Trick to delete it


class PedidoUnicoUsuario(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title = QLabel("Pedido")
        self.title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 25px;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id = QLabel("id")
        self.data = QLabel("data:")
        self.servico = QLabel("servico:")
        self.estado = QLabel("estado:")
        self.total = QLabel("total:")
        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)
        layout = QVBoxLayout()
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 25px;
            }
            QPushButton {
                color: white;
                font-size: 20px;
                background-color: #2c3e50;
            }
        """)

        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.id)
        layout.addWidget(self.data)
        layout.addWidget(self.servico)
        layout.addWidget(self.estado)
        layout.addWidget(self.total)
        layout.addWidget(self.button_voltar)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def load(self, id):
        resp = get_pedido(id)
        print("*********************\nPEDIDO UNICO USUARIO", resp)
        if not resp[0]:
            QMessageBox.warning(self, "Erro", str(resp[1]))
            return

        dados = resp[2]
        print(dados)
        # self.title.setText("Pedido")
        # self.title.setStyleSheet("""
        #     QLabel {
        #         color: #2c3e50;
        #         font-weight: bold;
        #         font-size: 20px;
        #     }
        # """)
        self.id.setText(f"ID: {id}")
        self.id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.data.setText(f"Data: {dados['data_pedido']}")
        self.data.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.servico.setText(f"Servico: {dados['nome_servico']}")
        self.servico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estado.setText(f"Estado: {dados['estado_pedido']}")
        self.estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total.setText(f"Total: {dados['total']}")
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete = QPushButton("Cancelar pedido")

    def voltar(self):
        self.parent.goto_pedidos_loja()


class PedidoUnico(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.id = ""
        self.title = QLabel("Pedido")
        self.title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 25px;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)

        self.data = QLabel("data:")
        self.cliente = QLabel("servico:")
        self.servico = QLabel("servico:")
        self.estado = QLabel("estado:")
        self.data_entrega = QLabel("data entrega:")
        self.total = QLabel("total:")
        self.nome_loja = QLabel("loja:")
        self.delete = QPushButton("Cancelar pedido")
        self.button_pagar = QPushButton("Realizar Pagamento ")

        self.delete.clicked.connect(self.deletar)
        self.button_pagar.clicked.connect(self.pagar)
        self.button_pagar.setEnabled(False)  # Make it unclickable

        layout = QVBoxLayout()
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 25px;
            }
            QPushButton {
                color: white;
                font-size: 20px;
                background-color: #2c3e50;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
                color: #ecf0f1;
            }
        """)

        layout.addStretch()
        layout.addWidget(self.button_voltar)
        layout.addWidget(self.title)
        # layout.addWidget(self.id)
        layout.addWidget(self.data)
        # layout.addWidget(self.cliente)
        layout.addWidget(self.servico)
        layout.addWidget(self.nome_loja)
        layout.addWidget(self.estado)
        layout.addWidget(self.data_entrega)
        layout.addWidget(self.total)
        layout.addWidget(self.delete)
        layout.addWidget(self.button_pagar)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def voltar(self):
        self.parent.goto_meus_pedidos()

    def load(self, id):
        resp = get_pedido(id)
        if not resp[0]:
            QMessageBox.warning(self, "Erro", str(resp[1]))

        dados = resp[2]
        print("PEDIDOS DADOS:", dados)

        self.id = id
        # self.id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.data.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.data.setText(f"Data: {dados['data_pedido']}")

        self.servico.setText(f"Nome do Servico: {dados['nome_servico']}")
        self.servico.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.cliente.setText(f"Servico: {dados['nome_cliente']}")
        # self.cliente.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.data_entrega.setText(f"Data da entrega: {dados['data_entrega']}")
        self.data_entrega.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.total.setText(f"Servico: {dados['total']}")
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.nome_loja.setText(f"Nome da loja: {dados['nome_loja']}")
        self.nome_loja.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.estado.setText(f"Estado: {dados['estado_pedido']}")

        self.button_pagar.setEnabled(True)
        self.delete.setEnabled(True)
        self.estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        print("ESTADO ANTES DE TESTAR IFS", dados["estado_pedido"])
        if str(dados["estado_pedido"]).upper() == "PENDENTE":
            self.button_pagar.setEnabled(True)  # Make it unclickable
            self.delete.setEnabled(True)  # Make it unclickable
        if str(dados["estado_pedido"]).upper() == "ENVIADO":
            self.button_pagar.setEnabled(False)  # Make it unclickable
            self.delete.setEnabled(True)  # Make it unclickable
        if str(dados["estado_pedido"]).upper() == "CONCLUIDO":
            self.button_pagar.setEnabled(False)
            self.delete.setEnabled(False)
        self.total.setText(f"Total: {dados['total']}")
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def pagar(self):
        popup = QRCodePopup("https://youtu.be/wLtBGGX8GIk?si=pFbGeLxnuJdIwGU_", self)
        popup.exec()  # This blocks until closed
        resp = pagar_pedido(self.id)
        if not resp[0]:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                str(resp[1]),
            )
        else:
            QMessageBox.information(self, "Sucesso", str(resp[1]))
            self.parent.goto_meus_pedidos()

    def deletar(self):
        resp = cancelar_pedido(self.id)
        if not resp[0]:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                str(resp[1]),
            )
        else:
            QMessageBox.information(self, "Sucesso", str(resp[1]))
            self.parent.goto_meus_pedidos()


class Pedido(QWidget):
    def __init__(
        self, parent, id, data, servico, estado, total, nome_servico, nome_loja
    ):
        super().__init__(parent)
        self.parent = parent
        self.id = id
        self.title = QLabel("Pedido")
        self.title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 25px;
                font-weight: bold;
            }
        """)
        # self.id_label = QLabel(f"id {self.id}")
        self.data = QLabel(f"Data: {data}")
        self.estado = QLabel(f"Estado: {estado}")
        self.total = QLabel(f"Total: {total}")
        self.servico = QLabel(f"Nome do Servico: {nome_servico}")
        self.loja = QLabel(f"Loja: {nome_loja}")
        self.button_ver = QPushButton("Visualizar")
        self.button_ver.clicked.connect(self.visualizar)
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
        layout = QVBoxLayout()

        layout.addStretch()
        # layout.addWidget(self.id_label)
        layout.addWidget(self.data)
        layout.addWidget(self.servico)
        layout.addWidget(self.estado)
        layout.addWidget(self.total)
        layout.addWidget(self.loja)
        layout.addWidget(self.button_ver)
        layout.addStretch()

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def visualizar(self):
        self.parent.goto_pedido_unico(self.id)

    def deletar(self):
        status, message = cancelar_pedido(self.id)
        if not status:
            QMessageBox.warning(
                self,
                "Erro de autenticacao",
                message,
            )
        else:
            self.parent.goto_meus_pedidos()


def load_pedido_loja():
    resp = get_pedidos_minha_loja()
    if not resp[0]:
        raise Exception(resp[1])

    return resp[2]


class PedidosLoja(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

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

        text = QLabel("Página de Pedidos")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
            }
        """)

        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)

        self.lista = QListWidget()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(text)
        self.main_layout.addWidget(self.button_voltar)
        self.main_layout.addWidget(self.lista)
        self.setLayout(self.main_layout)

    def load(self):
        self.lista.clear()
        resp = get_pedidos_minha_loja()
        if not resp[0]:
            QMessageBox.warning(self, "Erro", str(resp[1]))
            return

        print("Pedido loja", resp[2])
        dados = resp[2]
        for dado in dados:
            pedido = Pedido(
                self,
                dado["idPedido"],
                dado["data_pedido"],
                dado["idServico"],
                dado["estado_pedido"],
                dado["total"],
                dado["nome_servico"],
                dado["nome_loja"],
            )
            item = QListWidgetItem()

            item.setSizeHint(pedido.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, dado["idPedido"])

            self.lista.addItem(item)
            self.lista.setItemWidget(item, pedido)

    def goto_pedido_unico(self, id):
        self.parent.goto_pedido_unico_usuario(id)

    def voltar(self):
        self.parent.goto_area_pedidos()


def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            elif item.layout() is not None:
                clear_layout(item.layout())


class MeusPedidos(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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
        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)

        self.title = QLabel("Pagina de Pedidos")

        self.lista = QListWidget()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.button_voltar)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.lista)
        self.setLayout(self.main_layout)

    def load(self):
        # Get pedidos
        self.lista.clear()
        resp = get_pedidos()
        if not resp[0]:
            QMessageBox.warning(self, "Erro", str(resp[1]))
            return

        dados = resp[2]
        print("_________________________--")
        print("Pedidos", dados)

        for dado in dados:
            pedido = Pedido(
                self,
                dado["idPedido"],
                dado["data_pedido"],
                dado["nome_servico"],
                # dado["idServico"],
                dado["estado_pedido"],
                dado["total"],
                dado["nome_servico"],
                dado["nome_loja"],
            )
            print("\n MEU PEDIDO", dado)

            item = QListWidgetItem()

            item.setSizeHint(pedido.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, dado["idPedido"])

            self.lista.addItem(item)
            self.lista.setItemWidget(item, pedido)

    def goto_meus_pedidos(self):
        self.parent.goto_meus_pedidos()

    def goto_pedido_unico(self, id):
        self.parent.goto_pedido_unico(id)

    def voltar(self):
        self.parent.goto_area_pedidos()


# class MeusPedidos(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.pedidos = QLabel("Nada")
#         self.setStyleSheet("""
#             QLabel {
#                 color: #2c3e50;
#                 font-size: 20px;
#             }
#             QPushButton {
#                 color: white;
#                 font-size: 20px;
#                 background-color: #2c3e50;
#             }
#         """)
#
#     def load(self):
#         # Clear existing layout and widgets
#         old_layout = self.layout()
#         if old_layout is not None:
#             clear_layout(old_layout)
#             QWidget().setLayout(old_layout)  # Safe detach (prevents warnings)
#
#         # Get pedidos
#         resp = get_pedidos()
#         if not resp[0]:
#             print("ERRO DOIDO", resp)
#             raise Exception(str(resp[1]))
#
#         dados = resp[2]
#
#         # Build inner layout
#         inner_layout = QVBoxLayout()
#
#         for dado in dados:
#             pedido = Pedido(
#                 self,
#                 dado["idPedido"],
#                 dado["data_pedido"],
#                 dado["servico"],
#                 dado["estado_pedido"],
#                 dado["total"],
#             )
#             inner_layout.addWidget(pedido)
#
#         inner_widget = QWidget()
#         inner_widget.setLayout(inner_layout)
#
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setWidget(inner_widget)
#
#         self.button_voltar = QPushButton("Voltar")
#         self.button_voltar.clicked.connect(self.voltar)
#
#         # New layout
#         main_layout = QVBoxLayout()
#         main_layout.addWidget(self.button_voltar)
#         text = QLabel("Página de Pedidos")
#         text.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         text.setStyleSheet("""
#             QLabel {
#                 color: #2c3e50;
#                 font-size: 20px;
#                 font-weight: bold;
#                 padding: 10px;
#             }
#         """)
#         main_layout.addWidget(text)
#         main_layout.addWidget(scroll)
#
#         # New layout
#         outer_layout = QHBoxLayout()
#         outer_layout.addStretch()
#         outer_layout.addLayout(main_layout)
#         outer_layout.addStretch()
#         self.setLayout(outer_layout)
#
#     def goto_meus_pedidos(self):
#         self.parent.goto_meus_pedidos()
#
#     def goto_pedido_unico(self, id):
#         self.parent.goto_pedido_unico(id)
#
#     def voltar(self):
#         self.parent.goto_area_pedidos()


class AreaPedidos(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title = QLabel("Area de Pedidos")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_pedidos_loja = QPushButton("Visualizar pedidos na minha loja")
        self.button_pedidos_loja.clicked.connect(self.goto_pedidos_loja)
        self.button_meus_pedidos = QPushButton("Visualizar meus próprios pedidos")
        self.button_meus_pedidos.clicked.connect(self.goto_meus_pedidos)
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 25px;
                font-weight: bold;
            }
            QPushButton {
                color: white;
                font-size: 20px;
                background-color: #2c3e50;
            }
        """)
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.button_pedidos_loja)
        layout.addWidget(self.button_meus_pedidos)
        layout.addStretch()
        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def goto_pedidos_loja(self):
        self.parent.goto_pedidos_loja()

    def goto_meus_pedidos(self):
        self.parent.goto_meus_pedidos()


class Pedidos(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.meus_pedidos = MeusPedidos(self)
        self.pedidos_loja = PedidosLoja(self)
        self.area_pedidos = AreaPedidos(self)
        self.pedidos_unico = PedidoUnico(self)
        self.pedidos_unico_usuario = PedidoUnicoUsuario(self)

        self.addWidget(self.meus_pedidos)
        self.addWidget(self.pedidos_loja)
        self.addWidget(self.area_pedidos)
        self.addWidget(self.pedidos_unico)
        self.addWidget(self.pedidos_unico_usuario)

        self.setCurrentWidget(self.area_pedidos)

    def goto_meus_pedidos(self):
        self.meus_pedidos.load()
        self.setCurrentWidget(self.meus_pedidos)

    def goto_area_pedidos(self):
        self.setCurrentWidget(self.area_pedidos)

    def goto_pedido_unico(self, id):
        self.pedidos_unico.load(id)
        self.setCurrentWidget(self.pedidos_unico)

    def goto_pedido_unico_usuario(self, id):
        self.pedidos_unico_usuario.load(id)
        self.setCurrentWidget(self.pedidos_unico_usuario)

    def goto_pedidos_loja(self):
        self.pedidos_loja.load()
        self.setCurrentWidget(self.pedidos_loja)

    def load(self):
        print("Carregando pedidos")
        # self.pedidos_loja.load()
        self.meus_pedidos.load()
