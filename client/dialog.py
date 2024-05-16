from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, 
    QDialogButtonBox, 
    # QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QScrollArea, 
    QVBoxLayout, 
    QWidget
    )
import qtawesome as qta # pyright: ignore[reportMissingTypeStubs]
import datetime

class Dialog(QDialog):
    def __init__(self, title: str, message: str):
        super().__init__()

        self.setWindowTitle(title)
        icon = qta.icon("mdi6.cloud-outline", options=[{"scale_factor":1.25}])
        self.setWindowIcon(icon)
        
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button.accepted.connect(self.accept) # type: ignore[reportUnknownVariableType]
        
        label = QLabel(message)
        label.setTextFormat(Qt.TextFormat.RichText)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)


class ServerSettingDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setWindowTitle("Indirizzo Server")
        icon = qta.icon("mdi6.cloud-outline", options=[{"scale_factor":1.25}])
        self.setWindowIcon(icon)
        
        QBtn = QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok

        button = QDialogButtonBox(QBtn)
        button.accepted.connect(self.ok) # type: ignore[reportUnknownVariableType]
        button.rejected.connect(self.reject) # type: ignore[reportUnknownVariableType]

        label = QLabel("<p style=\"font-size:13px\">Inserisci l'indirizzo http del server</p>")
        label.setTextFormat(Qt.TextFormat.RichText)
        
        self.ip_edit = QLineEdit()
        self.ip_edit.setText(parent.ip)
        self.ip_edit.setPlaceholderText("es. http://localhost:8080")

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.ip_edit)
        layout.addWidget(button)
        self.setLayout(layout)

    def ok(self):
        self.parent().ip = self.ip_edit.text() # type: ignore[reportUnknownVariableType]
        self.accept()


class RecentSentDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        scroll = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.setWindowTitle("Scaricati di recente")
        icon = qta.icon("mdi6.cloud-outline", options=[{"scale_factor":1.25}])
        self.setWindowIcon(icon)

        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        _ = button.accepted.connect(self.accept)

        try:
            with open("recent.txt", "r+t") as f:
                recent = f.readlines()
        except Exception:
            _ = Dialog("Errore", "Non esiste il file 'recent.txt'. " +
                       "Probabilemente non hai ancora inviato qualcosa").exec()
            _ = self.close()
            return
        
        if len(recent) == 0:
            _ = Dialog("Errore", "Non hai ancora inviato qualcosa che non sia già stato inviato").exec()
            _ = self.close()
            return

        for i in range(len(recent)):
            item = recent[i].split(";")
            label = QLabel("- Name: " + item[0] + " Password: " + item[1] + " Date: " + datetime.datetime.fromtimestamp(float(item[2])).strftime("%d-%m-%Y %H:%M:%S"))
            label.setStyleSheet("font-size:14px")
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(label)

        widget.setLayout(layout)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        layout.addWidget(button)

        self.resize(600,800)
        self.setLayout(layout)
    


if __name__ == "__main__":
    pass
