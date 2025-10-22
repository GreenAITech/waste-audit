import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_EXPAND_PNG = os.path.join(_CURRENT_DIR, "expand.png").replace('\\', '/')

BUTTON_CONNECT_CAMERA = """
    QPushButton {
        height: 30px;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        font-size: 18px;
        font-family: 'Arial';
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        margin-top: 10px; 
    }
    QPushButton:hover {
        background-color: #357ABD;
    }
    QPushButton:pressed {
        background-color: #2E6DA4;
    }
    QPushButton:disabled {
        background-color: #ADADAD;
    }
"""

BUTTON_DISCONNECT_CAMERA = """
    QPushButton {
        height: 30px;
        background-color: #A8382C;
        color: white;
        font-weight: bold;
        font-size: 18px;
        font-family: 'Arial';
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        margin-top: 10px; 
    }
    QPushButton:hover {
        background-color: #8C2F24;
    }
    QPushButton:pressed {
        background-color: #A93226;
    }
    QPushButton:disabled {
        background-color: #ADADAD;
    }
"""

BUTTON_CONNECT_SERIAL = """
    QPushButton {
        height: 30px;
        color: white;
        background-color: #4A90E2;
        font-weight: bold;
        font-family: 'Arial';
        font-size: 18px;
        border-radius: 10px; 
        padding: 10px 10px;  
    }
    QPushButton:hover {
        background-color: #357ABD;
    }
    QPushButton:pressed {
        background-color: #2E6DA4;
    }
    QPushButton:disabled {
        background-color: #ADADAD;
    }
"""

BUTTON_DISCONNECT_SERIAL = """
    QPushButton {
        height: 30px;
        background-color: #A8382C;
        color: white;
        font-weight: bold;
        font-family: 'Arial';
        font-size: 18px;
        border: none;
        border-radius: 10px; 
        padding: 10px 10px;  
    }
    QPushButton:hover {
        background-color: #8C2F24;
    }
    QPushButton:pressed {
        background-color: #A93226;
    }
    QPushButton:disabled {
        background-color: #ADADAD;
    }
"""

BUTTON_ZERO_TARE = """
    QPushButton {
        height: 30px;
        background-color: #5b8487;
        color: white;
        font-weight: bold;
        font-size: 20px;
        font-family: 'Arial';
        border: none;
        border-radius: 10px; 
        padding: 12px 24px;  
    }
    QPushButton:hover {
        background-color: #2c6165;
    }
    QPushButton:pressed {
        background-color: #2c6165;
    }
    QPushButton:disabled {
        background-color: #ADADAD;
    }
"""


COMBOBOX_PORT_SELECTOR = f"""
    QComboBox {{
        background-color: #f0f0f0;
        color: black;  
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 0px 30px 0px 8px;
        min-height: 40px;
        font-size: 20px;
        font-family: 'Arial';
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 1px solid #555555;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }}
    QComboBox::down-arrow {{
        image: url({_EXPAND_PNG});
        width: 20px;
        height: 20px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #f0f0f0; 
        color: black;
        border: 1px solid #555555;
        outline: none;
        padding: 0px;
    }}
    QComboBox QAbstractItemView::item {{
        padding-left: 10px;
        border: none;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: #CCCCCC;
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: #CCCCCC;
        color: black;
    }}
"""

COMBOBOX_CATEGORY_SELECTOR = f"""    
    QComboBox {{
        background-color: #f0f0f0;
        color: black;  
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 0px 30px 0px 8px;
        min-height: 40px;
        font-size: 20px;
        font-family: 'Arial';
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 1px solid #555555;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }}
    QComboBox::down-arrow {{
        image: url({_EXPAND_PNG});
        width: 20px;
        height: 20px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #f0f0f0; 
        color: black;
        border: 1px solid #555555;
        outline: none;
        padding: 0px;
        font-size: 20px;
    }}
    QComboBox QAbstractItemView::item {{
        padding-left: 10px;
        border: none;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: #CCCCCC;
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: #CCCCCC;
        color: black;
    }}
"""

FRAME_CAMERA = "background-color: #111; border: 1px solid #444;"

# Label
LABEL_CAMERA = "color: #f9f9f9; font-size: 20px;"
LABEL_WEIGHT = "font-family: 'Arial'; font-size: 18px;"
LABEL_STATUS = "color: #888; font-size: 12px;"
NORMAL_LABEL = "font-family: 'Arial'; color: #FFFFFF; background-color: #54B1DE; font-size: 28px; padding: 10px; border-radius:4px;"
ALERT_LABEL = "font-family: 'Arial'; color: #FFFFFF; background-color: #ED9061; font-size: 28px; padding: 10px; border-radius:4px;"