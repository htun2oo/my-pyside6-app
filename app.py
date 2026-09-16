import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, 
    QCheckBox, QFrame, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class PropertiesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Properties Window')
        self.setFixedSize(300, 260)
        self.setStyleSheet("background-color: #A0A0A0;") # အပြင်ဘက် နောက်ခံခဲရောင်

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Tab Widget
        self.tabs = QTabWidget()
        
        # ----------------- Tab 1: Properties -----------------
        tab_properties = QWidget()
        tab_properties.setStyleSheet("background-color: #FFFFFF;")
        
        tab_properties_layout = QVBoxLayout(tab_properties)
        tab_properties_layout.setContentsMargins(12, 12, 12, 12)
        tab_properties_layout.setAlignment(Qt.AlignTop)

        # Group Box Container (ဒုတိယပုံပါ အဖြူရောင် ဘောင်ကွက်)
        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                border-radius: 4px;
            }
        """)
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(0, 0, 0, 10)
        card_layout.setSpacing(10)

        # Header (- Front Side Properties)
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #EAEAEA;
                border: none;
                border-bottom: 1px solid #D0D0D0;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 6, 8, 6)
        header_layout.setSpacing(6)

        minus_lbl = QLabel("-")
        minus_lbl.setFont(QFont("Arial", 11, QFont.Bold))
        minus_lbl.setStyleSheet("color: #333333; border: none; background: transparent;")

        title_lbl = QLabel("Front Side Properties")
        title_lbl.setFont(QFont("Arial", 9, QFont.Bold))
        title_lbl.setStyleSheet("color: #222222; border: none; background: transparent;")

        header_layout.addWidget(minus_lbl)
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        card_layout.addWidget(header_frame)

        # Checkboxes Container
        checkbox_container = QWidget()
        checkbox_container.setStyleSheet("border: none;")
        checkbox_layout = QVBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(10, 0, 10, 0)
        checkbox_layout.setSpacing(10)

        # Checkbox Style (ဒုတိယပုံအတိုင်း ပုံစံဖော်ခြင်း)
        checkbox_style = """
            QCheckBox {
                font-size: 12px;
                font-family: Arial;
                color: #334455;
                spacing: 6px;
                border: none;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #888888;
                border-radius: 2px;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #334455;
            }
        """

        self.cb1 = QCheckBox("Rotate print orientation 180\ndegrees")
        self.cb1.setStyleSheet(checkbox_style)

        self.cb2 = QCheckBox("Tactile Impression Module")
        self.cb2.setStyleSheet(checkbox_style)

        checkbox_layout.addWidget(self.cb1)
        checkbox_layout.addWidget(self.cb2)

        card_layout.addWidget(checkbox_container)
        tab_properties_layout.addWidget(card_frame)

        # ----------------- Tab 2: Layers -----------------
        tab_layers = QWidget()
        tab_layers.setStyleSheet("background-color: #FFFFFF;")

        # Add tabs
        self.tabs.addTab(tab_properties, "Properties")
        self.tabs.addTab(tab_layers, "Layers")

        # Tab Bar Style (ဒုတိယပုံပါ Tab ဒီဇိုင်းအတိုင်း)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background: #E5E5E5;
                color: #333333;
                font-size: 12px;
                font-weight: bold;
                font-family: Arial;
                padding: 6px 20px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                color: #000000;
            }
        """)

        main_layout.addWidget(self.tabs)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PropertiesWindow()
    window.show()
    sys.exit(app.exec())
