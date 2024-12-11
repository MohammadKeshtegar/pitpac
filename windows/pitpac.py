from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from utils.styles import button_size, button_dark_style, button_light_style
from utils.assets import is_dark_theme, PATH_TO_FILE
from utils.assets import settings

from pages.text_from_image_page import TextFromImagePage
from pages.image_resizer_page import ImageResizerPage
from pages.pdf_combiner_page import PDFCombinerPage
from pages.image_to_pdf_page import Image2PDFPage

from video_size_reducer import VideoSizeReducer
from settings import SettingsWindow
from about import AboutWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pitpac")
        self.setGeometry(600, 250, 600, 600)
        self.setWindowIcon(QIcon(f'{PATH_TO_FILE}app-icon.png'))

        self.initUI()

        if is_dark_theme():
            self.apply_main_dark_style()
        else:
            self.apply_main_light_style()

        self.about_window = None
        self.settings_window = None
        self.video_size_reducer_window = None

    def initUI(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Main page
        self.main_page = QWidget()
        self.setup_main_page()
        self.stack.addWidget(self.main_page)

        # Image to pdf pages
        self.image2pdf_page = Image2PDFPage(self)
        self.stack.addWidget(self.image2pdf_page)

        # PDF combiner page
        self.pdf_combiner_page = PDFCombinerPage(self)
        self.stack.addWidget(self.pdf_combiner_page)

        # Image resizer page
        self.image_resizer_page = ImageResizerPage(self)
        self.stack.addWidget(self.image_resizer_page)

        # Text from image page
        self.text_from_image_page = TextFromImagePage(self)
        self.stack.addWidget(self.text_from_image_page)

        self.show_main_page()

    def setup_main_page(self):
        layout = QVBoxLayout(self.main_page)

        # Creating main buttons
        self.image2pdf_button = QPushButton('Image to PDF')
        self.pdf_combiner_button = QPushButton("Combine PDFs")
        self.image_resizer_button = QPushButton("Image resizer")
        self.text_from_image_button = QPushButton("Text from image")
        self.video_size_reducer_button = QPushButton("Video Size Reducer")
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")
        self.close_app_button = QPushButton("Exit")

        # Setting fix size for buttons
        self.image2pdf_button.setFixedWidth(button_size)
        self.pdf_combiner_button.setFixedWidth(button_size)
        self.image_resizer_button.setFixedWidth(button_size)
        self.text_from_image_button.setFixedWidth(button_size)
        self.video_size_reducer_button.setFixedWidth(button_size)
        self.settings_button.setFixedWidth(button_size)
        self.about_button.setFixedWidth(button_size)
        self.close_app_button.setFixedWidth(button_size)

        # buttons font family and size
        self.image2pdf_button.setFont(QFont(settings.font_family, settings.font_size))
        self.pdf_combiner_button.setFont(QFont(settings.font_family, settings.font_size))
        self.image_resizer_button.setFont(QFont(settings.font_family, settings.font_size))
        self.text_from_image_button.setFont(QFont(settings.font_family, settings.font_size))
        self.video_size_reducer_button.setFont(QFont(settings.font_family, settings.font_size))
        self.settings_button.setFont(QFont(settings.font_family, settings.font_size))
        self.about_button.setFont(QFont(settings.font_family, settings.font_size))
        self.close_app_button.setFont(QFont(settings.font_family, settings.font_size))

        # Setting buttons function
        self.pdf_combiner_button.clicked.connect(self.show_pdf_combiner_page)
        self.image2pdf_button.clicked.connect(self.show_img2pdf_page)
        self.image_resizer_button.clicked.connect(self.show_image_resizer_page)
        self.text_from_image_button.clicked.connect(self.show_text_from_image_page)
        self.video_size_reducer_button.clicked.connect(self.show_video_decrease_size_page)
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
        button_layout.addWidget(self.image2pdf_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.pdf_combiner_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.image_resizer_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.text_from_image_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.video_size_reducer_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.about_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.close_app_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(1)
        layout.addWidget(button_container, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.main_page.setLayout(layout)

    def show_main_page(self):
        self.stack.setCurrentWidget(self.main_page)

    def show_img2pdf_page(self):
        self.stack.setCurrentWidget(self.image2pdf_page)

    def show_pdf_combiner_page(self):
        self.stack.setCurrentWidget(self.pdf_combiner_page)

    def show_image_resizer_page(self):
        self.stack.setCurrentWidget(self.image_resizer_page)

    def show_text_from_image_page(self):
        self.stack.setCurrentWidget(self.text_from_image_page)

    def show_video_decrease_size_page(self):
        self.video_size_reducer_window = VideoSizeReducer()
        self.video_size_reducer_window.show()

    def close_app(self):
        if self.settings_window:
            self.settings_window.close()
        if self.about_window:
            self.about_window.close()
        if self.video_size_reducer_window:
            self.video_size_reducer_window.close()
        self.close()

    def show_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.show()

        if self.settings_window and self.settings_window.isVisible:
            self.settings_window.aboutWindowObject = self.about_window

    def show_settings_window(self):
        self.settings_window = SettingsWindow(self, self.about_window)
        self.settings_window.show()

    # Main styles
    def apply_main_dark_style(self):
        self.main_page.setStyleSheet("background: #1e1e1e")
        self.image2pdf_button.setStyleSheet(button_dark_style)
        self.image_resizer_button.setStyleSheet(button_dark_style)
        self.pdf_combiner_button.setStyleSheet(button_dark_style)
        self.text_from_image_button.setStyleSheet(button_dark_style)
        self.video_size_reducer_button.setStyleSheet(button_dark_style)
        self.settings_button.setStyleSheet(button_dark_style)
        self.about_button.setStyleSheet(button_dark_style)
        self.close_app_button.setStyleSheet(button_dark_style)

    def apply_main_light_style(self):
        self.main_page.setStyleSheet("background: #f5f5f5; color: #000000")
        self.image2pdf_button.setStyleSheet(button_light_style)
        self.image_resizer_button.setStyleSheet(button_light_style)
        self.pdf_combiner_button.setStyleSheet(button_light_style)
        self.text_from_image_button.setStyleSheet(button_light_style)
        self.video_size_reducer_button.setStyleSheet(button_light_style)
        self.settings_button.setStyleSheet(button_light_style)
        self.about_button.setStyleSheet(button_light_style)
        self.close_app_button.setStyleSheet(button_light_style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
