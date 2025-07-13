from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QSpinBox, QFontComboBox
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from qtwidgets import Toggle

from utils.assets import save_theme_preference, settings, START_LOCATION
# from utils.styles import button_dark_style, settings_option_dark_style

import sys
import os

class SettingsWindow(QWidget):
    def __init__(self, mainWindowObject, aboutWindowObject):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 400)
        self.mainWindowObject = mainWindowObject
        self.aboutWindowObject = aboutWindowObject
        self.new_font_family = None
        self.new_font_size = None
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.settings_options_widget = QWidget()
        settings_options_layout = QVBoxLayout()
        settings_options_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_options_widget.setLayout(settings_options_layout)

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

        # Font family
        self.font_family_widget = QWidget()
        font_family_layout = QHBoxLayout()
        self.font_family_widget.setLayout(font_family_layout)

        self.font_label = QLabel("Select Font", self)
        self.font_combo = QFontComboBox(self)
        self.font_combo.setCurrentText(settings.font_family)

        self.current_font_family = self.font_combo.currentText()
        
        font_db = QFontDatabase()
        for family in font_db.families():
            self.font_combo.addItem(family)
 
        self.font_combo.currentFontChanged.connect(self.set_font_family)
        
        font_family_layout.addWidget(self.font_label, alignment=Qt.AlignLeft)
        font_family_layout.addWidget(self.font_combo, alignment=Qt.AlignRight)

        # Font size
        self.font_size_widget = QWidget()
        font_size_layout = QHBoxLayout()
        self.font_size_widget.setLayout(font_size_layout)

        self.font_size_label = QLabel("Font Size", self)
        self.font_size_spin = QSpinBox(self)
        self.font_size_spin.setRange(6, 72)
        self.font_size_spin.setValue(settings.font_size) 
        self.font_size_spin.setFixedWidth(60)
        self.font_size_spin.valueChanged.connect(self.set_font_size)

        self.current_font_size = self.font_size_spin.value()

        font_size_layout.addWidget(self.font_size_label, alignment=Qt.AlignLeft)
        font_size_layout.addWidget(self.font_size_spin, alignment=Qt.AlignRight)        

        # Show image preview
        self.image_preview = QWidget()
        image_preview_layout = QHBoxLayout()
        self.image_preview.setLayout(image_preview_layout)

        self.image_preview_label = QLabel("Show image preview", self)

        self.image_preview_toggle = Toggle()
        self.image_preview_toggle.setChecked(settings.show_image_preview)
        self.image_preview_toggle.stateChanged.connect(self.toggle_show_image_preview)

        image_preview_layout.addWidget(self.image_preview_label, alignment=Qt.AlignmentFlag.AlignLeft)
        image_preview_layout.addWidget(self.image_preview_toggle, alignment=Qt.AlignmentFlag.AlignRight)

        # Ok and Reset button
        self.ok_reset_widget = QWidget()
        ok_reset_layout = QHBoxLayout()
        self.ok_reset_widget.setLayout(ok_reset_layout)

        self.ok_button = QPushButton("Ok")
        self.ok_button.setFixedWidth(100)
        self.ok_button.clicked.connect(self.ok_click)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(100)
        self.reset_button.clicked.connect(self.reset_click)

        # settings_options_layout.addWidget(self.toggle_mode_widget)
        settings_options_layout.addWidget(self.image_preview)
        settings_options_layout.addWidget(self.location_widget)
        settings_options_layout.addWidget(self.font_family_widget)
        settings_options_layout.addWidget(self.font_size_widget)

        ok_reset_layout.addWidget(self.reset_button, alignment=Qt.AlignmentFlag.AlignLeft)
        ok_reset_layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.settings_options_widget, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.ok_reset_widget, alignment=Qt.AlignmentFlag.AlignBottom)

        if not self.layout():
            self.setLayout(layout)
        self.update_style()

    def toggle_show_image_preview(self, state):
        settings.show_image_preview = True if state == 2 else False
        print(settings.show_image_preview)
        save_theme_preference()

    def set_font_family(self, font):
        settings.font_family = font.family()
        save_theme_preference()
        self.new_font_family = font.family()

    def set_font_size(self, size):
        settings.font_size = size
        save_theme_preference()
        self.new_font_size = size

    def ok_click(self):
        condition_1 = self.new_font_family is not None and self.current_font_family != self.new_font_size
        condition_2 = self.new_font_size is not None and self.current_font_size != self.new_font_size

        if condition_1 or condition_2:
            self.reload_main_window()
        self.close()

    def reset_click(self):
        settings.mode = "dark"
        settings.location = START_LOCATION
        settings.font_family = "Noto Sans"
        settings.font_size = 10
        settings.show_image_preview = True
        save_theme_preference()
        self.reload_main_window()

    def browse_location(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog 
        file_path = QFileDialog.getExistingDirectory(self, "Select Directory", settings.location, options=options)
        if file_path: 
            self.location_field.setText(file_path)
            settings.location = file_path
            save_theme_preference()
    
    def update_style(self):
        # self.settings_dark_style()
        pass

    def switch_mode(self, state):
        settings.mode = "dark" if state == 2 else "light"

        # self.settings_dark_style()
        save_theme_preference()

        self.update_style()
        self.mainWindowObject.initUI()

    def reload_main_window(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    # def settings_dark_style(self):
    #     self.setStyleSheet("background-color: #1e1e1e")
    #     self.location_widget.setStyleSheet(settings_option_dark_style)
    #     self.location_field.setStyleSheet("border: none; background-color: #3e3e3e; border-radius: 3px; padding: 3px 6px; color: #d4d4d4")
    #     self.browse_location_button.setStyleSheet(button_dark_style)
    #     self.font_family_widget.setStyleSheet(settings_option_dark_style)
    #     self.font_size_widget.setStyleSheet(settings_option_dark_style)
    #     self.font_combo.setStyleSheet("background-color: #3e3e3e")
    #     self.font_size_spin.setStyleSheet("background-color: #3e3e3e")
    #     self.image_preview.setStyleSheet(settings_option_dark_style)
    #     self.reset_button.setStyleSheet(button_dark_style)
    #     self.ok_button.setStyleSheet(button_dark_style)
