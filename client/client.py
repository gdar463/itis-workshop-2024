# import json
import ctypes
import sys

import qtawesome as qta  # pyright: ignore[reportMissingTypeStubs]
from PyQt6.QtCore import QSize, Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QApplication,
    # QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QFont

from dialog import ServerSettingDialog, RecentSentDialog
from send import get_file_from_server, open_file_dialog
from spinner import QtWaitingSpinner

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        icon = qta.icon("mdi6.cloud-outline", options=[{"scale_factor":1.25}])

        self.setWindowTitle("Key Cloud - Workshop ITIS 2024")
        
        self.ip = "http://localhost:8080"
        self.setWindowIcon(icon)

        widget = MainWidget(self)
        self.setCentralWidget(widget)

    def open_dialog(self):
        _ = ServerSettingDialog(self).exec()


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        recent_button = QPushButton()
        recent_button.setFixedSize(30,30)
        recent_button.setIcon(qta.icon("fa.list-ul"))
        recent_button.setIconSize(QSize(16,18))
        _ = recent_button.clicked.connect(self.show_list)

        options_button = QPushButton()
        options_button.setFixedSize(30,30)
        options_button.setIcon(qta.icon("fa.gear"))
        options_button.setIconSize(QSize(16,18))
        _ = options_button.clicked.connect(parent.open_dialog)

        # options_layout = QGridLayout()
        # options_layout.addWidget(options_button, 0, 0, Qt.AlignmentFlag.AlignRight)

        self.spinner = QtWaitingSpinner(self, True, True, self.windowModality(), 70.0, 70.0, 12, 10, 5, 10)

        title_label = QLabel("<p style=\"font-size:20px\"><b>Key Cloud</b></p>")
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setFont(QFont("PoetsenOne"))
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon("mdi6.cloud-outline").pixmap(48,48))

        self.title_layout = QHBoxLayout()
        self.title_layout.addSpacing(15)
        self.title_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.title_layout.setSpacing(10)
        self.title_layout.addWidget(title_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.title_layout.addStretch()
        self.title_layout.addWidget(recent_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.title_layout.addWidget(options_button, alignment=Qt.AlignmentFlag.AlignRight)

        hint_label = QLabel("<p style=\"font-size:16px\">Benvenuto, scegli cosa fare:</p>")
        hint_label.setTextFormat(Qt.TextFormat.RichText)

        get_button = QPushButton()
        get_button.setText("Scarica file")
        get_button.setStyleSheet("font-size: 14px")
        get_button.setFixedSize(90,32)
        _ = get_button.clicked.connect(self.get_file)

        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("es. 230140")
        
        send_button = QPushButton()
        send_button.setText("Invia file")
        send_button.setStyleSheet("font-size: 14px")
        send_button.setFixedSize(70,32)
        _ = send_button.clicked.connect(self.send_file)
        
        send_layout = QVBoxLayout()
        send_layout.addWidget(self.pass_edit, alignment=Qt.AlignmentFlag.AlignHCenter)
        send_layout.addWidget(get_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # buttons_layer = QHBoxLayout()
        # buttons_layer.addWidget(send_button)
        # buttons_layer.addLayout(send_layout)

        layout = QVBoxLayout()
        # layout.addLayout(options_layout)
        layout.addLayout(self.title_layout)
        layout.addWidget(hint_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(6)
        # layout.addLayout(buttons_layer)
        layout.addWidget(send_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(4)
        layout.addLayout(send_layout)
        self.setLayout(layout)

    @pyqtSlot()
    def send_file(self):
        open_file_dialog(self)
    
    @pyqtSlot()
    def get_file(self):
        result = get_file_from_server(self)
        if result:
            self.pass_edit.setText("")

    def show_list(self):
        _ = RecentSentDialog(self).exec()

myappid = u'gdar463.keycloud.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# QFontDatabase.addApplicationFont("PoetsenOne-Regular.ttf")
app = QApplication(sys.argv)
window = MainWindow()
window.resize(450,240)
window.show()
sys.exit(app.exec())
