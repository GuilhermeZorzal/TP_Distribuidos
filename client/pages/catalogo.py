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


from requestAPI.moc_gpt import get_catalogo, get_categoria


class ServiceItemWidget(QWidget):
    def __init__(self, service):
        super().__init__()
        layout = QVBoxLayout()

        desc = QLabel(service["descricao_servico"])
        category = QLabel(f"Categoria: {service['categoria']}")
        payment = QLabel(
            f"Pagamento: {service['tipo_pagamento']} - R$ {service['quantidade_pagamento']}"
        )
        visibility = QLabel("Visível" if service["esta_visivel"] else "Oculto")

        layout.addWidget(desc)
        layout.addWidget(category)
        layout.addWidget(payment)
        layout.addWidget(visibility)

        self.setLayout(layout)


class Catalogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_page = 0
        self.page_size = 10
        self.is_loading = False

        # UI setup
        self.main_layout = QVBoxLayout()
        self.user_list = QListWidget()

        self.search_box = QComboBox()
        status, message, categorias = get_categoria()
        self.search_box.addItems(categorias)
        self.search_box.currentIndexChanged.connect(self.filter_services)

        self.main_layout.addWidget(self.search_box)
        self.main_layout.addWidget(self.user_list)
        self.setLayout(self.main_layout)

        # Connect scroll after user_list is created
        self.user_list.verticalScrollBar().valueChanged.connect(
            self.check_scroll_position
        )

        self.load_services()

    def filter_services(self, text):
        self.current_page = 0
        self.load_services(filter_text=text, append=False)

    def load_services(self, filter_text="", append=False):
        if self.is_loading:
            return

        self.is_loading = True
        try:
            resp = get_catalogo(filter_text)
            if not resp[0]:
                raise Exception(resp[1])
            services = resp[2]

            if not append:
                self.user_list.clear()

            for service in services:
                item = QListWidgetItem()
                widget = ServiceItemWidget(service)
                item.setSizeHint(widget.sizeHint())
                self.user_list.addItem(item)
                self.user_list.setItemWidget(item, widget)

            if services:
                self.current_page += 1

        except Exception as e:
            print(f"Erro ao carregar serviços: {e}")
        finally:
            self.is_loading = False

    def check_scroll_position(self):
        scroll_bar = self.user_list.verticalScrollBar()
        if scroll_bar.value() >= scroll_bar.maximum() - 50:
            self.load_services(filter_text=self.search_box.currentText(), append=True)


# class Catalogo(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         layout = QVBoxLayout(self)
#
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#
#         container = CardGrid()
#         scroll.setWidget(container)
#
#         layout.addWidget(scroll)
#


class Card(QWidget):
    def __init__(self, title, image_path=None):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        button = QPushButton("View")
        layout.addWidget(button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                border-radius: 8px;
                border: 1px solid #bdc3c7;
                padding: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)


class CardGrid(QWidget):
    def __init__(self, cards_per_row=3):
        super().__init__()
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        num_cards = 12  # example
        for index in range(num_cards):
            row = index // cards_per_row
            col = index % cards_per_row
            card = Card(f"Card {index + 1}", "./assets/card.png")  # optional image
            grid.addWidget(card, row, col)


class ScrollableGrid(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = CardGrid()
        scroll.setWidget(container)

        layout.addWidget(scroll)
