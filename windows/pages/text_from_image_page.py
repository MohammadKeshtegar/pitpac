from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QPushButton, QTextEdit, QComboBox, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PIL import Image

from utils.backButton import BackButton

from utils.styles import button_dark_style, button_light_style, scroll_area_dark_style, scroll_area_light_style, combobox_dark_style ,combobox_light_style
from utils.assets import is_dark_theme, settings
from utils.notification import notification

import pytesseract

class TextFromImagePage(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
        self.setup_text_from_image_page()

    def setup_text_from_image_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.back_button = BackButton(mainWindowObject=self.mainWindowObject)

        self.text_container = QWidget()
        self.text_container_layout = QVBoxLayout()
        self.text_container_layout.setContentsMargins(0, 0, 0, 0)
        self.text_container.setLayout(self.text_container_layout)

        self.text_scroll_area = QScrollArea()
        self.text_scroll_area.setWidgetResizable(True)

        font = QFont("Arial", 12)
        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)

        self.text_widget = QWidget()
        self.text_layout = QVBoxLayout(self.text_widget)
        self.text_layout.setContentsMargins(0, 0, 0, 0)
        
        self.copy_button_widget = QWidget()
        self.copy_button_layout = QHBoxLayout()
        self.copy_button_layout.setContentsMargins(5,5,5,3)
        self.copy_button_layout.addStretch()
        self.copy_button_widget.setLayout(self.copy_button_layout)
        self.copy_button = QPushButton("Copy", self.textEdit)
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copyText)
        self.copy_button_layout.addWidget(self.copy_button)
        
        self.text_layout.addWidget(self.copy_button_widget)
        self.text_layout.addWidget(self.textEdit)

        self.text_scroll_area.setWidget(self.text_widget)
        self.text_container_layout.addWidget(self.text_scroll_area)

        self.buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        self.buttons_widget.setLayout(buttons_layout)

        self.select_image_to_extract_button = QPushButton("Select image", self)
        self.select_image_to_extract_button.clicked.connect(self.selectImage)

        self.select_language_menu = QComboBox(self)
        self.select_language_menu.setFixedWidth(100)
        self.select_language_menu.addItem("English", "eng")
        self.select_language_menu.addItem("Farsi", "fas")
        self.select_language_menu.setCurrentIndex(0)
        self.language = self.select_language_menu.currentData()
        self.select_language_menu.currentIndexChanged.connect(self.set_language)

        self.save_text_button = QPushButton("Save Text")
        self.save_text_button.setEnabled(False)
        self.save_text_button.clicked.connect(self.save_text_into_file)

        buttons_layout.addWidget(self.select_image_to_extract_button, alignment=Qt.AlignmentFlag.AlignLeft)
        buttons_layout.addWidget(self.select_language_menu, alignment=Qt.AlignmentFlag.AlignLeft)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.save_text_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.back_button)
        layout.addWidget(self.text_container)
        layout.addWidget(self.buttons_widget)

        if is_dark_theme():
            self.apply_text_from_image_dark_style()
        else:
            self.apply_text_from_image_light_style()

    def selectImage(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif *.jfif)", options=options)
        if filenames:
            self.extractText(filenames[0])
            self.copy_button.setEnabled(True)
            self.save_text_button.setEnabled(True)

    def extractText(self, filename):
        image = Image.open(filename)
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(image, lang=self.language, config=custom_config)
        self.textEdit.setPlainText(text)

    def copyText(self):
        self.textEdit.selectAll()
        self.textEdit.copy()
        notification(self.text_container, "Copied")

    def set_language(self, index):
        self.select_language_menu.setCurrentIndex(index)
        self.language = self.select_language_menu.currentData()

    def save_text_into_file(self):
        text = self.textEdit.toPlainText()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Text", settings.location, "Text Files (*.txt);;All Files (*)")
        if save_path:
            with open(f"{save_path}.txt", 'w') as f:
                f.write(text)

    # Text from image
    def apply_text_from_image_dark_style(self):
        self.central_widget.setStyleSheet("background-color: #262626")
        self.text_scroll_area.setStyleSheet(scroll_area_dark_style)
        self.textEdit.setStyleSheet("background-color: #333333")
        self.select_image_to_extract_button.setStyleSheet(button_dark_style)
        self.copy_button.setStyleSheet(button_dark_style)
        self.save_text_button.setStyleSheet(button_dark_style)
        self.select_language_menu.setStyleSheet(combobox_dark_style)

    def apply_text_from_image_light_style(self):
        self.central_widget.setStyleSheet("background-color: #e5e5e5")
        self.text_scroll_area.setStyleSheet(scroll_area_light_style)
        self.textEdit.setStyleSheet("background-color: #a5a5a5")
        self.select_image_to_extract_button.setStyleSheet(button_light_style)
        self.copy_button.setStyleSheet(button_light_style)
        self.save_text_button.setStyleSheet(button_light_style)
        self.select_language_menu.setStyleSheet(combobox_light_style)
