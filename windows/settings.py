from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QSpinBox, QFontComboBox
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from qtwidgets import Toggle

from assets import save_theme_preference, settings, is_dark_theme
from styles import button_dark_style, button_light_style

# from main_page import apply_main_light_style, apply_main_dark_style

class SettingsWindow(QWidget):
    def __init__(self, mainWindowObject, aboutWindowObject):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 400)
        self.mainWindowObject = mainWindowObject
        self.aboutWindowObject = aboutWindowObject
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.settings_options_widget = QWidget()
        settings_options_layout = QVBoxLayout()
        settings_options_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_options_widget.setLayout(settings_options_layout)

        # Toggle
        self.toggle_widget = QWidget()
        toggle_layout = QHBoxLayout()
        self.toggle_widget.setLayout(toggle_layout)

        self.toggle_label = QLabel(f"{settings.mode.title()} Mode", self)
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

        # Font family
        self.font_family_widget = QWidget()
        font_family_layout = QHBoxLayout()
        self.font_family_widget.setLayout(font_family_layout)

        self.font_label = QLabel("Select Font", self)
        self.font_combo = QFontComboBox(self)

        font_db = QFontDatabase()
        for family in font_db.families():
            self.font_combo.addItem(family)
 
        self.font_combo.currentFontChanged.connect(self.set_font)
        
        font_family_layout.addWidget(self.font_label, alignment=Qt.AlignLeft)
        font_family_layout.addWidget(self.font_combo, alignment=Qt.AlignRight)

        settings_options_layout.addWidget(self.font_family_widget)

        # Font size
        self.font_size_widget = QWidget()
        font_size_layout = QHBoxLayout()
        self.font_size_widget.setLayout(font_size_layout)

        self.font_size_label = QLabel("Font Size", self)
        self.font_size_spin = QSpinBox(self)
        self.font_size_spin.setRange(6, 72) # Example range 
        self.font_size_spin.setValue(12) # Default value 
        self.font_size_spin.setFixedWidth(60)
        self.font_size_spin.valueChanged.connect(self.set_font_size)

        font_size_layout.addWidget(self.font_size_label, alignment=Qt.AlignLeft)
        font_size_layout.addWidget(self.font_size_spin, alignment=Qt.AlignRight)
        
        settings_options_layout.addWidget(self.font_size_widget)

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

    def set_font(self, font):
        self.selected_font = font.family()

    def set_font_size(self, size):
        self.selected_font_size = size

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
        self.toggle_label.setText("Dark Mode")
        self.location_widget.setStyleSheet("background-color: #262626")
        self.location_field.setStyleSheet("border: none; background-color: #3e3e3e; border-radius: 3px; padding: 3px 6px; color: #d4d4d4")
        self.browse_location_button.setStyleSheet(button_dark_style)
        self.font_family_widget.setStyleSheet("background-color: #262626")
        self.font_size_widget.setStyleSheet("background-color: #262626")
        self.font_combo.setStyleSheet("background-color: #3e3e3e")
        self.font_size_spin.setStyleSheet("background-color: #3e3e3e")
        self.ok_button.setStyleSheet(button_dark_style)

    def settings_light_style(self):
        self.setStyleSheet("background-color: #f5f5f5")
        self.toggle_widget.setStyleSheet("background-color: #d4d4d4; color: #222222")
        self.toggle_label.setText("Light Mode")
        self.location_widget.setStyleSheet("background-color: #d4d4d4; color: #222222")
        self.location_field.setStyleSheet("border: none; background-color: #e5e5e5; border-radius: 3px; padding: 3px 6px; color: #111111")
        self.browse_location_button.setStyleSheet(button_light_style)
        self.font_family_widget.setStyleSheet("background-color: #d4d4d4; color: #111111")
        self.font_size_widget.setStyleSheet("background-color: #d4d4d4; color: #111111")
        self.font_combo.setStyleSheet("background-color: #e5e5e5")
        self.font_size_spin.setStyleSheet("background-color: #e5e5e5")
        self.ok_button.setStyleSheet(button_light_style)

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
