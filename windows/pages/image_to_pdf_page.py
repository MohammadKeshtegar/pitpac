from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from utils.styles import button_dark_style, button_light_style, scroll_area_dark_style, scroll_area_light_style, remove_button_dark_style, remove_button_light_style
from utils.assets import is_dark_theme, settings, PATH_TO_FILE

import img2pdf

class Image2PDFPage(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
        self.setup_img2pdf_page()

    def setup_img2pdf_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.back_button = QPushButton()
        self.back_button_style()
        self.back_button.setFixedSize(50, 25)
        self.back_button.clicked.connect(self.handle_back_button)

        # Creating scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Creating image container
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout(self.image_container)
        self.image_container.setLayout(self.image_layout)
        self.scroll_area.setWidget(self.image_container)

        # Creating buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)

        # Select, Remove, Add button container
        three_buttons_container = QWidget()
        three_buttons_layout = QHBoxLayout(three_buttons_container)
        buttons_layout.addWidget(three_buttons_container)

        # Select button
        self.button_img_to_pdf_select = QPushButton("Select Images")

        # Add button
        self.button_img_to_pdf_add = QPushButton("Add Images")
        self.button_img_to_pdf_add.setEnabled(False)

        # Remove all button
        self.button_img_to_pdf_remove_all = QPushButton("Remove All")
        self.button_img_to_pdf_remove_all.setEnabled(False)

        # Save button
        self.button_img_to_pdf_save = QPushButton("Convert to PDF")
        self.button_img_to_pdf_save.setEnabled(False)

        if is_dark_theme():
            self.apply_img_to_pdf_dark_style()
        else:
            self.apply_img_to_pdf_light_style()

        self.button_img_to_pdf_select.clicked.connect(self.selectImage)
        self.button_img_to_pdf_add.clicked.connect(self.add_images)
        self.button_img_to_pdf_remove_all.clicked.connect(self.remove_all_images)
        self.button_img_to_pdf_save.clicked.connect(self.save_img_pdf)

        three_buttons_layout.addWidget(self.button_img_to_pdf_select, alignment=Qt.AlignmentFlag.AlignCenter)
        three_buttons_layout.addWidget(self.button_img_to_pdf_add, alignment=Qt.AlignmentFlag.AlignCenter)
        three_buttons_layout.addWidget(self.button_img_to_pdf_remove_all, alignment=Qt.AlignmentFlag.AlignCenter)

        buttons_layout.addWidget(self.button_img_to_pdf_save, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.scroll_area)
        layout.addWidget(buttons_container)

        self.image_files = []

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
                remove_button.setStyleSheet(remove_button_dark_style)
            else:
                remove_button.setStyleSheet(remove_button_light_style)

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

    def selectImage(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif *.jfif)", options=options)
        if filenames:
            self.image_files = filenames
            self.display_selected_images(self.image_layout)
            self.button_img_to_pdf_save.setEnabled(True)
            self.button_img_to_pdf_remove_all.setEnabled(True)
            self.button_img_to_pdf_add.setEnabled(True)

    def handle_back_button(self):
        self.mainWindowObject.show_main_page()

    def back_button_style(self):
        if is_dark_theme():
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
        else:
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))

    # Img to pdf styles
    def apply_img_to_pdf_dark_style(self):
        self.setStyleSheet("background-color: #262626; color: #e5e5e5")
        self.back_button.setStyleSheet(button_dark_style)
        self.scroll_area.setStyleSheet(scroll_area_dark_style)
        self.image_container.setStyleSheet("background-color: #333333")
        self.button_img_to_pdf_select.setStyleSheet(button_dark_style)
        self.button_img_to_pdf_add.setStyleSheet(button_dark_style)
        self.button_img_to_pdf_remove_all.setStyleSheet(button_dark_style)
        self.button_img_to_pdf_save.setStyleSheet(button_dark_style)

    def apply_img_to_pdf_light_style(self):
        self.setStyleSheet("background-color: #e5e5e5")
        self.back_button.setStyleSheet(button_light_style)
        self.scroll_area.setStyleSheet(scroll_area_light_style)
        self.image_container.setStyleSheet("background-color: #a5a5a5")
        self.button_img_to_pdf_select.setStyleSheet(button_light_style)
        self.button_img_to_pdf_add.setStyleSheet(button_light_style)
        self.button_img_to_pdf_remove_all.setStyleSheet(button_light_style)
        self.button_img_to_pdf_save.setStyleSheet(button_light_style)
