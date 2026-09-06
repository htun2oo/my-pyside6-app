import sys
import math
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QStackedWidget,
    QTabWidget, QCheckBox, QScrollArea, QComboBox
)


# -------------------------------------------------------------
# Clickable Card Canvas Box
# -------------------------------------------------------------
class SelectableCardWidget(QFrame):
    clicked = Signal()

    def __init__(self, title_text):
        super().__init__()
        self.setFixedSize(380, 420)
        self.setCursor(Qt.PointingHandCursor)
        
        self.is_selected = False
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(10)

        # Title (Front Side / Back Side)
        self.title_lbl = QLabel(title_text)
        self.title_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.title_lbl.setStyleSheet("color: #374151; background: transparent;")
        layout.addWidget(self.title_lbl)

        # Gray Container Outer Box
        self.gray_box = QFrame()
        self.gray_box.setStyleSheet("background-color: #9CA3AF; border-radius: 0px;")
        
        gray_layout = QVBoxLayout(self.gray_box)
        gray_layout.setContentsMargins(25, 40, 25, 40)

        # White PVC Card Area
        self.white_card = QFrame()
        self.white_card.setFixedHeight(210)
        self.white_card.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #4B5563;
            border-radius: 12px;
        """)

        gray_layout.addWidget(self.white_card)
        layout.addWidget(self.gray_box)

        self.update_selection_style()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.update_selection_style()

    def update_selection_style(self):
        if self.is_selected:
            self.setStyleSheet("QFrame { background-color: #E5E7EB; border: 1px solid #7C3AED; }")
            self.gray_box.setStyleSheet("background-color: #8D96A0; border: None;")
        else:
            self.setStyleSheet("QFrame { background-color: transparent; border: 1px solid transparent; }")
            self.gray_box.setStyleSheet("background-color: #9CA3AF; border: None;")


# -------------------------------------------------------------
# Card Designer Widget (Matching Image 2 Layout)
# -------------------------------------------------------------
class CardDesignerWidget(QWidget):
    def __init__(self, card_name="Credential Design 1", on_close_callback=None):
        super().__init__()
        self.on_close_callback = on_close_callback

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Purple Ribbon Header
        purple_ribbon = QFrame()
        purple_ribbon.setFixedHeight(36)
        purple_ribbon.setStyleSheet("background-color: #5B21B6;")
        purple_layout = QHBoxLayout(purple_ribbon)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        title_lbl = QLabel(f"{card_name} ✏")
        title_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF;")
        purple_layout.addWidget(title_lbl)
        purple_layout.addStretch()

        main_layout.addWidget(purple_ribbon)

        # 2. Designer Toolbar (Exact UI Match Image 2)
        toolbar = QFrame()
        toolbar.setFixedHeight(40)
        toolbar.setStyleSheet("background-color: #E5E7EB; border-bottom: 1px solid #D1D5DB;")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(10, 2, 10, 2)
        tb_layout.setSpacing(3)

        tools = [
            "↩", "↪", "📄+", "✂", "📋", "T", "T_i", "👤", "🖼", "📊", "〰", "||||", 
            "💳", "💻", "╱", "⬜", "⭕", "📏", "▦", "🔍+", "🔍-"
        ]
        
        for tool in tools:
            btn = QPushButton(tool)
            btn.setFixedSize(26, 26)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    border: 1px solid #D1D5DB;
                    border-radius: 2px;
                    font-size: 11px;
                    font-weight: bold;
                    color: #374151;
                }
                QPushButton:hover {
                    background-color: #F3F4F6;
                    border-color: #6B21A8;
                }
            """)
            tb_layout.addWidget(btn)

        tb_layout.addSpacing(8)
        zoom_lbl = QLabel("Zoom:")
        zoom_lbl.setStyleSheet("color: #374151; font-size: 11px;")
        tb_layout.addWidget(zoom_lbl)

        zoom_combo = QComboBox()
        zoom_combo.addItems(["100%", "75%", "50%", "150%"])
        zoom_combo.setFixedWidth(65)
        zoom_combo.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; font-size: 11px;")
        tb_layout.addWidget(zoom_combo)

        tb_layout.addSpacing(6)
        grid_icon_btn = QPushButton("▦")
        grid_icon_btn.setFixedSize(26, 26)
        grid_icon_btn.setStyleSheet("background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 2px;")
        tb_layout.addWidget(grid_icon_btn)

        tb_layout.addStretch()
        main_layout.addWidget(toolbar)

        # 3. Middle Design Workspace Area
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Canvas Area
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setStyleSheet("background-color: #F3F4F6; border: none;")

        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(10, 10, 10, 10)

        # Dynamic Active Layer Label
        self.active_layer_lbl = QLabel("Active Design Layer: Color")
        self.active_layer_lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.active_layer_lbl.setStyleSheet("color: #374151;")
        self.active_layer_lbl.setAlignment(Qt.AlignCenter)
        canvas_layout.addWidget(self.active_layer_lbl)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        self.front_card = SelectableCardWidget("Front Side")
        self.back_card = SelectableCardWidget("Back Side")

        cards_layout.addStretch()
        cards_layout.addWidget(self.front_card)
        cards_layout.addWidget(self.back_card)
        cards_layout.addStretch()

        canvas_layout.addLayout(cards_layout)
        canvas_layout.addStretch()

        canvas_scroll.setWidget(canvas_container)
        body_layout.addWidget(canvas_scroll, stretch=1)

        # Right Properties Side Panel
        right_panel = QFrame()
        right_panel.setFixedWidth(230)
        right_panel.setStyleSheet("background-color: #F9FAFB; border-left: 1px solid #D1D5DB;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        prop_tabs = QTabWidget()
        prop_tabs.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background: #E5E7EB;
                color: #374151;
                padding: 5px 14px;
                font-size: 11px;
                border: 1px solid #D1D5DB;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                border-bottom: 2px solid #6B21A8;
            }
        """)

        properties_page = QWidget()
        prop_page_layout = QVBoxLayout(properties_page)
        prop_page_layout.setContentsMargins(10, 12, 10, 12)

        self.prop_title = QLabel("— Front Side Properties")
        self.prop_title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.prop_title.setStyleSheet("color: #374151;")
        prop_page_layout.addWidget(self.prop_title)

        chk1 = QCheckBox("Rotate print orientation 180 degrees")
        chk1.setStyleSheet("color: #4B5563; font-size: 11px;")
        prop_page_layout.addWidget(chk1)

        chk2 = QCheckBox("Tactile Impression Module")
        chk2.setStyleSheet("color: #4B5563; font-size: 11px;")
        prop_page_layout.addWidget(chk2)

        prop_page_layout.addStretch()

        layers_page = QWidget()
        layers_layout = QVBoxLayout(layers_page)
        layers_layout.addWidget(QLabel("Layer 1: Color\nLayer 2: Black", alignment=Qt.AlignTop))

        prop_tabs.addTab(properties_page, "Properties")
        prop_tabs.addTab(layers_page, "Layers")

        right_layout.addWidget(prop_tabs)
        body_layout.addWidget(right_panel)

        main_layout.addLayout(body_layout, stretch=1)

        # 4. Bottom Action Footer
        footer = QFrame()
        footer.setFixedHeight(36)
        footer.setStyleSheet("background-color: #E5E7EB; border-top: 1px solid #D1D5DB;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 0, 15, 0)
        footer_layout.setSpacing(6)

        btn_style = """
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                font-size: 11px;
                border: none;
                border-radius: 3px;
                padding: 4px 12px;
            }
            QPushButton:hover { background-color: #1D4ED8; }
            QPushButton:disabled { background-color: #9CA3AF; color: #F3F4F6; }
        """

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(btn_style)

        save_as_btn = QPushButton("Save As...")
        save_as_btn.setStyleSheet(btn_style)
        save_as_btn.setEnabled(False)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(btn_style)
        if self.on_close_callback:
            close_btn.clicked.connect(self.on_close_callback)

        print_sample_btn = QPushButton("Print Sample")
        print_sample_btn.setStyleSheet(btn_style)
        print_sample_btn.setEnabled(False)

        footer_layout.addWidget(save_btn)
        footer_layout.addWidget(save_as_btn)
        footer_layout.addWidget(close_btn)
        footer_layout.addWidget(print_sample_btn)
        footer_layout.addStretch()

        main_layout.addWidget(footer)

        # Card Click Signal Events Handling
        self.front_card.clicked.connect(self.select_front_side)
        self.back_card.clicked.connect(self.select_back_side)

        # Default Active Selection: Front Side
        self.select_front_side()

    def select_front_side(self):
        self.front_card.set_selected(True)
        self.back_card.set_selected(False)
        self.active_layer_lbl.setText("Active Design Layer: Color")
        self.prop_title.setText("— Front Side Properties")

    def select_back_side(self):
        self.front_card.set_selected(False)
        self.back_card.set_selected(True)
        self.active_layer_lbl.setText("Active Design Layer: Black")
        self.prop_title.setText("— Back Side Properties")
