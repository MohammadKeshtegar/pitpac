from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from utils.assets import is_dark_theme

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About Pitpac")
        self.setGeometry(800, 300, 600, 300)

        self.about_text = """
            <p style='font-size:16px'>Pitpac is a desktop application allows you to convert images to pdf files or cobine pdf files into one pdf file.</p>
            <p style='font-size:14px; line-height:1.2'>
                Version: 3.2.2<br>
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
        label.setFixedWidth(500)

        ok_button = QPushButton("Ok", self)
        ok_button.clicked.connect(self.close_about)

        layout.addStretch(1)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        if is_dark_theme():
            self.apply_about_dark_style()
        else:
            self.apply_about_light_style()

        self.setLayout(layout)

    def apply_about_dark_style(self):
        self.setStyleSheet("background-color: #222222")

    def apply_about_light_style(self):
        self.setStyleSheet("background-color: #f5f5f5; color: #222222")

    def close_about(self):
        self.close()