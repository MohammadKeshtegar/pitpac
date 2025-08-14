from PyQt5.QtWidgets import QMainWindow, QPushButton, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt

from components.BackButton import BackButton

from utils.assets import  settings, PATH_TO_ICON_FILE
from utils.notification import notification

import PyPDF4
import fitz
import os

class PDFCombinerPage(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
        self.setObjectName("PDFCombiner")
        self.setup_pdf_combiner_page()

    def setup_pdf_combiner_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        
        # Redirect button
        self.back_button = BackButton(mainWindowObject=self.mainWindowObject)
    
        layout.setAlignment(self.back_button, Qt.AlignLeft)
        layout.addWidget(self.back_button)
    
        # Creating scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setProperty("class", "scroll-area-dark")
        layout.addWidget(self.scroll_area)

        # Creating pdf container
        self.pdf_container = QWidget()
        self.pdf_layout = QVBoxLayout()
        self.pdf_container.setLayout(self.pdf_layout)
        self.scroll_area.setWidget(self.pdf_container)

        # Creating buttons container 
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        layout.addWidget(buttons_container)

        # Select, Remove, Add button container
        three_buttons_container = QWidget()
        three_buttons_layout = QHBoxLayout(three_buttons_container)
        buttons_layout.addWidget(three_buttons_container)

        # Select button
        self.button_pdf_combiner_select = QPushButton("Select pdf")
        three_buttons_layout.addWidget(self.button_pdf_combiner_select)
        three_buttons_layout.setAlignment(self.button_pdf_combiner_select, Qt.AlignCenter)

        # Add button
        self.button_pdf_combiner_add = QPushButton("Add pdf")
        self.button_pdf_combiner_add.setEnabled(False)
        three_buttons_layout.addWidget(self.button_pdf_combiner_add)
        three_buttons_layout.setAlignment(self.button_pdf_combiner_add, Qt.AlignCenter)

        # Remove all button
        self.button_pdf_combiner_remove_all = QPushButton("Remove All")
        self.button_pdf_combiner_remove_all.setEnabled(False)
        three_buttons_layout.addWidget(self.button_pdf_combiner_remove_all)
        three_buttons_layout.setAlignment(self.button_pdf_combiner_remove_all, Qt.AlignCenter)

        # Save button
        self.button_pdf_combiner_save = QPushButton("Combine PDFs")
        self.button_pdf_combiner_save.setEnabled(False)
        buttons_layout.addWidget(self.button_pdf_combiner_save)
        buttons_layout.setAlignment(self.button_pdf_combiner_save, Qt.AlignRight)

        self.button_pdf_combiner_select.setProperty("class", "button-dark")
        self.button_pdf_combiner_add.setProperty("class", "button-dark")
        self.button_pdf_combiner_remove_all.setProperty("class", "button-dark")
        self.button_pdf_combiner_save.setProperty("class", "button-dark")

        self.button_pdf_combiner_select.clicked.connect(self.open_pdf_dialog)
        self.button_pdf_combiner_add.clicked.connect(self.add_pdf)
        self.button_pdf_combiner_remove_all.clicked.connect(self.remove_all_pdfs)
        self.button_pdf_combiner_save.clicked.connect(self.save_pdf_combiner)

        self.pdf_files = []

    def open_pdf_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", settings.location, "PDF Files (*.pdf);;All Files (*)", options=options)
        if files:
            self.pdf_files = files
            self.display_selected_pdfs()
            self.button_pdf_combiner_save.setEnabled(True)
            self.button_pdf_combiner_remove_all.setEnabled(True)
            self.button_pdf_combiner_add.setEnabled(True)

    def display_selected_pdfs(self):    
        # Clear existing widgets
        for i in reversed(range(self.pdf_layout.count())):
            widget_to_remove = self.pdf_layout.itemAt(i).widget()
            self.pdf_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for index, file in enumerate(self.pdf_files):
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            row_widget.setStyleSheet("background-color: #202020; border-radius: 4px")
            row_widget.setLayout(row_layout)
            row_widget.setFixedHeight(120)

            # Remove button
            remove_button = QPushButton()
            remove_button.setIcon(QIcon(f"{PATH_TO_ICON_FILE}x-dark.svg"))
            remove_button.setFixedSize(30, 30)
            remove_button.setProperty("class", "remove-button-dark")
            remove_button.clicked.connect(lambda _, f=file: self.remove_pdf(f))

            # PDF thumbnail
            label = QLabel()
            pixmap = self.get_pdf_thumbnail(file)
            if pixmap and not pixmap.isNull():
                label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            else:
                # Fallback to generic PDF icon
                icon_path = f"{PATH_TO_ICON_FILE}pdf-icon.png"  # Replace with your icon path
                if os.path.exists(icon_path):
                    label.setPixmap(QPixmap(icon_path).scaled(100, 100, Qt.KeepAspectRatio))
                else:
                    label.setText("No Preview")
                print(f"No valid thumbnail generated for {file}")
            
            label.setFixedSize(100, 100)
            label.setStyleSheet("border: none;")

            # PDF name
            name_label = QLabel(os.path.basename(file))
            name_label.setWordWrap(True)
            name_label.setFixedWidth(380)
            name_label.setStyleSheet("color: #a3a3a3")
            
            row_layout.addWidget(label)
            row_layout.addWidget(name_label)
            row_layout.addWidget(remove_button)

            self.pdf_layout.addWidget(row_widget)
            self.pdf_layout.setAlignment(Qt.AlignTop)

    def get_pdf_thumbnail(self, pdf_file, zoom=1.0):
        try:
            # Verify file exists
            if not os.path.exists(pdf_file):
                print(f"Error: PDF file not found: {pdf_file}")
                return None
            
            # Open PDF
            doc = fitz.open(pdf_file)
            if doc.page_count == 0:
                print(f"Error: PDF has no pages: {pdf_file}")
                doc.close()
                return None
            
            # Check for encryption
            if doc.is_encrypted:
                print(f"Error: PDF is encrypted and cannot be rendered: {pdf_file}")
                doc.close()
                return None
            
            # Load first page
            page = doc.load_page(0)
            
            # Check page dimensions
            rect = page.rect
            if rect.is_empty or rect.width <= 0 or rect.height <= 0:
                print(f"Error: First page is empty or has invalid dimensions (width: {rect.width}, height: {rect.height}): {pdf_file}")
                doc.close()
                return None
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            if pix.width == 0 or pix.height == 0:
                print(f"Error: Rendered pixmap is empty (width: {pix.width}, height: {pix.height}): {pdf_file}")
                doc.close()
                return None
            
            # Verify samples
            expected_samples = pix.width * pix.height * pix.n
            if not pix.samples or len(pix.samples) != expected_samples:
                print(f"Error: Invalid pixmap samples (expected: {expected_samples}, got: {len(pix.samples)}, n: {pix.n}): {pdf_file}")
                doc.close()
                return None

            # Create QImage
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            if image.isNull():
                print(f"Error: Failed to create QImage with Format_RGB888 for {pdf_file}. Trying Format_RGBA8888...")
                # Fallback to RGBA8888
                image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGBA8888)
                if image.isNull():
                    print(f"Error: Failed to create QImage with Format_RGBA8888 for {pdf_file}")
                    doc.close()
                    return None
            
            # Convert to QPixmap
            pixmap = QPixmap.fromImage(image)
            if pixmap.isNull():
                print(f"Error: Failed to create QPixmap from QImage for {pdf_file}")
                doc.close()
                return None
            
            doc.close()
            return pixmap
        except Exception as e:
            print(f"Unexpected error generating thumbnail for {pdf_file}: {str(e)}")
            if 'doc' in locals():
                doc.close()
            return None

    def add_pdf(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Add pdfs", settings.location, "PDF Files (*.pdf);;All Files (*)", options=options)
        if files:
            self.pdf_files.extend(files)
            self.display_selected_pdfs()

    def remove_all_pdfs(self):
        self.pdf_files = []
        self.display_selected_pdfs()
        self.button_pdf_combiner_add.setEnabled(False)
        self.button_pdf_combiner_remove_all.setEnabled(False)
        self.button_pdf_combiner_save.setEnabled(False)

    def save_pdf_combiner(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", settings.location, "PDF Files (*.pdf);;All Files (*)")
        if save_path:
            pdf_merger = PyPDF4.PdfFileMerger()
            for pdf in self.pdf_files:
                pdf_merger.append(pdf)
            with open(f"{save_path}.pdf", 'wb') as f:
                pdf_merger.write(f)
            notification(self, "PDF saved successfully!")

    def remove_pdf(self, file):
        self.pdf_files.remove(file)
        self.display_selected_pdfs()
        if not self.pdf_files:
            self.button_pdf_combiner_add.setEnabled(False)
            self.button_pdf_combiner_remove_all.setEnabled(False)
            self.button_pdf_combiner_save.setEnabled(False)
