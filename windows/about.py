from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

from utils.styles import button_dark_style, button_light_style
from utils.assets import is_dark_theme

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About Pitpac")
        self.setGeometry(1100, 400, 700, 300)

        self.about_text = """
            <p style='font-size:16px'>Pitpac is a desktop application allows you to convert images to pdf files or cobine pdf files into one pdf file.</p>
            <p style='font-size:14px; line-height:1.2'>
                Version: 4.1.0<br>
                Owner: Mohammad Keshtegar<br>
                Also you can find the source code <a href='https://github.com/MohammadKeshtegar/pitpac' >here</a>
                <br />
                <br />
                If your faced any issues or have any question, feel free to ask me at:
                <a style='font-size:14px' href='https://t.me/MohammadKeshtegar1401'>@MohammadKeshtegar1401</a>
            </p>
        """

        layout = QVBoxLayout()
        label = QLabel(self.about_text, self)

        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        label.setFixedWidth(self.width() - 100)
        label.setFixedHeight(self.height() - 100)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.ok_button = QPushButton("Ok", self)
        self.ok_button.setFixedWidth(100)
        self.ok_button.clicked.connect(self.close_about)

        layout.addStretch(1)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)

        layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        if is_dark_theme():
            self.apply_about_dark_style()
        else:
            self.apply_about_light_style()

        self.setLayout(layout)

    def apply_about_dark_style(self):
        self.setStyleSheet("background-color: #222222")
        self.ok_button.setStyleSheet(button_dark_style)

    def apply_about_light_style(self):
        self.setStyleSheet("background-color: #f5f5f5; color: #222222")
        self.ok_button.setStyleSheet(button_light_style)

    def close_about(self):
        self.close()