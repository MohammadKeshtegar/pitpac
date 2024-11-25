from PyQt5.QtWidgets import QScrollArea, QLabel, QVBoxLayout, QWidget, QMainWindow, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from utils.assets import is_dark_theme, PATH_TO_FILE
from utils.styles import button_dark_style, button_light_style, scroll_area_dark_style, scroll_area_light_style

class ImageDisplayWindow(QMainWindow): 
    def __init__(self, parent=None): 
        super().__init__(parent) 

        self.setWindowTitle("Resized Image") 
        self.setGeometry(1200, 250, 600, 600)
        self.setMaximumWidth(1400)
        self.setMaximumHeight(900)

        self.zoom_level = 1.0 
        
        self.zoom_widget = QWidget() 
        self.zoom_widget.setFixedWidth(120)
        self.zoom_layout = QHBoxLayout(self.zoom_widget) 

        self.zoom_in_button = QPushButton()
        self.zoom_out_button = QPushButton()

        self.zoom_in_button.setFixedWidth(40)
        self.zoom_out_button.setFixedWidth(40)

        self.apply_icon_theme()

        self.zoom_in_button.clicked.connect(self.zoom_in) 
        self.zoom_out_button.clicked.connect(self.zoom_out) 
        
        self.zoom_level_label = QLabel("100%")
        self.zoom_level_label.setFixedWidth(40)
        self.zoom_level_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        
        self.zoom_layout.addWidget(self.zoom_out_button) 
        self.zoom_layout.addWidget(self.zoom_level_label) 
        self.zoom_layout.addWidget(self.zoom_in_button)

        self.resized_image_scroll_area = QScrollArea(self)
        self.resized_image_scroll_area.setWidgetResizable(True)
        print(self.resized_image_scroll_area.styleSheet())

        self.image_label = QLabel(self)

        self.resized_image_scroll_area.setWidget(self.image_label)

        layout = QVBoxLayout()
        layout.addWidget(self.zoom_widget)
        layout.addWidget(self.resized_image_scroll_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        if is_dark_theme():
            self.apply_image_preview_dark_style()
        else:
            self.apply_image_preview_light_style()

    def apply_icon_theme(self):
        if is_dark_theme():
            self.zoom_in_button.setIcon(QIcon(f"{PATH_TO_FILE}plus-bold-dark.svg"))
            self.zoom_out_button.setIcon(QIcon(f"{PATH_TO_FILE}minus-bold-dark.svg"))
        else:
            self.zoom_in_button.setIcon(QIcon(f"{PATH_TO_FILE}plus-bold-light.svg"))
            self.zoom_out_button.setIcon(QIcon(f"{PATH_TO_FILE}minus-bold-light.svg"))

    def zoom_out(self):
        self.zoom_level = max(0.1, self.zoom_level - 0.1)
        self.update_image_label()

    def zoom_in(self):
        self.zoom_level += 0.1
        self.update_image_label()

    def update_image_label(self):
        if self.original_pixmap:
            scaled_pixmap = self.original_pixmap.scaled(self.original_pixmap.size() * self.zoom_level, Qt.KeepAspectRatio) 
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.adjustSize()
            self.zoom_level_label.setText(f"{int(self.zoom_level * 100)}%")

    def display_image(self, pixmap): 
        self.original_pixmap = pixmap 
        self.update_image_label()

    def apply_image_preview_dark_style(self):
        self.setStyleSheet("background-color: #262626")
        self.zoom_in_button.setStyleSheet(button_dark_style)
        self.zoom_out_button.setStyleSheet(button_dark_style)
        self.zoom_level_label.setStyleSheet("background-color: #525252")
        self.resized_image_scroll_area.setStyleSheet(scroll_area_dark_style)
        # self.image_label.setStyleSheet(scroll_area_dark_style)

    def apply_image_preview_light_style(self):
        self.setStyleSheet("background-color: #e5e5e5")
        self.zoom_in_button.setStyleSheet(button_light_style)
        self.zoom_out_button.setStyleSheet(button_light_style)
        self.zoom_level_label.setStyleSheet("background-color: #e5e5e5")
        # self.resized_image_scroll_area.setStyleSheet(scroll_area_light_style)
