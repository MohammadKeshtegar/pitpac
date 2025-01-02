from PyQt5.QtWidgets import  QPushButton
from PyQt5.QtGui import QIcon

from utils.assets import is_dark_theme, PATH_TO_FILE
from utils.styles import button_dark_style, button_light_style


class BackButton(QPushButton):
    def __init__(self, mainWindowObject, text=None):
        super().__init__()
        self.mainWindowObject = mainWindowObject

        self.setText(text)
        self.redirect_button_style()
        self.setFixedSize(50, 25)
        self.clicked.connect(self.handle_redirect_button)

    def handle_redirect_button(self):
        self.mainWindowObject.show_main_page()

    def redirect_button_style(self):
        if is_dark_theme():
            self.redirect_button_dark_style()
        else:
             self.redirect_button_light_style()

    def redirect_button_dark_style(self):
            self.setStyleSheet(button_dark_style)
            self.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
    
    def redirect_button_light_style(self):
            self.setStyleSheet(button_light_style)
            self.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))