from PyQt5.QtWidgets import QScrollArea, QLabel, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtCore import Qt

class ImageDisplayWindow(QMainWindow): 
    def __init__(self, parent=None): 
        super().__init__(parent) 

        self.setWindowTitle("Resized Image") 
        self.setGeometry(600, 250, 600, 600)
        self.setMaximumWidth(1400)
        self.setMaximumHeight(900)

        self.resized_image_scroll_area = QScrollArea(self)
        self.resized_image_scroll_area.setWidgetResizable(True)

        self.image_label = QLabel(self) 
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.image_label.setStyleSheet("border: 1px solid #111111") 

        self.resized_image_scroll_area.setWidget(self.image_label)

        layout = QVBoxLayout()
        layout.addWidget(self.resized_image_scroll_area)

        container = QWidget() 
        container.setLayout(layout) 
        self.setCentralWidget(container) 

    def display_image(self, pixmap): 
        self.image_label.setPixmap(pixmap) 
        self.image_label.adjustSize()