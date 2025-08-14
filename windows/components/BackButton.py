from PyQt5.QtWidgets import  QPushButton
from PyQt5.QtGui import QIcon

# from utils.styles import button_dark_style
from utils.assets import  PATH_TO_ICON_FILE

class BackButton(QPushButton):
    def __init__(self, mainWindowObject, text=None):
        super().__init__()
        self.mainWindowObject = mainWindowObject

        self.current_widget = None
        self.prev_widget = None

        self.setText(text)
        self.redirect_button_style()
        self.setFixedSize(50, 25)
        self.clicked.connect(self.handle_back)

    def handle_back(self):
        self.mainWindowObject.show_main_page()

    def redirect_button_style(self):
        self.setIcon(QIcon(f'{PATH_TO_ICON_FILE}arrow-left-dark.svg'))
        
