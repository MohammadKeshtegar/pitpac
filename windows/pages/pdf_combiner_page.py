from PyQt5.QtWidgets import QMainWindow, QPushButton, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from utils.backButton import BackButton

from utils.styles import button_dark_style, button_light_style, scroll_area_dark_style, scroll_area_light_style, remove_button_dark_style, remove_button_light_style
from utils.assets import is_dark_theme, settings, PATH_TO_FILE
from utils.notification import notification

import PyPDF4

class PDFCombinerPage(QMainWindow):
    def __init__(self, mainWindowObject):
        super().__init__()
        self.mainWindowObject = mainWindowObject
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

        if is_dark_theme():
            self.apply_pdf_combiner_dark_style()
        else:
            self.apply_pdf_combiner_light_style()

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
        for i in reversed(range(self.pdf_layout.count())):
            widget_to_remove = self.pdf_layout.itemAt(i).widget()
            self.pdf_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for file in self.pdf_files:
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            if is_dark_theme():
                row_widget.setStyleSheet("background-color: #202020; border-radius: 4px")
            else:
                row_widget.setStyleSheet("background-color: #e5e5e5; border-radius: 4px")
            
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

            remove_button.clicked.connect(lambda _, f=file: self.remove_pdf(f))
            row_layout.addWidget(remove_button)

            label = QLabel()
            pixmap = QPixmap(file)
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            row_layout.addWidget(label)

            name_label = QLabel(file)
            name_label.setWordWrap(True)
            name_label.setFixedWidth(400)

            if settings.mode  == "dark":
                name_label.setStyleSheet("color: #a3a3a3")
            else:
                name_label.setStyleSheet("color: #000000")

            row_layout.addWidget(name_label)

            self.pdf_layout.addWidget(row_widget)
            self.pdf_layout.setAlignment(Qt.AlignTop)

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

    # PDF combiner
    def apply_pdf_combiner_dark_style(self):
        self.central_widget.setStyleSheet("background-color: #262626")
        self.scroll_area.setStyleSheet(scroll_area_dark_style)
        self.pdf_container.setStyleSheet("background-color: #333333")
        self.button_pdf_combiner_select.setStyleSheet(button_dark_style)
        self.button_pdf_combiner_add.setStyleSheet(button_dark_style)
        self.button_pdf_combiner_remove_all.setStyleSheet(button_dark_style)
        self.button_pdf_combiner_save.setStyleSheet(button_dark_style)

    def apply_pdf_combiner_light_style(self):
        self.scroll_area.setStyleSheet(scroll_area_light_style)
        self.central_widget.setStyleSheet("background-color: #e5e5e5")
        self.pdf_container.setStyleSheet("background-color: #a5a5a5")
        self.button_pdf_combiner_select.setStyleSheet(button_light_style)
        self.button_pdf_combiner_add.setStyleSheet(button_light_style)
        self.button_pdf_combiner_remove_all.setStyleSheet(button_light_style)
        self.button_pdf_combiner_save.setStyleSheet(button_light_style)
