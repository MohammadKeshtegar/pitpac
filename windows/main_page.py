from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt

from assets import is_dark_theme
from styles import button_size, button_dark_style, button_light_style

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setup_main_page()

    def setup_main_page(self):
        layout = QVBoxLayout(self.main_page)

        # Creating main buttons
        self.img2pdf_button = QPushButton('Image to PDF')
        self.pdf_combiner_button = QPushButton("Combine PDFs")
        self.image_resizer_button = QPushButton("Image resizer")
        self.text_from_image_button = QPushButton("Text from image")
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")
        self.close_app_button = QPushButton("Exit")

        # Setting fix size for buttons
        self.img2pdf_button.setFixedWidth(button_size)
        self.pdf_combiner_button.setFixedWidth(button_size)
        self.image_resizer_button.setFixedWidth(button_size)
        self.text_from_image_button.setFixedWidth(button_size)
        self.settings_button.setFixedWidth(button_size)
        self.about_button.setFixedWidth(button_size)
        self.close_app_button.setFixedWidth(button_size)

        # Setting buttons function
        self.pdf_combiner_button.clicked.connect(self.show_pdf_combiner_page)
        self.img2pdf_button.clicked.connect(self.show_img2pdf_page)
        self.image_resizer_button.clicked.connect(self.show_image_resizer_page)
        self.text_from_image_button.clicked.connect(self.show_text_from_image_page)
        self.settings_button.clicked.connect(self.show_settings_window)
        self.about_button.clicked.connect(self.show_about_window)
        self.close_app_button.clicked.connect(self.close_app)

        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)

        if is_dark_theme():
            self.apply_main_dark_style()
        else:
            self.apply_main_light_style()

        # Configuring buttons
        button_layout.addWidget(self.img2pdf_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.pdf_combiner_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.image_resizer_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.text_from_image_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.about_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.close_app_button, alignment=Qt.AlignCenter)

        layout.addStretch(1)
        layout.addWidget(button_container, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.main_page.setLayout(layout)

    # Main styles
    def apply_main_dark_style(self):
        self.main_page.setStyleSheet("background: #1e1e1e")
        self.img2pdf_button.setStyleSheet(button_dark_style)
        self.image_resizer_button.setStyleSheet(button_dark_style)
        self.pdf_combiner_button.setStyleSheet(button_dark_style)
        self.settings_button.setStyleSheet(button_dark_style)
        self.about_button.setStyleSheet(button_dark_style)
        self.close_app_button.setStyleSheet(button_dark_style)

    def apply_main_light_style(self):
        self.main_page.setStyleSheet("background: #f5f5f5; color: #000000")
        self.img2pdf_button.setStyleSheet(button_light_style)
        self.image_resizer_button.setStyleSheet(button_light_style)
        self.pdf_combiner_button.setStyleSheet(button_light_style)
        self.settings_button.setStyleSheet(button_light_style)
        self.about_button.setStyleSheet(button_light_style)
        self.close_app_button.setStyleSheet(button_light_style)
