import sys
import os

PATH_TO_CSS_FILE = os.getenv("PATH_TO_CSS_FILE")

def load_styles(widget):
    css_files = ["base.css", "video_size_reducer.css"]
    styles = ""

    for css_file in css_files:
        css_files_path = None
        if PATH_TO_CSS_FILE:
            css_files_path = PATH_TO_CSS_FILE
        else:
            css_files_path = os.path.join(os.getcwd(), "styles", css_file)

        css_file_path = os.path.join(css_files_path, css_file)

        if os.path.exists(os.path.join(css_files_path, css_file)):
            with open(css_file_path, 'r') as file:
                styles += file.read()
        else:
            print(f"Failed to find {css_file}")

    widget.setStyleSheet(styles)