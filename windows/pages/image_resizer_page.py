from PyQt5.QtWidgets import QMainWindow, QPushButton, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QFileDialog, QLabel
from PyQt5.QtGui import QFont, QIntValidator, QIcon, QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

from image_preview import ImageDisplayWindow
from components.BackButton import BackButton

from utils.assets import PATH_TO_ICON_FILE, settings
from utils.notification import notification

import io
import os

class ImageResizerPage(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
        
        if settings.show_image_preview:
            self.image_display_window = ImageDisplayWindow()
        self.setup_image_resizer_page()

    def setup_image_resizer_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Back button
        self.back_button = BackButton(mainWindowObject=self.mainWindowObject)

        self.images_scroll_area = QScrollArea()
        self.images_scroll_area.setWidgetResizable(True)
        self.images_scroll_area.setProperty("class", "scroll-area-dark")

        self.images_container = QWidget()
        self.resized_images_layout = QVBoxLayout(self.images_container)
        self.images_scroll_area.setWidget(self.images_container)

        # Select image button
        self.select_image_button = QPushButton("Open Images")
        self.select_image_button.clicked.connect(self.selectImage)
        self.select_image_button.setFixedWidth(300)

        # Remove all image button
        self.remove_all_images_button = QPushButton("Remove all images")
        self.remove_all_images_button.clicked.connect(self.remove_all_images)
        self.remove_all_images_button.setFixedWidth(300)
        self.remove_all_images_button.setEnabled(False)

        # Add image button
        self.add_image_button = QPushButton("Add image")
        self.add_image_button.clicked.connect(self.add_image)
        self.add_image_button.setFixedWidth(300)
        self.add_image_button.setEnabled(False)

        # Save button
        self.save_resized_image_button = QPushButton("Save")
        self.save_resized_image_button.clicked.connect(self.save_resized_image)
        self.save_resized_image_button.setFixedWidth(300)
        self.save_resized_image_button.setEnabled(False)
        
        self.select_image_button.setProperty("class", "button-dark")
        self.remove_all_images_button.setProperty("class", "button-dark")
        self.add_image_button.setProperty("class", "button-dark")
        self.save_resized_image_button.setProperty("class", "button-dark")

        # Width input
        self.width_input = QLineEdit(self)
        self.width_input.setPlaceholderText("width")
        self.width_input.setMaximumWidth(300)
        self.width_input.setFont(QFont("Arial", 14))
        self.width_input.setValidator(QIntValidator())
        self.width_input.setEnabled(False)
        self.width_input.textChanged.connect(self.width_input_changed)

        # Height input
        self.height_input = QLineEdit(self)
        self.height_input.setPlaceholderText("height")
        self.height_input.setMaximumWidth(300)
        self.height_input.setFont(QFont("Arial", 14))
        self.height_input.setValidator(QIntValidator())
        self.height_input.setEnabled(False)
        self.height_input.textChanged.connect(self.height_input_changed)

        # Aspect ratio
        self.aspect_ratio_check = QCheckBox("Aspect Ratio", self)
        self.aspect_ratio_check.setChecked(True)

        # Convert to icon
        self.convert_to_icon_check = QCheckBox("Convert to icon file", self)
        self.convert_to_icon_check.setChecked(False)

        # Layout for width and height inputs
        width_height_layout = QVBoxLayout()
        width_height_layout.addWidget(self.width_input)
        width_height_layout.addWidget(self.height_input)
        width_height_layout.addWidget(self.aspect_ratio_check)
        width_height_layout.addWidget(self.convert_to_icon_check)

        # Layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.select_image_button, alignment=Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.add_image_button, alignment=Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.remove_all_images_button, alignment=Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.save_resized_image_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Layout for width and height inputs and buttons layout
        width_height_buttons_layout = QHBoxLayout()
        width_height_buttons_layout.addLayout(width_height_layout)
        width_height_buttons_layout.addLayout(button_layout)

        # Add widgets to the main layout
        layout.addWidget(self.back_button)
        layout.addWidget(self.images_scroll_area)
        layout.addLayout(width_height_buttons_layout)

    def display_selected_images(self, layout):
        for i in reversed(range(layout.count())): 
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for file in self.image_files:
            row_widget = QWidget()
            row_layout = QHBoxLayout()

            row_widget.setStyleSheet("background-color: #262626; border-radius: 4px")
            row_widget.setLayout(row_layout)
            row_widget.setFixedHeight(120)
            row_widget.setCursor(Qt.CursorShape.PointingHandCursor)
            row_widget.mousePressEvent = lambda event, f=file: self.update_preview(f)

            label = QLabel()
            pixmap = QPixmap(file)
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

            name_label = QLabel(os.path.basename(file))
            name_label.setWordWrap(True)
            name_label.setFixedWidth(380)
            name_label.setStyleSheet("color: #a3a3a3")

            remove_button = QPushButton()
            remove_button.setIcon(QIcon(f"{PATH_TO_ICON_FILE}x-dark.svg"))
            remove_button.setFixedSize(30, 30)
            remove_button.setProperty("class", "remove-button-dark")          
            remove_button.clicked.connect(lambda _, f=file: self.remove_image(layout, f))

            row_layout.addWidget(label)
            row_layout.addWidget(name_label)
            row_layout.addWidget(remove_button)

            layout.addWidget(row_widget)
            layout.setAlignment(Qt.AlignTop)

        if self.image_files:
            self.update_preview(self.image_files[0])

    def update_preview(self, file):
        if not settings.show_image_preview:
            return

        pixmap = QPixmap(file)
        self.image_display_window.display_image(pixmap)
        self.image_display_window.show()

        for index, f in enumerate(self.image_files):
            row_widget = self.resized_images_layout.itemAt(index).widget()
            if f == file:
                row_widget.setStyleSheet("background-color: #202020; border-radius: 4px;")
            else:
                row_widget.setStyleSheet("background-color: #262626; border-radius: 4px;")

    def remove_image(self, layout, file):
        self.image_files.remove(file)
        self.display_selected_images(layout)
        if not self.image_files:
            self.width_input.setText("")
            self.height_input.setText("")
            self.remove_all_images_button.setEnabled(False)
            self.add_image_button.setEnabled(False)
            self.save_resized_image_button.setEnabled(False)
            self.width_input.setEnabled(False)
            self.height_input.setEnabled(False)
            
            if settings.show_image_preview:
                self.image_display_window.close()
    
    def add_image(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Add Images", settings.location, "Images (*.png *.jpg *.jpeg *.jfif);;All Files (*)", options=options)
        if files:
            self.image_files.extend(files)
            self.display_selected_images(self.resized_images_layout)

    def remove_all_images(self):
        self.image_files = []
        self.width_input.setText("")
        self.height_input.setText("")
        self.display_selected_images(self.resized_images_layout)
        self.save_resized_image_button.setEnabled(False)
        self.remove_all_images_button.setEnabled(False)
        self.add_image_button.setEnabled(False)
        self.image_display_window.close()

    def selectImage(self): 
        options = QFileDialog.Options() 
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif *.jfif)", options=options) 
        if filenames: 
            self.images_scroll_area.setVisible(True) 
            self.image_files = filenames 
            self.display_selected_images(self.resized_images_layout) 
            self.images = self.images_ref = [Image.open(image_filename) for image_filename in filenames] 

            self.original_aspect_ratio = self.images[0].width / self.images[0].height
            self.width_input.setText(str(self.images[0].width))
            self.height_input.setText(str(self.images[0].height))
            
            self.width_input.setEnabled(True)
            self.height_input.setEnabled(True)
            self.remove_all_images_button.setEnabled(True) 
            self.add_image_button.setEnabled(True) 
            self.save_resized_image_button.setEnabled(True)  

            self.update_preview(filenames[0])

    def updateImage(self, width=None, height=None):
        if self.images:
            first_image = self.images[0]
            width_input_text = self.width_input.text()
            height_input_text = self.height_input.text()

            new_width =  width if (width != '') else (int(width_input_text) if width_input_text else first_image.width)
            new_height = height or (int(height_input_text) if height_input_text else first_image.height)
            keep_aspect_ratio = self.aspect_ratio_check.isChecked()

            if keep_aspect_ratio:
                if self.original_aspect_ratio < 1:
                    new_width = int(new_height * self.original_aspect_ratio)
                else:
                    new_height = int(new_width / self.original_aspect_ratio)

            if new_width and new_height and  (new_width <= 1 or new_height <= 1): # Just pass, because it stuck when there is no value in the input
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

                if settings.show_image_preview:
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
                self.height_input.setText(str(round(int(text) / self.original_aspect_ratio)))
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
                self.width_input.setText(str(round(int(text) * self.original_aspect_ratio)))
                self.width_input.blockSignals(False)
            self.updateImage(height=int(text))

    def save_resized_image(self):
        if self.image:
            for image in self.image:
                new_size = (int(self.width_input.text()), int(self.height_input.text()))
                resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

                save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", settings.location, "Image Files (*.png *.jpg *.jpeg *.gif *.ico);;All Files (*)")
                if save_path:
                    if self.convert_to_icon_check.isChecked():
                        self.convert_image_to_icon(resized_image, save_path)
                    else:
                        resized_image.save(save_path)
            notification(self, "Images saved!")

    def convert_image_to_icon(self, pil_image, save_path):
        pil_image = pil_image.convert("RGBA")
        data = pil_image.tobytes("raw", "RGBA")
        q_image = QImage(data, pil_image.width, pil_image.height, QImage.Format.Format_RGBA8888)

        pixmap = QPixmap.fromImage(q_image)
        icon = QIcon(pixmap)

        icon_pixmap = icon.pixmap(256, 256)
        icon_pixmap.save(save_path, "ICO")
