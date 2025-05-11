import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QScrollArea,
    QGridLayout,
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


class Catalogo(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = CardGrid()
        scroll.setWidget(container)

        layout.addWidget(scroll)


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
