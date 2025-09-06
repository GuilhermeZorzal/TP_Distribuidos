from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QDialog,
    QApplication,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QImage

import qrcode
import sys
import io


class QRCodePopup(QDialog):
    closed = pyqtSignal()  # Sinal personalizado

    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("QR Code")
        self.setModal(True)

        layout = QVBoxLayout()

        qr_image = self.generate_qr_image(data)
        qr_label = QLabel()
        qr_label.setPixmap(qr_image)
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(qr_label)
        self.setLayout(layout)

    def generate_qr_image(self, data):
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        qimage = QImage.fromData(buffer.getvalue())
        return QPixmap.fromImage(qimage)

    def closeEvent(self, event):
        self.closed.emit()  # Emite sinal quando fechado
        super().closeEvent(event)
