import sys
from PyQt6.QtWidgets import (
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
from requestAPI.moc_gpt import get_pedidos, get_pedidos_minha_loja


class Pedido(QWidget):
    def __init__(self, parent, id, data, servico, estado, total):
        super().__init__(parent)
        self.id = QLabel(f"id {id}")
        self.data = QLabel(f"data: {data}")
        self.servico = QLabel(f"servico: {servico}")
        self.estado = QLabel(f"estado: {estado}")
        self.total = QLabel(f"total: {total}")

        layout = QVBoxLayout()
        layout.addWidget(self.id)
        layout.addWidget(self.data)
        layout.addWidget(self.servico)
        layout.addWidget(self.estado)
        layout.addWidget(self.total)
        self.setLayout(layout)


class PedidosLoja(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        resp = get_pedidos_minha_loja()
        if not resp[0]:
            raise Exception(resp[1])

        dados = resp[2]
        # Inner layout with Pedido cards
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

        # ScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)


class PedidosLista(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        resp = get_pedidos()
        if not resp[0]:
            raise Exception(resp[1])

        dados = resp[2]
        # Inner layout with Pedido cards
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

        # ScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)


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
        self.pedidos = PedidosLista(self)
        self.addWidget(self.pedidos)
        self.pedidos_loja = PedidosLoja(self)
        self.addWidget(self.pedidos_loja)
        self.area_pedidos = AreaPedidos(self)
        self.addWidget(self.area_pedidos)

        self.setCurrentWidget(self.area_pedidos)

    def goto_meus_pedidos(self):
        self.setCurrentWidget(self.pedidos)

    def goto_pedidos_loja(self):
        self.setCurrentWidget(self.pedidos_loja)
