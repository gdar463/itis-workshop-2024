from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

from spinner import QtWaitingSpinner

class Dialog(QDialog):
    def __init__(self, title: str, message: str):
        super().__init__()

        self.setWindowTitle(title)
        
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button.accepted.connect(self.accept) # type: ignore[reportUnknownVariableType]
        
        label = QLabel(message)
        label.setTextFormat(Qt.TextFormat.RichText)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)


class LoadingDialog(QDialog):
    def __init__(self, title: str):
        super().__init__()

        self.setWindowTitle(title)
        
        spinner = QtWaitingSpinner(self, True)
        spinner.setRoundness(70.0) # pyright: ignore[reportUnknownMemberType]
        spinner.setMinimumTrailOpacity(15.0) # pyright: ignore[reportUnknownMemberType]
        spinner.setTrailFadePercentage(70.0) # pyright: ignore[reportUnknownMemberType]
        spinner.setNumberOfLines(12) # pyright: ignore[reportUnknownMemberType]
        spinner.setLineLength(10) # pyright: ignore[reportUnknownMemberType]
        spinner.setLineWidth(5) # pyright: ignore[reportUnknownMemberType]
        spinner.setInnerRadius(10) # pyright: ignore[reportUnknownMemberType]
        spinner.setRevolutionsPerSecond(1) # pyright: ignore[reportUnknownMemberType]
        spinner.setColor(QColor(81, 4, 71)) # pyright: ignore[reportArgumentType]

        spinner.start()
        
        layout = QVBoxLayout()
        layout.addWidget(spinner)
        self.setLayout(layout)


if __name__ == "__main__":
    pass
