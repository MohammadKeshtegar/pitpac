import os
import io
import sys
import PyPDF4
import img2pdf
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QScrollArea, QHBoxLayout, QStackedWidget, QLineEdit, QCheckBox, QTextEdit, QComboBox
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage, QIntValidator
from PyQt5.QtCore import Qt, QSettings
from qtwidgets import Toggle
from pyqttoast import Toast, ToastPreset, ToastPosition
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

PATH_TO_FILE = os.getenv("PATH_TO_FILE")
START_LOCATION = os.getenv("START_LOCATION")

def load_theme_prefernence():
    app_settings = QSettings("Pitpac", "pitpac")
    mode = app_settings.value("mode", "dark")
    location = app_settings.value("location", START_LOCATION)
    return mode, location

def is_dark_theme():
    return settings.mode == "dark"

def save_theme_preference():
    app_settings = QSettings("Pitpac", "pitpac")
    app_settings.setValue("mode", settings.mode)
    app_settings.setValue("location", settings.location)

class Settings:
    def __init__(self):
        self.mode, self.location = load_theme_prefernence()

settings = Settings()

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About Pitpac")
        self.setGeometry(800, 300, 600, 300)

        self.about_text = """
            <p style='font-size:16px'>Pitpac is a desktop application allows you to convert images to pdf files or cobine pdf files into one pdf file.</p>
            <p style='font-size:14px; line-height:1.2'>
                Application version: 1.0.0<br>
                owner: Mohammad Keshtegar<br>
                If your faced any issues, feel free to ask me at:
                <a style='font-size:14px' href='https://t.me/MohammadKeshtegar1401'>@MohammadKeshtegar1401</a>
                Also you can find the source code <a href='https://github.com/MohammadKeshtegar/pitpac' >here<a/>
            </p>
        """

        layout = QHBoxLayout()
        label = QLabel(self.about_text, self)

        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        label.setFixedWidth(500)

        layout.addStretch(1)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        if is_dark_theme():
            self.apply_about_dark_style()
        else:
            self.apply_about_light_style()

        self.setLayout(layout)

    def apply_about_dark_style(self):
        self.setStyleSheet("background-color: #222222")

    def apply_about_light_style(self):
        self.setStyleSheet("background-color: #f5f5f5; color: #222222")

class SettingsWindow(QWidget):
    def __init__(self, mainWindowObject, aboutWindowObject):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 400)
        self.mainWindowObject = mainWindowObject
        self.aboutWindowObject = aboutWindowObject
        
        self.initUI()

    def initUI(self):        
        # Toggle button
        layout = QVBoxLayout()

        self.settings_options_widget = QWidget()
        settings_options_layout = QVBoxLayout()
        settings_options_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_options_widget.setLayout(settings_options_layout)

        # Toggle
        self.toggle_widget = QWidget()
        toggle_layout = QHBoxLayout()
        self.toggle_widget.setLayout(toggle_layout)

        self.toggle_label = QLabel("Toggle Mode", self)
        self.toggle = Toggle()

        self.toggle.setChecked(True if is_dark_theme() else False)
        self.toggle.stateChanged.connect(self.switch_mode)

        toggle_layout.addWidget(self.toggle_label, alignment=Qt.AlignLeft)
        toggle_layout.addWidget(self.toggle, alignment=Qt.AlignRight)

        # Location
        self.location_widget = QWidget()
        location_layout = QHBoxLayout()
        self.location_widget.setLayout(location_layout)

        self.location_field = QLineEdit(settings.location, self)
        self.location_field.setMinimumWidth(200)
        self.location_field.setMaximumWidth(400)
        self.location_field.setFont(QFont("Arial", 12))

        self.browse_location_button = QPushButton("Browse", self)
        self.browse_location_button.clicked.connect(self.browse_location)

        location_layout.addWidget(self.location_field, alignment=Qt.AlignmentFlag.AlignLeft)
        location_layout.addWidget(self.browse_location_button, alignment=Qt.AlignmentFlag.AlignRight)

        settings_options_layout.addWidget(self.toggle_widget)
        settings_options_layout.addWidget(self.location_widget)

        # Ok button
        self.ok_widget = QWidget()
        ok_layout = QHBoxLayout()
        self.ok_widget.setLayout(ok_layout)

        self.ok_button = QPushButton("Ok")
        self.ok_button.setFixedWidth(100)
        self.ok_button.clicked.connect(self.ok_click)

        ok_layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.settings_options_widget, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.ok_widget, alignment=Qt.AlignmentFlag.AlignBottom)
        
        if not self.layout():
            self.setLayout(layout)
        self.update_style()

    def ok_click(self):
        self.close()

    def browse_location(self):
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog 
        file_path = QFileDialog.getExistingDirectory(self, "Select Directory", settings.location, options=options) 
        if file_path: 
            self.location_field.setText(file_path)
            settings.location = file_path
            save_theme_preference()
    
    def update_style(self):
        if is_dark_theme():
            self.settings_dark_style()
        else:
            self.settings_light_style()

    def settings_dark_style(self):
        self.setStyleSheet("background-color: #1e1e1e")
        self.toggle_widget.setStyleSheet("background-color: #262626")
        self.location_widget.setStyleSheet("background-color: #262626")
        self.location_field.setStyleSheet("border: none; background-color: #3e3e3e; border-radius: 3px; padding: 3px 6px; color: #d4d4d4")
        self.ok_button.setStyleSheet(self.mainWindowObject.button_dark_style)
        self.browse_location_button.setStyleSheet(self.mainWindowObject.button_dark_style)

    def settings_light_style(self):
        self.setStyleSheet("background-color: #f5f5f5")
        self.toggle_widget.setStyleSheet("background-color: #d4d4d4; color: #222222")
        self.location_widget.setStyleSheet("background-color: #d4d4d4; color: #222222")
        self.location_field.setStyleSheet("border: none; background-color: #e5e5e5; border-radius: 3px; padding: 3px 6px; color: #111111")
        self.ok_button.setStyleSheet(self.mainWindowObject.button_light_style)
        self.browse_location_button.setStyleSheet(self.mainWindowObject.button_light_style)

    def switch_mode(self, state):
        settings.mode = "dark" if state == 2 else "light"
        
        if is_dark_theme():
            if self.aboutWindowObject:
                self.aboutWindowObject.apply_about_dark_style()
            self.mainWindowObject.apply_main_dark_style()
            self.settings_dark_style()
            save_theme_preference()
        else:
            if self.aboutWindowObject:
                self.aboutWindowObject.apply_about_light_style()
            self.mainWindowObject.apply_main_light_style()
            self.settings_light_style()
            save_theme_preference()

        self.update_style()
        self.mainWindowObject.initUI()

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
            QScrollBar { background-color: #262626; border: 1px solid #111111 }
            QScrollBar::handle { margin: 16px 0; border-radius: 2px; border: 1px solid #404040; background-color: #404040 }
            QScrollBar::handle:pressed { background-color: #333333 }
            QScrollArea { background-color: #525252 }
        """

        self.scroll_area_light_style = """
            QScrollBar { background-color: #868686; border: 1px solid #111111 }
            QScrollBar::handle { margin: 16px 0; border-radius: 2px; border: 1px solid #404040; background-color: #a7a7a7 }
            QScrollBar::handle:pressed { background-color: #333333 }
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

    def apply_image_resizer_page_dark_style(self):
        self.image_resizer_page.setStyleSheet("background-color: #262626")
        self.back_button.setStyleSheet(self.button_dark_style)
        self.image_label.setStyleSheet("background-color: #333333")
        self.width_input.setStyleSheet("background-color: #333333; padding: 3px 6px; border-radius: 3px")
        self.height_input.setStyleSheet("background-color: #333333; padding: 3px 6px; border-radius: 3px")
        self.save_resized_image_button.setStyleSheet(self.button_dark_style)
        self.select_image_button.setStyleSheet(self.button_dark_style)

    def apply_image_resizer_page_light_style(self):
        self.image_resizer_page.setStyleSheet("background-color: #e5e5e5")
        self.back_button.setStyleSheet(self.button_light_style)
        self.image_label.setStyleSheet("background-color: #a5a5a5")
        self.width_input.setStyleSheet("background-color: #a5a5a5")
        self.height_input.setStyleSheet("background-color: #a5a5a5")
        self.save_resized_image_button.setStyleSheet(self.button_light_style)
        self.select_image_button.setStyleSheet(self.button_light_style)

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
        self.close_app_button = QPushButton("Close App")

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

        self.button_img_to_pdf_select.clicked.connect(self.open_image_dialog)
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

        self.image_label = QLabel()
        self.image_label.setStyleSheet("border: 1px solid #111111")

        # Select image button
        self.select_image_button = QPushButton("Open Image")
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
        layout.addWidget(self.image_label)
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

    def open_image_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", settings.location, "Images (*.png *.jpg *.jpeg *.jfif);;All Files (*)", options=options)
        if files:
            self.image_files = files
            self.display_selected_images()
            self.button_img_to_pdf_save.setEnabled(True)
            self.button_img_to_pdf_remove_all.setEnabled(True)
            self.button_img_to_pdf_add.setEnabled(True)

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
            self.display_selected_images()

    def remove_all_images(self):
        self.image_files = []
        self.display_selected_images()
        self.button_img_to_pdf_save.setEnabled(False)
        self.button_img_to_pdf_remove_all.setEnabled(False)
        self.button_img_to_pdf_add.setEnabled(False)

    def display_selected_images(self):
        for i in reversed(range(self.image_layout.count())): 
            widget_to_remove = self.image_layout.itemAt(i).widget()
            self.image_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for file in self.image_files:
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            if settings.mode  == "dark":
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

            remove_button.clicked.connect(lambda _, f=file: self.remove_image(f))
            row_layout.addWidget(remove_button)

            label = QLabel()
            pixmap = QPixmap(file)
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            row_layout.addWidget(label)

            name_label = QLabel(file)
            name_label.setWordWrap(True)
            name_label.setFixedWidth(400)
            if is_dark_theme():
                name_label.setStyleSheet("color: #a3a3a3")
            else:
                name_label.setStyleSheet("color: #000000")
            
            row_layout.addWidget(name_label)

            self.image_layout.addWidget(row_widget)
            self.image_layout.setAlignment(Qt.AlignTop)

    def remove_image(self, file):
        self.image_files.remove(file)
        self.display_selected_images()
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
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif)", options=options)
        if filename:
            if self.stack.currentWidget() == self.text_from_image_page:
                self.extractText(filename)
            else:
                self.image = self.image_ref = Image.open(filename)
                self.width_input.setText(str(self.image.width))
                self.width_input.setEnabled(True)
                self.height_input.setText(str(self.image.height))
                self.height_input.setEnabled(True)
                self.updateImage()

    def updateImage(self, width = None, height = None):
        if self.image:
            width_input_text = self.width_input.text()
            height_input_text = self.height_input.text()

            new_width = width or (int(width_input_text) if width_input_text else self.image.width)
            new_height = height or (int(height_input_text) if height_input_text else self.image.height)
            keep_aspect_ratio = self.aspect_ratio_check.isChecked()

            if keep_aspect_ratio:
                original_aspect_ratio = self.image.width / self.image.height
                if new_width / original_aspect_ratio > new_height:
                    new_width = int(new_height * original_aspect_ratio)
                else:
                    new_height = int(new_width * original_aspect_ratio)

            new_size = (int(new_width), int(new_height))
            resized_image = self.image.resize(new_size, Image.Resampling.LANCZOS)


            image_bytes = io.BytesIO()
            resized_image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            qimage = QImage()
            qimage.loadFromData(image_bytes.read())

            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()

    def width_input_changed(self, text):
        if text == '':
            self.image = None
            return self.image
        else:
            self.image = self.image_ref
            self.updateImage(width=int(text))
            if self.aspect_ratio_check.isChecked():
                self.height_input.setText(text)

    def height_input_changed(self, text):
        if text == '':
            self.image = None
            return self.image
        else:
            self.image = self.image_ref
            self.updateImage(height=int(text))
            if self.aspect_ratio_check.isChecked():
                self.width_input.setText(text)

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
