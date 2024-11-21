import io
import sys
import PyPDF4
import img2pdf
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QScrollArea, QHBoxLayout, QStackedWidget, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage, QIntValidator
from PyQt5.QtCore import Qt
from pyqttoast import Toast, ToastPreset, ToastPosition
from PIL import Image

from about import AboutWindow
from assets import is_dark_theme, settings, PATH_TO_FILE
from settings import SettingsWindow
from image_preview import ImageDisplayWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pitpac")
        self.setGeometry(600, 250, 600, 600)
        self.setWindowIcon(QIcon(f'{PATH_TO_FILE}app-icon.png'))

        self.button_dark_style = f"""
            QPushButton:disabled {{ color: #525252 }} 
            QPushButton {{ padding: 5px 10px }} 
            QPushButton:hover {{ background-color: #313131 }}
        """

        self.button_light_style = f"""
            QPushButton:disabled {{ color: #646464 }} 
            QPushButton {{ padding: 5px 10px; color: #262626 }} 
            QPushButton:hover {{ background-color: #4464e6 }}
        """

        self.scroll_area_dark_style = """
            QScrollBar:vertical { background-color: #262626; border: 1px solid #111111 }
            QScrollBar::handle:vertical { margin: 16px 0; border-radius: 2px; border: 1px solid #404040; background-color: #1e1e1e }
            QScrollBar::handle:vertical:pressed { background-color: #333333 }
            QScrollBar:horizontal { background-color: #262626; border: 1px solid #111111 }
            QScrollBar::handle:horizontal { margin: 0 16px; border-radius: 2px; border: 1px solid #404040; background-color: #1e1e1e }
            QScrollBar::handle:horizontal:pressed { background-color: #333333 }
            QScrollArea { background-color: #525252 }
        """

        self.scroll_area_light_style = """
            QScrollBar:vertical { background-color: #b5b5b5; border: 1px solid #737373 }
            QScrollBar::handle:vertical { margin: 16px 0; border-radius: 2px; border: 1px solid #626262; background-color: #7f7f7f }
            QScrollBar::handle:vertical:pressed { background-color: #333333 }
            QScrollBar:horizontal { background-color: #b5b5b5; border: 1px solid #737373 }
            QScrollBar::handle:horizontal { margin: 0 16px; border-radius: 2px; border: 1px solid #626262; background-color: #7f7f7f }
            QScrollBar::handle:horizontal:pressed { background-color: #333333 }
            QScrollArea { background-color: #646464 }
        """

        self.remove_button_dark_style = f"""
            QPushButton {{ background-color: #1a1a1a; border: 1px solid #404040 }} 
            QPushButton:hover {{ background-color: #313131 }}
        """
        
        self.remove_button_light_style = f"""
            QPushButton {{ background-color: #fff; border: 1px solid #a3a3a3 }} 
            QPushButton:hover {{ background-color: #4464e6 }}
        """

        self.button_size = 400
        self.initUI()
        self.image_display_window = ImageDisplayWindow()


        if is_dark_theme():
            self.apply_main_dark_style()
        else:
            self.apply_main_light_style()

        self.about_window = None
        self.settings_window = None

    # Main styles
    def apply_main_dark_style(self):
        self.main_page.setStyleSheet("background: #1e1e1e")
        self.img2pdf_button.setStyleSheet(self.button_dark_style)
        self.image_resizer_button.setStyleSheet(self.button_dark_style)
        self.pdf_combiner_button.setStyleSheet(self.button_dark_style)
        self.settings_button.setStyleSheet(self.button_dark_style)
        self.about_button.setStyleSheet(self.button_dark_style)
        self.close_app_button.setStyleSheet(self.button_dark_style)
    
    def apply_main_light_style(self):
        self.main_page.setStyleSheet("background: #f5f5f5; color: #000000")
        self.img2pdf_button.setStyleSheet(self.button_light_style)
        self.image_resizer_button.setStyleSheet(self.button_light_style)
        self.pdf_combiner_button.setStyleSheet(self.button_light_style)
        self.settings_button.setStyleSheet(self.button_light_style)
        self.about_button.setStyleSheet(self.button_light_style)
        self.close_app_button.setStyleSheet(self.button_light_style)
    
    # Img to pdf styles
    def apply_img_to_pdf_dark_style(self):
        self.img2pdf_page.setStyleSheet("background-color: #262626; color: #e5e5e5")
        self.back_button.setStyleSheet(self.button_dark_style)
        self.scroll_area.setStyleSheet(self.scroll_area_dark_style)
        self.image_container.setStyleSheet("background-color: #333333")
        self.button_img_to_pdf_select.setStyleSheet(self.button_dark_style)
        self.button_img_to_pdf_add.setStyleSheet(self.button_dark_style)
        self.button_img_to_pdf_remove_all.setStyleSheet(self.button_dark_style)
        self.button_img_to_pdf_save.setStyleSheet(self.button_dark_style)

    def apply_img_to_pdf_light_style(self):
        self.img2pdf_page.setStyleSheet("background-color: #e5e5e5")
        self.back_button.setStyleSheet(self.button_light_style)
        self.scroll_area.setStyleSheet(self.scroll_area_light_style)
        self.image_container.setStyleSheet("background-color: #a5a5a5")
        self.button_img_to_pdf_select.setStyleSheet(self.button_light_style)
        self.button_img_to_pdf_add.setStyleSheet(self.button_light_style)
        self.button_img_to_pdf_remove_all.setStyleSheet(self.button_light_style)
        self.button_img_to_pdf_save.setStyleSheet(self.button_light_style)
    
    # PDF combiner
    def apply_pdf_combiner_dark_style(self):
        self.pdf_combiner_page.setStyleSheet("background-color: #262626")
        self.back_button.setStyleSheet(self.button_dark_style)
        self.scroll_area.setStyleSheet(self.scroll_area_dark_style)
        self.pdf_container.setStyleSheet("background-color: #333333")
        self.button_pdf_combiner_select.setStyleSheet(self.button_dark_style)
        self.button_pdf_combiner_add.setStyleSheet(self.button_dark_style)
        self.button_pdf_combiner_remove_all.setStyleSheet(self.button_dark_style)
        self.button_pdf_combiner_save.setStyleSheet(self.button_dark_style)

    def apply_pdf_combiner_light_style(self):
        self.pdf_combiner_page.setStyleSheet("background-color: #e5e5e5")
        self.back_button.setStyleSheet(self.button_light_style)
        self.scroll_area.setStyleSheet(self.scroll_area_light_style)
        self.pdf_container.setStyleSheet("background-color: #a5a5a5")
        self.button_pdf_combiner_select.setStyleSheet(self.button_light_style)
        self.button_pdf_combiner_add.setStyleSheet(self.button_light_style)
        self.button_pdf_combiner_remove_all.setStyleSheet(self.button_light_style)
        self.button_pdf_combiner_save.setStyleSheet(self.button_light_style)

    # Image resizer
    def apply_image_resizer_page_dark_style(self):
        self.image_resizer_page.setStyleSheet("background-color: #262626")
        self.back_button.setStyleSheet(self.button_dark_style)
        self.width_input.setStyleSheet("background-color: #333333; padding: 3px 6px; border-radius: 3px")
        self.height_input.setStyleSheet("background-color: #333333; padding: 3px 6px; border-radius: 3px")
        self.save_resized_image_button.setStyleSheet(self.button_dark_style)
        self.select_image_button.setStyleSheet(self.button_dark_style)
        self.resized_image_scroll_area.setStyleSheet(self.scroll_area_dark_style)

    def apply_image_resizer_page_light_style(self):
        self.image_resizer_page.setStyleSheet("background-color: #e5e5e5")
        self.back_button.setStyleSheet(self.button_light_style)
        self.width_input.setStyleSheet("background-color: #a5a5a5")
        self.height_input.setStyleSheet("background-color: #a5a5a5")
        self.save_resized_image_button.setStyleSheet(self.button_light_style)
        self.select_image_button.setStyleSheet(self.button_light_style)
        self.resized_image_scroll_area.setStyleSheet(self.scroll_area_light_style)

    # Text from image
    def apply_text_from_image_dark_style(self):
        self.text_from_image_page.setStyleSheet("background-color: #262626")
        self.text_from_image_button.setStyleSheet(self.button_dark_style)
        self.back_button.setStyleSheet(self.button_dark_style)
        self.text_scroll_area.setStyleSheet(self.scroll_area_dark_style)
        self.textEdit.setStyleSheet("background-color: #212121")
        self.select_image_to_extract_button.setStyleSheet(self.button_dark_style)
        self.copy_button.setStyleSheet(self.button_dark_style)

    def apply_text_from_image_light_style(self):
        self.text_from_image_page.setStyleSheet("background-color: #e5e5e5")
        self.text_from_image_button.setStyleSheet(self.button_light_style)
        self.back_button.setStyleSheet(self.button_light_style)
        self.text_scroll_area.setStyleSheet(self.scroll_area_light_style)
        self.textEdit.setStyleSheet("background-color: #a5a5a5")
        self.select_image_to_extract_button.setStyleSheet(self.button_light_style)
        self.copy_button.setStyleSheet(self.button_light_style)

    def initUI(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # main page
        self.main_page = QWidget()
        self.setup_main_page()
        self.stack.addWidget(self.main_page)

        # img2pdf page
        self.img2pdf_page = QWidget()
        self.setup_img2pdf_page()
        self.stack.addWidget(self.img2pdf_page)

        # pdf combiner page
        self.pdf_combiner_page = QWidget()
        self.setup_pdf_combiner_page()
        self.stack.addWidget(self.pdf_combiner_page)

        # image resizer page
        self.image_resizer_page = QWidget()
        self.setup_image_resizer_page()
        self.stack.addWidget(self.image_resizer_page)

        # text from image page
        self.text_from_image_page = QWidget()
        self.setup_text_from_image_page()
        self.stack.addWidget(self.text_from_image_page)

        self.show_main_page()

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
        self.img2pdf_button.setFixedWidth(self.button_size)
        self.pdf_combiner_button.setFixedWidth(self.button_size)
        self.image_resizer_button.setFixedWidth(self.button_size)
        self.text_from_image_button.setFixedWidth(self.button_size)
        self.settings_button.setFixedWidth(self.button_size)
        self.about_button.setFixedWidth(self.button_size)
        self.close_app_button.setFixedWidth(self.button_size)

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

    def setup_img2pdf_page(self):
        layout = QVBoxLayout(self.img2pdf_page)

        self.back_button = QPushButton()
        if is_dark_theme():
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
        else:
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))

        self.back_button.setFixedSize(50, 25)
        self.back_button.clicked.connect(self.handle_back_button)

        layout.setAlignment(self.back_button, Qt.AlignLeft)
        layout.addWidget(self.back_button)
        
        # Creating scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Creating image container
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout()
        self.image_container.setLayout(self.image_layout)
        self.scroll_area.setWidget(self.image_container)

        # Creating buttons container 
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        layout.addWidget(buttons_container)

        # Select, Remove, Add button container
        three_buttons_container = QWidget()
        three_buttons_layout = QHBoxLayout(three_buttons_container)
        buttons_layout.addWidget(three_buttons_container)

        # Select button
        self.button_img_to_pdf_select = QPushButton("Select Images")
        three_buttons_layout.addWidget(self.button_img_to_pdf_select)
        three_buttons_layout.setAlignment(self.button_img_to_pdf_select, Qt.AlignCenter)

        # Add button
        self.button_img_to_pdf_add = QPushButton("Add Images")
        self.button_img_to_pdf_add.setEnabled(False)
        three_buttons_layout.addWidget(self.button_img_to_pdf_add)
        three_buttons_layout.setAlignment(self.button_img_to_pdf_add, Qt.AlignCenter)

        # Remove all button
        self.button_img_to_pdf_remove_all = QPushButton("Remove All")
        self.button_img_to_pdf_remove_all.setEnabled(False)
        three_buttons_layout.addWidget(self.button_img_to_pdf_remove_all)
        three_buttons_layout.setAlignment(self.button_img_to_pdf_remove_all, Qt.AlignCenter)

        # Save button
        self.button_img_to_pdf_save = QPushButton("Convert to PDF")
        self.button_img_to_pdf_save.setEnabled(False)
        buttons_layout.addWidget(self.button_img_to_pdf_save)
        buttons_layout.setAlignment(self.button_img_to_pdf_save, Qt.AlignRight)

        if is_dark_theme():
            self.apply_img_to_pdf_dark_style()
        else:
            self.apply_img_to_pdf_light_style()

        self.button_img_to_pdf_select.clicked.connect(self.selectImage)
        self.button_img_to_pdf_add.clicked.connect(self.add_images)
        self.button_img_to_pdf_remove_all.clicked.connect(self.remove_all_images)
        self.button_img_to_pdf_save.clicked.connect(self.save_img_pdf)

        self.image_files = []

    def setup_pdf_combiner_page(self):
        layout = QVBoxLayout(self.pdf_combiner_page)

        self.back_button = QPushButton()
        if is_dark_theme():
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
        else:
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))
        
        self.back_button.setFixedSize(50, 25)
        self.back_button.clicked.connect(self.handle_back_button)

        layout.setAlignment(self.back_button, Qt.AlignLeft)
        layout.addWidget(self.back_button)
        
        # Creating scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Creating pdf container
        self.pdf_container = QWidget()
        self.pdf_layout = QVBoxLayout()
        self.pdf_container.setLayout(self.pdf_layout)
        self.scroll_area.setWidget(self.pdf_container)

        # Creating buttons container 
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        layout.addWidget(buttons_container)

        # Select, Remove, Add button container
        three_buttons_container = QWidget()
        three_buttons_layout = QHBoxLayout(three_buttons_container)
        buttons_layout.addWidget(three_buttons_container)

        # Select button
        self.button_pdf_combiner_select = QPushButton("Select pdf")
        three_buttons_layout.addWidget(self.button_pdf_combiner_select)
        three_buttons_layout.setAlignment(self.button_pdf_combiner_select, Qt.AlignCenter)

        # Add button
        self.button_pdf_combiner_add = QPushButton("Add pdf")
        self.button_pdf_combiner_add.setEnabled(False)
        three_buttons_layout.addWidget(self.button_pdf_combiner_add)
        three_buttons_layout.setAlignment(self.button_pdf_combiner_add, Qt.AlignCenter)

        # Remove all button
        self.button_pdf_combiner_remove_all = QPushButton("Remove All")
        self.button_pdf_combiner_remove_all.setEnabled(False)
        three_buttons_layout.addWidget(self.button_pdf_combiner_remove_all)
        three_buttons_layout.setAlignment(self.button_pdf_combiner_remove_all, Qt.AlignCenter)

        # Save button
        self.button_pdf_combiner_save = QPushButton("Combine PDFs")
        self.button_pdf_combiner_save.setEnabled(False)
        buttons_layout.addWidget(self.button_pdf_combiner_save)
        buttons_layout.setAlignment(self.button_pdf_combiner_save, Qt.AlignRight)

        if is_dark_theme():
            self.apply_pdf_combiner_dark_style()
        else:
            self.apply_pdf_combiner_light_style()

        self.button_pdf_combiner_select.clicked.connect(self.open_pdf_dialog)
        self.button_pdf_combiner_add.clicked.connect(self.add_pdf)
        self.button_pdf_combiner_remove_all.clicked.connect(self.remove_all_pdfs)
        self.button_pdf_combiner_save.clicked.connect(self.save_pdf_combiner)

        self.pdf_files = []

    def setup_image_resizer_page(self):
        layout = QVBoxLayout()
        self.image_resizer_page.setLayout(layout)

        self.back_button = QPushButton()
        if is_dark_theme():
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
        else:
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))

        self.back_button.setFixedSize(50, 25)
        self.back_button.clicked.connect(self.handle_back_button)

        self.resized_image_scroll_area = QScrollArea(self)
        self.resized_image_scroll_area.setWidgetResizable(True)

        self.resized_images_widget = QWidget()
        self.resized_images_layout = QVBoxLayout(self.resized_images_widget)
        self.resized_image_scroll_area.setWidget(self.resized_images_widget)

        # Select image button
        self.select_image_button = QPushButton("Open Images")
        self.select_image_button.clicked.connect(self.selectImage)

        # Width input
        self.width_input = QLineEdit(self)
        self.width_input.setPlaceholderText("width")
        self.width_input.setMaximumWidth(200)
        self.width_input.setFont(QFont("Arial", 14))
        self.width_input.setValidator(QIntValidator())
        self.width_input.setEnabled(False)
        self.width_input.textChanged.connect(self.width_input_changed)

        # Height input
        self.height_input = QLineEdit(self)
        self.height_input.setPlaceholderText("height")
        self.height_input.setMaximumWidth(200)
        self.height_input.setFont(QFont("Arial", 14))
        self.height_input.setValidator(QIntValidator())
        self.height_input.setEnabled(False)
        self.height_input.textChanged.connect(self.height_input_changed)

        # Aspect ratio
        self.aspect_ratio_check = QCheckBox("Aspect ratio", self)
        self.aspect_ratio_check.setChecked(True)

        # Save button
        self.save_resized_image_button = QPushButton("Save")
        self.save_resized_image_button.clicked.connect(self.save_resized_image)

        # Layout for width and height inputs
        width_height_layout = QVBoxLayout()
        width_height_layout.addWidget(self.width_input)
        width_height_layout.addWidget(self.height_input)

        # Layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.select_image_button)
        button_layout.addWidget(self.save_resized_image_button)

        # Layout for width and height inputs and buttons layout
        width_height_buttons_layout = QHBoxLayout()
        width_height_buttons_layout.addLayout(width_height_layout)
        width_height_buttons_layout.addLayout(button_layout)

        # Add widgets to the main layout
        layout.addWidget(self.back_button)
        layout.addWidget(self.resized_image_scroll_area)
        layout.addLayout(width_height_buttons_layout)
        layout.addWidget(self.aspect_ratio_check)

        if is_dark_theme():
            self.apply_image_resizer_page_dark_style()
        else:
            self.apply_image_resizer_page_light_style()

    def setup_text_from_image_page(self):
        layout = QVBoxLayout()
        self.text_from_image_page.setLayout(layout)

        self.back_button = QPushButton()
        if is_dark_theme():
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
        else:
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))

        self.back_button.setFixedSize(50, 25)
        self.back_button.clicked.connect(self.handle_back_button)

        self.text_scroll_area = QScrollArea()
        self.text_scroll_area.setWidgetResizable(True)

        font = QFont("Arial", 12)
        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(font)
        self.text_scroll_area.setWidget(self.textEdit)
        self.textEdit.setReadOnly(True)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copyText)

        self.select_image_to_extract_button = QPushButton("Select image", self)
        self.select_image_to_extract_button.clicked.connect(self.selectImage)

        layout.addWidget(self.back_button)
        layout.addWidget(self.text_scroll_area)
        layout.addWidget(self.select_image_to_extract_button)
        layout.addWidget(self.copy_button)

        if is_dark_theme():
            self.apply_text_from_image_dark_style()
        else:
            self.apply_text_from_image_light_style()

    def show_main_page(self):
        self.stack.setCurrentWidget(self.main_page)

    def show_img2pdf_page(self):
        self.stack.setCurrentWidget(self.img2pdf_page)

    def show_pdf_combiner_page(self):
        self.stack.setCurrentWidget(self.pdf_combiner_page)

    def show_image_resizer_page(self):
        self.stack.setCurrentWidget(self.image_resizer_page)

    def show_text_from_image_page(self):
        self.stack.setCurrentWidget(self.text_from_image_page)

    def handle_back_button(self):
        self.stack.setCurrentWidget(self.main_page)

    def close_app(self):
        self.close()
        if self.settings_window:
            self.settings_window.close()
        if self.about_window:
            self.about_window.close()

    def open_pdf_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", settings.location, "PDF Files (*.pdf);;All Files (*)", options=options)
        if files:
            self.pdf_files = files
            self.display_selected_pdfs()
            self.button_pdf_combiner_save.setEnabled(True)
            self.button_pdf_combiner_remove_all.setEnabled(True)
            self.button_pdf_combiner_add.setEnabled(True)

    def display_selected_pdfs(self):    
        for i in reversed(range(self.pdf_layout.count())):
            widget_to_remove = self.pdf_layout.itemAt(i).widget()
            self.pdf_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for file in self.pdf_files:
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            if is_dark_theme():
                row_widget.setStyleSheet("background-color: #202020; border-radius: 4px")
            else:
                row_widget.setStyleSheet("background-color: #e5e5e5; border-radius: 4px")
            
            row_widget.setLayout(row_layout)
            row_widget.setFixedHeight(120)

            remove_button = QPushButton()
            if is_dark_theme():
                remove_button.setIcon(QIcon(f"{PATH_TO_FILE}x-dark.svg"))
            else:
                remove_button.setIcon(QIcon(f"{PATH_TO_FILE}x-light.svg"))

            remove_button.setFixedSize(30, 30)
            if is_dark_theme():
                remove_button.setStyleSheet(self.remove_button_dark_style)
            else:
                remove_button.setStyleSheet(self.remove_button_light_style)

            remove_button.clicked.connect(lambda _, f=file: self.remove_pdf(f))
            row_layout.addWidget(remove_button)

            label = QLabel()
            pixmap = QPixmap(file)
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            row_layout.addWidget(label)

            name_label = QLabel(file)
            name_label.setWordWrap(True)
            name_label.setFixedWidth(400)

            if settings.mode  == "dark":
                name_label.setStyleSheet("color: #a3a3a3")
            else:
                name_label.setStyleSheet("color: #000000")

            row_layout.addWidget(name_label)

            self.pdf_layout.addWidget(row_widget)
            self.pdf_layout.setAlignment(Qt.AlignTop)

    def add_pdf(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Add pdfs", settings.location, "PDF Files (*.pdf);;All Files (*)", options=options)
        if files:
            self.pdf_files.extend(files)
            self.display_selected_pdfs()


    def remove_all_pdfs(self):
        self.pdf_files = []
        self.display_selected_pdfs()
        self.button_pdf_combiner_add.setEnabled(False)
        self.button_pdf_combiner_remove_all.setEnabled(False)
        self.button_pdf_combiner_save.setEnabled(False)

    def save_pdf_combiner(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", settings.location, "PDF Files (*.pdf);;All Files (*)")
        if save_path:
            pdf_merger = PyPDF4.PdfFileMerger()
            for pdf in self.pdf_files:
                pdf_merger.append(pdf)
            with open(f"{save_path}.pdf", 'wb') as f:
                pdf_merger.write(f)

    def remove_pdf(self, file):
        self.pdf_files.remove(file)
        self.display_selected_pdfs()
        if not self.pdf_files:
            self.button_pdf_combiner_add.setEnabled(False)
            self.button_pdf_combiner_remove_all.setEnabled(False)
            self.button_pdf_combiner_save.setEnabled(False)

    def add_images(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Add Images", settings.location, "Images (*.png *.jpg *.jpeg *.jfif);;All Files (*)", options=options)
        if files:
            self.image_files.extend(files)
            self.display_selected_images(self.image_layout)

    def remove_all_images(self):
        self.image_files = []
        self.display_selected_images(self.image_layout)
        self.button_img_to_pdf_save.setEnabled(False)
        self.button_img_to_pdf_remove_all.setEnabled(False)
        self.button_img_to_pdf_add.setEnabled(False)

    def display_selected_images(self, layout):
        for i in reversed(range(layout.count())): 
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for file in self.image_files:
            row_widget = QWidget()
            row_layout = QHBoxLayout()

            if settings.mode  == "dark":
                row_widget.setStyleSheet("background-color: #202020; border-radius: 4px")
            else:
                row_widget.setStyleSheet("background-color: #f5f5f5; border-radius: 4px")
            
            row_widget.setLayout(row_layout)
            row_widget.setFixedHeight(120)

            remove_button = QPushButton()
            if is_dark_theme():
                remove_button.setIcon(QIcon(f"{PATH_TO_FILE}x-dark.svg"))
            else:
                remove_button.setIcon(QIcon(f"{PATH_TO_FILE}x-light.svg"))

            remove_button.setFixedSize(30, 30)
            if is_dark_theme():
                remove_button.setStyleSheet(self.remove_button_dark_style)
            else:
                remove_button.setStyleSheet(self.remove_button_light_style)

            remove_button.clicked.connect(lambda _, f=file: self.remove_image(layout, f))
            row_layout.addWidget(remove_button)

            label = QLabel()
            pixmap = QPixmap(file)
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            row_layout.addWidget(label)

            name_label = QLabel(file)
            name_label.setWordWrap(True)
            name_label.setFixedWidth(380)
            if is_dark_theme():
                name_label.setStyleSheet("color: #a3a3a3")
            else:
                name_label.setStyleSheet("color: #000000")
            
            row_layout.addWidget(name_label)

            layout.addWidget(row_widget)
            layout.setAlignment(Qt.AlignTop)

    def remove_image(self, layout, file):
        self.image_files.remove(file)
        self.display_selected_images(layout)
        if not self.image_files:
            self.button_img_to_pdf_save.setEnabled(False)
            self.button_img_to_pdf_remove_all.setEnabled(False)
            self.button_img_to_pdf_add.setEnabled(False)

    def save_img_pdf(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", settings.location, "PDF Files (*.pdf);;All Files (*)")
        if save_path:
            with open(f"{save_path}.pdf", 'wb') as f:
                f.write(img2pdf.convert(self.image_files))
                print(f"PDF saved to {save_path}")

    def show_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.show()

        if self.settings_window and self.settings_window.isVisible:
            self.settings_window.aboutWindowObject = self.about_window

    def show_settings_window(self):
        self.settings_window = SettingsWindow(self, self.about_window)
        self.settings_window.show()

    def selectImage(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif *.jfif)", options=options)
        if filenames:
            if self.stack.currentWidget() == self.text_from_image_page:
                self.extractText(filenames)
            elif self.stack.currentWidget() == self.img2pdf_page:
                self.image_files = filenames
                self.display_selected_images(self.image_layout)
                self.button_img_to_pdf_save.setEnabled(True)
                self.button_img_to_pdf_remove_all.setEnabled(True)
                self.button_img_to_pdf_add.setEnabled(True)
            else:
                self.resized_image_scroll_area.setVisible(True)
                self.image_files = filenames
                
                if self.stack.currentWidget == self.img2pdf_page:
                    self.display_selected_images(self.image_layout)
                else:
                    self.display_selected_images(self.resized_images_layout)
                
                    self.images = self.images_ref = [Image.open(image_filename) for image_filename in filenames]
                    self.original_aspect_ratio = self.images[0].width / self.images[0].height
                    self.width_input.setText(str(self.images[0].width))
                    self.width_input.setEnabled(True)
                    self.height_input.setText(str(self.images[0].height))
                    self.height_input.setEnabled(True)

                    self.updateImage()

    def updateImage(self, width=None, height=None):
        if self.images:
            first_image = self.images[0]
            width_input_text = self.width_input.text()
            height_input_text = self.height_input.text()

            new_width = width or (int(width_input_text) if width_input_text else first_image.width)
            new_height = height or (int(height_input_text) if height_input_text else first_image.height)
            keep_aspect_ratio = self.aspect_ratio_check.isChecked()

            if keep_aspect_ratio:
                if new_width / self.original_aspect_ratio > new_height:
                    new_width = int(new_height * self.original_aspect_ratio)
                else:
                    new_height = int(new_width / self.original_aspect_ratio)

            if new_width <= 1 or new_height <= 1:
                pass
            else:
                new_size = (int(new_width), int(new_height))
                resized_image = first_image.resize(new_size, Image.Resampling.LANCZOS)

                image_bytes = io.BytesIO()
                resized_image.save(image_bytes, format="PNG")
                image_bytes.seek(0)

                qimage = QImage()
                qimage.loadFromData(image_bytes.read())

                pixmap = QPixmap.fromImage(qimage)

                self.image_display_window.display_image(pixmap)
                self.image_display_window.show()

    def width_input_changed(self, text):
        if text == '':
            self.image = None
            return self.image
        else:
            self.image = self.images_ref
            if self.aspect_ratio_check.isChecked() and self.image:
                self.height_input.blockSignals(True)

                if self.images[0].width > self.images[0].height:
                    self.height_input.setText(str(round(int(text) / self.original_aspect_ratio)))
                else:
                    self.height_input.setText(str(round(int(text) * self.original_aspect_ratio)))

                self.height_input.blockSignals(False)
            self.updateImage(width=int(text))

    def height_input_changed(self, text):
        if text == '':
            self.image = None
            return self.image
        else:
            self.image = self.images_ref
            if self.aspect_ratio_check.isChecked() and self.image:
                self.width_input.blockSignals(True)

                if self.images[0].width > self.images[0].height:
                    self.width_input.setText(str(round(int(text) * self.original_aspect_ratio)))
                else:
                    self.width_input.setText(str(round(int(text) / self.original_aspect_ratio)))
                
                self.width_input.blockSignals(False)
            self.updateImage(height=int(text))

    def save_resized_image(self):
        if self.image:
            new_size = (int(self.width_input.text()), int(self.height_input.text()))
            resized_image = self.image.resize(new_size, Image.Resampling.LANCZOS)
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif);;All Files (*)")
            if save_path:
                resized_image.save(save_path)

    def extractText(self, filename):
        image = Image.open(filename)
        text = pytesseract.image_to_string(image)
        self.textEdit.setPlainText(text)

    def copyText(self):
        self.textEdit.selectAll()
        self.textEdit.copy()
        self.notification("Copied")

    def notification(self, message, message_type = "SUCCESS"):
        Toast.setPosition(ToastPosition.TOP_MIDDLE)
        Toast.setPositionRelativeToWidget(self)
        Toast.setOffset(30, 10)
        toast = Toast(self)
        toast.setDuration(2000)
        toast.setText(message)
        toast.setResetDurationOnHover(False)
        if message_type == "SUCCESS":
            if is_dark_theme():
                toast.applyPreset(ToastPreset.SUCCESS_DARK)
            else:
                toast.applyPreset(ToastPreset.SUCCESS)
        else:
            if is_dark_theme():
                toast.applyPreset(ToastPreset.ERROR_DARK)
            else:
                toast.applyPreset(ToastPreset.ERROR)
        toast.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
