from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QVBoxLayout
import qtawesome as qta # pyright: ignore[reportMissingTypeStubs]


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


if __name__ == "__main__":
    pass
