import sys
from PyQt6.QtWidgets import (
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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from requestAPI.moc_gpt import (
    cancelar_pedido,
    get_pedido,
    get_pedidos,
    get_pedidos_minha_loja,
)


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


class PedidoUnico(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.id = QLabel("id")
        self.data = QLabel("data:")
        self.servico = QLabel("servico:")
        self.estado = QLabel("estado:")
        self.total = QLabel("total:")
        self.delete = QPushButton("Cancelar pedido")
        self.delete.clicked.connect(self.deletar)
        layout = QVBoxLayout()

        layout.addWidget(self.id)
        layout.addWidget(self.data)
        layout.addWidget(self.servico)
        layout.addWidget(self.estado)
        layout.addWidget(self.total)
        layout.addWidget(self.delete)
        self.setLayout(layout)

    def load(self, id):
        print("AAAAAaaa")
        resp = get_pedido(id)
        if not resp[0]:
            raise Exception(resp[1])

        dados = resp[2]
        print(dados)
        self.id.setText(f"id {id}")
        self.data.setText(f"data: {dados['data_pedido']}")
        self.servico.setText(f"servico: {dados['servico']}")
        self.estado.setText(f"estado: {dados['estado_pedido']}")
        self.total.setText(f"total: {dados['total']}")
        self.delete = QPushButton("Cancelar pedido")

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


class Pedido(QWidget):
    def __init__(self, parent, id, data, servico, estado, total):
        super().__init__(parent)
        self.parent = parent
        self.id = id
        self.id_label = QLabel(f"id {self.id}")
        self.data = QLabel(f"data: {data}")
        self.servico = QLabel(f"servico: {servico}")
        self.estado = QLabel(f"estado: {estado}")
        self.total = QLabel(f"total: {total}")
        self.button_ver = QPushButton("Visualizar")
        self.button_ver.clicked.connect(self.visualizar)
        layout = QVBoxLayout()

        layout.addWidget(self.id_label)
        layout.addWidget(self.data)
        layout.addWidget(self.servico)
        layout.addWidget(self.estado)
        layout.addWidget(self.total)
        layout.addWidget(self.button_ver)

        self.setLayout(layout)

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


class PedidosLoja(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        resp = get_pedidos_minha_loja()
        if not resp[0]:
            raise Exception(resp[1])

        dados = resp[2]
        # Inner layout with Pedido cards
        inner_layout = QVBoxLayout()
        text = QLabel("Página de Pedidos")

        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(text)

        for dado in dados:
            pedido = Pedido(
                self,
                dado["idPedido"],
                dado["data_pedido"],
                dado["servico"],
                dado["estado_pedido"],
                dado["total"],
            )
            inner_layout.addWidget(pedido)

        inner_widget = QWidget()
        inner_widget.setLayout(inner_layout)

        # ScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.button_voltar)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

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
        self.pedidos = QLabel("Nada")
        # resp = get_pedidos()
        # if not resp[0]:
        #     raise Exception(resp[1])
        #
        # dados = resp[2]
        # # Inner layout with Pedido cards
        # inner_layout = QVBoxLayout()
        # text = QLabel("Página de Pedidos")
        # text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # inner_layout.addWidget(text)
        #
        # for dado in dados:
        #     pedido = Pedido(
        #         self,
        #         dado["idPedido"],
        #         dado["data_pedido"],
        #         dado["servico"],
        #         dado["estado_pedido"],
        #         dado["total"],
        #     )
        #     inner_layout.addWidget(pedido)
        #
        # inner_widget = QWidget()
        # inner_widget.setLayout(inner_layout)
        #
        # # ScrollArea
        # scroll = QScrollArea()
        # scroll.setWidgetResizable(True)
        # scroll.setWidget(inner_widget)
        #
        # self.button_voltar = QPushButton("Voltar")
        # self.button_voltar.clicked.connect(self.voltar)
        #
        # main_layout = QVBoxLayout(self)
        # main_layout.addWidget(self.button_voltar)
        # main_layout.addWidget(scroll)
        # self.setLayout(main_layout)

    def load(self):
        # Clear existing layout and widgets
        old_layout = self.layout()
        if old_layout is not None:
            clear_layout(old_layout)
            QWidget().setLayout(old_layout)  # Safe detach (prevents warnings)

        # Get pedidos
        resp = get_pedidos()
        if not resp[0]:
            raise Exception(resp[1])

        dados = resp[2]

        # Build inner layout
        inner_layout = QVBoxLayout()
        text = QLabel("Página de Pedidos")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(text)

        for dado in dados:
            pedido = Pedido(
                self,
                dado["idPedido"],
                dado["data_pedido"],
                dado["servico"],
                dado["estado_pedido"],
                dado["total"],
            )
            inner_layout.addWidget(pedido)

        inner_widget = QWidget()
        inner_widget.setLayout(inner_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner_widget)

        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.clicked.connect(self.voltar)

        # New layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.button_voltar)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def goto_meus_pedidos(self):
        self.parent.goto_meus_pedidos()

    def goto_pedido_unico(self, id):
        self.parent.goto_pedido_unico(id)

    def voltar(self):
        self.parent.goto_area_pedidos()


class AreaPedidos(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.button_pedidos_loja = QPushButton("Visualizar pedidos na minha loja")
        self.button_pedidos_loja.clicked.connect(self.goto_pedidos_loja)
        self.button_meus_pedidos = QPushButton("Visualizar meus próprios pedidos")
        self.button_meus_pedidos.clicked.connect(self.goto_meus_pedidos)
        layout = QVBoxLayout()
        layout.addWidget(self.button_pedidos_loja)
        layout.addWidget(self.button_meus_pedidos)
        self.setLayout(layout)

    def goto_pedidos_loja(self):
        self.parent.goto_pedidos_loja()

    def goto_meus_pedidos(self):
        self.parent.goto_meus_pedidos()


class Pedidos(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.pedidos = MeusPedidos(self)
        self.pedidos_loja = PedidosLoja(self)
        self.area_pedidos = AreaPedidos(self)
        self.pedidos_unico = PedidoUnico(self)

        self.addWidget(self.pedidos)
        self.addWidget(self.pedidos_loja)
        self.addWidget(self.area_pedidos)
        self.addWidget(self.pedidos_unico)

        self.setCurrentWidget(self.area_pedidos)

    def goto_meus_pedidos(self):
        self.pedidos.load()
        self.setCurrentWidget(self.pedidos)

    def goto_area_pedidos(self):
        self.setCurrentWidget(self.area_pedidos)

    def goto_pedido_unico(self, id):
        self.pedidos_unico.load(id)
        self.setCurrentWidget(self.pedidos_unico)

    def goto_pedidos_loja(self):
        self.setCurrentWidget(self.pedidos_loja)
