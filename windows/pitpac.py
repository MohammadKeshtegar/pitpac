from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from utils.assets import PATH_TO_FILE, settings
from utils.styles import load_styles

from pages.image_resizer_page import ImageResizerPage
from pages.pdf_combiner_page import PDFCombinerPage
from pages.image_to_pdf_page import Image2PDFPage

from video_size_reducer import VideoSizeReducer
from settings import SettingsWindow
from about import AboutWindow

import sys

class Pitpac(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pitpac")
        self.setGeometry(600, 250, 600, 600)
        self.setWindowIcon(QIcon(f'{PATH_TO_FILE}app-icon.png'))
        self.setProperty("class", "base")

        self.initUI()
        load_styles(self)

        self.about_window = None
        self.settings_window = None
        self.current_animation = None
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

        self.show_main_page()

    def setup_main_page(self):
        layout = QVBoxLayout(self.main_page)

        # Creating main buttons
        self.image2pdf_button = QPushButton('Image to PDF')
        self.pdf_combiner_button = QPushButton("Combine PDFs")
        self.image_resizer_button = QPushButton("Image resizer")
        self.video_size_reducer_button = QPushButton("Video Size Reducer")
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")
        self.close_app_button = QPushButton("Exit")

        self.image2pdf_button.setProperty("class", "button-dark")
        self.pdf_combiner_button.setProperty("class", "button-dark")
        self.image_resizer_button.setProperty("class", "button-dark")
        self.video_size_reducer_button.setProperty("class", "button-dark")
        self.settings_button.setProperty("class", "button-dark")
        self.about_button.setProperty("class", "button-dark")
        self.close_app_button.setProperty("class", "button-dark")

        # Setting fix size for buttons
        self.image2pdf_button.setFixedWidth(300)
        self.pdf_combiner_button.setFixedWidth(300)
        self.image_resizer_button.setFixedWidth(300)
        self.video_size_reducer_button.setFixedWidth(300)
        self.settings_button.setFixedWidth(300)
        self.about_button.setFixedWidth(300)
        self.close_app_button.setFixedWidth(300)

        # Setting buttons function
        self.pdf_combiner_button.clicked.connect(self.show_pdf_combiner_page)
        self.image2pdf_button.clicked.connect(self.show_img2pdf_page)
        self.image_resizer_button.clicked.connect(self.show_image_resizer_page)
        self.video_size_reducer_button.clicked.connect(self.show_video_decrease_size_page)
        self.settings_button.clicked.connect(self.show_settings_window)
        self.about_button.clicked.connect(self.show_about_window)
        self.close_app_button.clicked.connect(self.closeEvent)

        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)

        # Configuring buttons
        button_layout.addWidget(self.image2pdf_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.pdf_combiner_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.image_resizer_button, alignment=Qt.AlignmentFlag.AlignCenter)
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

    def show_video_decrease_size_page(self):
        self.video_size_reducer_window = VideoSizeReducer()
        self.video_size_reducer_window.show()

    # The name of this function is a little different from other, be cause it's the main window close event.
    def closeEvent(self, event):
        if self.settings_window:
            self.settings_window.close()
        if self.about_window:
            self.about_window.close()
        if self.video_size_reducer_window:
            self.video_size_reducer_window.close()
        if self.image_resizer_page.image_display_window:
            self.image_resizer_page.image_display_window.close()
        self.close()

    def show_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.show()

        if self.settings_window and self.settings_window.isVisible:
            self.settings_window.aboutWindowObject = self.about_window

    def show_settings_window(self):
        self.settings_window = SettingsWindow(self, self.about_window)
        self.settings_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont(settings.font_family, settings.font_size))
    window = Pitpac()
    window.show()
    sys.exit(app.exec_())
