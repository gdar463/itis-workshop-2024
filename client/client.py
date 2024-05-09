# import json
import sys

from PyQt6.QtCore import Qt, pyqtSlot  
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from send import open_file_dialog, get_file_from_server
from spinner import QtWaitingSpinner


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        ip_label = QLabel("<p style=\"font-size:14px\">Inserisci l'indirizzo http del server</p>")
        ip_label.setTextFormat(Qt.TextFormat.RichText)
        self.ip_edit = QLineEdit()
        self.ip_edit.setText("http://localhost:8080")
        self.ip_edit.setPlaceholderText("http://localhost:8080")

        send_button = QPushButton(self)
        send_button.setText("Invia file")
        send_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        _ = send_button.clicked.connect(self.send_file)

        self.spinner = QtWaitingSpinner(self, True, True, self.windowModality())
        self.spinner.setRoundness(70.0)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(70.0)
        self.spinner.setNumberOfLines(12)
        self.spinner.setLineLength(10)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(10)
        self.spinner.setRevolutionsPerSecond(1)
        self.spinner.setColor(QColor(81, 4, 71)) # pyright: ignore[reportArgumentType]
        
        pass_label = QLabel("<p style=\"font-size:14px\">Inserisci la password del file che stai cercando</p>")
        ip_label.setTextFormat(Qt.TextFormat.RichText)
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("es. 230140")

        get_button = QPushButton(self)
        get_button.setText("Ottieni file")
        _ = get_button.clicked.connect(self.get_file)

        layout = QVBoxLayout()
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_edit)
        layout.addSpacing(15)
        layout.addWidget(send_button)
        layout.addSpacing(15)
        layout.addWidget(pass_label)
        layout.addWidget(self.pass_edit)
        layout.addWidget(get_button)
        self.setLayout(layout)

    @pyqtSlot()
    def send_file(self):
        open_file_dialog(self)
    
    @pyqtSlot()
    def get_file(self):
        get_file_from_server(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
