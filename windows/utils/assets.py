from PyQt5.QtCore import QSettings
from dotenv import load_dotenv
import os

load_dotenv()

PATH_TO_FILE = os.getenv("PATH_TO_FILE")
START_LOCATION = os.getenv("START_LOCATION")

def handle_back_button(self):
    self.stack.setCurrentWidget(self.main_page)

def is_dark_theme():
    return settings.mode == "dark"

def load_theme_prefernence():
    app_settings = QSettings("Pitpac", "pitpac")
    mode = app_settings.value("mode", "dark")
    location = app_settings.value("location", START_LOCATION)
    font_family = app_settings.value("font_family", "Noto Sans")
    font_size = app_settings.value("font_size", 10, type=int)
    show_image_preview = app_settings.value("show_image_preview", True, type=bool)
    return mode, location, font_family, font_size, show_image_preview

def save_theme_preference():
    app_settings = QSettings("Pitpac", "pitpac")
    app_settings.setValue("mode", settings.mode)
    app_settings.setValue("location", settings.location)
    app_settings.setValue("font_family", settings.font_family)
    app_settings.setValue("font_size", settings.font_size)
    app_settings.setValue("show_image_preview", settings.show_image_preview)

class Settings:
    def __init__(self):
        self.mode, self.location, self.font_family, self.font_size, self.show_image_preview = load_theme_prefernence()

settings = Settings()
