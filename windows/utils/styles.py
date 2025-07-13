import os

def load_styles(widget):
    css_files = ["base.css", "video_size_reducer.css"]
    styles = ""

    for css_file in css_files:
        css_file_path = os.path.join("windows", "styles", css_file)

        if os.path.exists(os.path.join("windows", "styles", css_file)):
            with open(css_file_path, 'r') as file:
                styles += file.read()
        else:
            print(f"Failed to find {css_file}")

    widget.setStyleSheet(styles)