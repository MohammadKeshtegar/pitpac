from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtGui import QIcon

from utils.assets import is_dark_theme, PATH_TO_FILE
from utils.styles import button_dark_style, button_light_style

class Page(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
        self.setStyleSheet("background-color: #262626")

    def redirect_button(self):
        self.redirect_button = QPushButton()
        self.redirect_button_style()
        self.redirect_button.setFixedSize(50, 25)
        self.redirect_button.clicked.connect(self.handle_redirect_button)

    def handle_redirect_button(self):
        self.mainWindowObject.show_main_page()

    def redirect_button_style(self):
        if is_dark_theme():
            self.redirect_button_dark_style()
        else:
             self.redirect_button_light_style()

    def redirect_button_dark_style(self):
            self.redirect_button.setStyleSheet(button_dark_style)
            self.redirect_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
    
    def redirect_button_light_style(self):
            self.redirect_button.setStyleSheet(button_light_style)
            self.redirect_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))