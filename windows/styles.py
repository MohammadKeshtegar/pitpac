from assets import is_dark_theme, PATH_TO_FILE

button_dark_style = f"""
    QPushButton:disabled {{ color: #525252 }} 
    QPushButton {{ padding: 5px 10px }} 
    QPushButton:hover {{ background-color: #313131 }}
"""

button_light_style = f"""
    QPushButton:disabled {{ color: #646464 }} 
    QPushButton {{ padding: 5px 10px; color: #262626 }} 
    QPushButton:hover {{ background-color: #4464e6 }}
"""

scroll_area_dark_style = """
    QScrollBar:vertical { background-color: #262626; border: 1px solid #111111 }
    QScrollBar::handle:vertical { margin: 16px 0; border-radius: 2px; border: 1px solid #404040; background-color: #1e1e1e }
    QScrollBar::handle:vertical:pressed { background-color: #333333 }
    QScrollBar:horizontal { background-color: #262626; border: 1px solid #111111 }
    QScrollBar::handle:horizontal { margin: 0 16px; border-radius: 2px; border: 1px solid #404040; background-color: #1e1e1e }
    QScrollBar::handle:horizontal:pressed { background-color: #333333 }
    QScrollArea { background-color: #525252 }
"""

scroll_area_light_style = """
    QScrollBar:vertical { background-color: #b5b5b5; border: 1px solid #737373 }
    QScrollBar::handle:vertical { margin: 16px 0; border-radius: 2px; border: 1px solid #626262; background-color: #7f7f7f }
    QScrollBar::handle:vertical:pressed { background-color: #333333 }
    QScrollBar:horizontal { background-color: #b5b5b5; border: 1px solid #737373 }
    QScrollBar::handle:horizontal { margin: 0 16px; border-radius: 2px; border: 1px solid #626262; background-color: #7f7f7f }
    QScrollBar::handle:horizontal:pressed { background-color: #333333 }
    QScrollArea { background-color: #646464 }
"""

remove_button_dark_style = f"""
    QPushButton {{ background-color: #1a1a1a; border: 1px solid #404040 }} 
    QPushButton:hover {{ background-color: #313131 }}
"""

remove_button_light_style = f"""
    QPushButton {{ background-color: #fff; border: 1px solid #a3a3a3 }} 
    QPushButton:hover {{ background-color: #4464e6 }}
"""

combobox_dark_style = """ 
    QComboBox:hover { background-color: #313131 }
    QComboBox::item:hover { background-color: #646464 }
""" 

combobox_light_style = """ 
    QComboBox { color: #262626 }
    QComboBox:hover { background-color: #4464e6 }
    QComboBox::item:hover { background-color: #646464 }
""" 

button_size = 400
