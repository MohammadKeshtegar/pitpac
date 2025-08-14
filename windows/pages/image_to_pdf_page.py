from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from components.BackButton import BackButton

from utils.assets import settings, PATH_TO_ICON_FILE
from utils.notification import notification

import img2pdf
import os

class Image2PDFPage(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
        self.setObjectName("Image2PDF")
        self.setup_img2pdf_page()

    def setup_img2pdf_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Redirect button
        self.back_button = BackButton(mainWindowObject=self.mainWindowObject)

        # Creating scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setProperty("class", "scroll-area-dark")

        # Creating image container
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout(self.image_container)
        self.image_container.setLayout(self.image_layout)
        self.image_container.setProperty("class", "image-container-dark")

        self.scroll_area.setWidget(self.image_container)

        # Creating buttons container
        self.buttons_container = QWidget()
        buttons_layout = QHBoxLayout(self.buttons_container)

        # Select, Remove, Add button container
        self.three_buttons_container = QWidget()
        three_buttons_layout = QHBoxLayout(self.three_buttons_container)
        buttons_layout.addWidget(self.three_buttons_container)

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

        self.button_img_to_pdf_select.setProperty("class", "button-dark")
        self.button_img_to_pdf_add.setProperty("class", "button-dark")
        self.button_img_to_pdf_remove_all.setProperty("class", "button-dark")
        self.button_img_to_pdf_save.setProperty("class", "button-dark")

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
        layout.addWidget(self.buttons_container)

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

            row_widget.setLayout(row_layout)
            row_widget.setFixedHeight(120)
            row_widget.setStyleSheet("background-color: #202020; border-radius: 4px")

            label = QLabel()
            pixmap = QPixmap(file)
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

            name_label = QLabel(os.path.basename(file))
            name_label.setWordWrap(True)
            name_label.setFixedWidth(380)
            name_label.setStyleSheet("color: #a3a3a3")

            remove_button = QPushButton()
            remove_button.setFixedSize(30, 30)
            remove_button.clicked.connect(lambda _, f=file: self.remove_image(layout, f))
            remove_button.setIcon(QIcon(f"{PATH_TO_ICON_FILE}x-dark.svg"))
            remove_button.setProperty("class", "remove-button-dark")

            row_layout.addWidget(label)
            row_layout.addWidget(name_label)
            row_layout.addWidget(remove_button)

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
                notification(self, message="PDF saved Successfully!")
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

