from PyQt5.QtWidgets import QMainWindow, QPushButton, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QFileDialog, QLabel
from PyQt5.QtGui import QFont, QIntValidator, QIcon, QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

from image_preview import ImageDisplayWindow

from styles import button_dark_style, button_light_style, scroll_area_dark_style, scroll_area_light_style, remove_button_dark_style, remove_button_light_style
from assets import is_dark_theme, PATH_TO_FILE, settings

import io

class ImageResizerPage(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
        self.image_display_window = ImageDisplayWindow()
        self.setup_image_resizer_page()

    def setup_image_resizer_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.back_button = QPushButton()
        self.back_button_style()

        self.back_button.setFixedSize(50, 25)
        self.back_button.clicked.connect(self.handle_back_button)

        self.resized_image_scroll_area = QScrollArea(self)
        self.resized_image_scroll_area.setWidgetResizable(True)

        self.resized_images_widget = QWidget()
        self.resized_images_layout = QVBoxLayout(self.resized_images_widget)
        self.resized_image_scroll_area.setWidget(self.resized_images_widget)

        # Select image button
        self.select_image_button = QPushButton("Open Images")
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
        layout.addWidget(self.resized_image_scroll_area)
        layout.addLayout(width_height_buttons_layout)
        layout.addWidget(self.aspect_ratio_check)

        if is_dark_theme():
            self.apply_image_resizer_page_dark_style()
        else:
            self.apply_image_resizer_page_light_style()

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

    def selectImage(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif *.jfif)", options=options)
        if filenames:
            self.resized_image_scroll_area.setVisible(True)
            self.image_files = filenames
            self.display_selected_images(self.resized_images_layout)
        
            self.images = self.images_ref = [Image.open(image_filename) for image_filename in filenames]
            self.original_aspect_ratio = self.images[0].width / self.images[0].height
            self.width_input.setText(str(self.images[0].width))
            self.width_input.setEnabled(True)
            self.height_input.setText(str(self.images[0].height))
            self.height_input.setEnabled(True)

            self.updateImage()

    def updateImage(self, width=None, height=None):
        if self.images:
            first_image = self.images[0]
            width_input_text = self.width_input.text()
            height_input_text = self.height_input.text()

            new_width = width or (int(width_input_text) if width_input_text else first_image.width)
            new_height = height or (int(height_input_text) if height_input_text else first_image.height)
            keep_aspect_ratio = self.aspect_ratio_check.isChecked()

            if keep_aspect_ratio:
                if new_width / self.original_aspect_ratio > new_height:
                    new_width = int(new_height * self.original_aspect_ratio)
                else:
                    new_height = int(new_width / self.original_aspect_ratio)

            if new_width <= 1 or new_height <= 1:
                pass
            else:
                new_size = (int(new_width), int(new_height))
                resized_image = first_image.resize(new_size, Image.Resampling.LANCZOS)

                image_bytes = io.BytesIO()
                resized_image.save(image_bytes, format="PNG")
                image_bytes.seek(0)

                qimage = QImage()
                qimage.loadFromData(image_bytes.read())

                pixmap = QPixmap.fromImage(qimage)

                self.image_display_window.display_image(pixmap)
                self.image_display_window.show()

    def width_input_changed(self, text):
        if text == '':
            self.image = None
            return self.image
        else:
            self.image = self.images_ref
            if self.aspect_ratio_check.isChecked() and self.image:
                self.height_input.blockSignals(True)

                if self.images[0].width > self.images[0].height:
                    self.height_input.setText(str(round(int(text) / self.original_aspect_ratio)))
                else:
                    self.height_input.setText(str(round(int(text) * self.original_aspect_ratio)))

                self.height_input.blockSignals(False)
            self.updateImage(width=int(text))

    def height_input_changed(self, text):
        if text == '':
            self.image = None
            return self.image
        else:
            self.image = self.images_ref
            if self.aspect_ratio_check.isChecked() and self.image:
                self.width_input.blockSignals(True)

                if self.images[0].width > self.images[0].height:
                    self.width_input.setText(str(round(int(text) * self.original_aspect_ratio)))
                else:
                    self.width_input.setText(str(round(int(text) / self.original_aspect_ratio)))
                
                self.width_input.blockSignals(False)
            self.updateImage(height=int(text))

    def save_resized_image(self):
        if self.image:
            new_size = (int(self.width_input.text()), int(self.height_input.text()))
            resized_image = self.image.resize(new_size, Image.Resampling.LANCZOS)
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif);;All Files (*)")
            if save_path:
                resized_image.save(save_path)

    def handle_back_button(self):
        self.mainWindowObject.show_main_page()

    def back_button_style(self):
        if is_dark_theme():
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-dark.svg'))
        else:
            self.back_button.setIcon(QIcon(f'{PATH_TO_FILE}arrow-left-light.svg'))
    # Image resizer
    def apply_image_resizer_page_dark_style(self):
        self.setStyleSheet("background-color: #262626")
        self.back_button.setStyleSheet(button_dark_style)
        self.resized_image_scroll_area.setStyleSheet(scroll_area_dark_style)
        self.resized_images_widget.setStyleSheet("background-color: #333333")
        self.width_input.setStyleSheet("background-color: #333333; padding: 3px 6px; border-radius: 3px")
        self.height_input.setStyleSheet("background-color: #333333; padding: 3px 6px; border-radius: 3px")
        self.save_resized_image_button.setStyleSheet(button_dark_style)
        self.select_image_button.setStyleSheet(button_dark_style)

    def apply_image_resizer_page_light_style(self):
        self.setStyleSheet("background-color: #e5e5e5")
        self.back_button.setStyleSheet(button_light_style)
        self.resized_image_scroll_area.setStyleSheet(scroll_area_light_style)
        self.resized_images_widget.setStyleSheet("background-color: #a5a5a5")
        self.width_input.setStyleSheet("background-color: #a5a5a5")
        self.height_input.setStyleSheet("background-color: #a5a5a5")
        self.save_resized_image_button.setStyleSheet(button_light_style)
        self.select_image_button.setStyleSheet(button_light_style)
