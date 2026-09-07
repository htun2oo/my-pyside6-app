import sys
import math
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QStackedWidget,
    QTabWidget, QCheckBox, QScrollArea, QComboBox, QGridLayout
)

# -------------------------------------------------------------
# Top (Horizontal) Ruler Widget
# -------------------------------------------------------------
class HorizontalRulerWidget(QWidget):
    def __init__(self, height=22):
        super().__init__()
        self.setFixedHeight(height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)
        
        painter.fillRect(self.rect(), QColor("#E5E7EB"))
        painter.setPen(QPen(QColor("#9CA3AF"), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        font = QFont("Segoe UI", 7)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#374151"), 1))

        step = 10
        major_step = 50
        num_val = 0

        for x in range(0, self.width(), step):
            if x % major_step == 0:
                painter.drawLine(x, self.height() - 12, x, self.height())
                if x > 0:
                    painter.drawText(x - 10, 2, 20, 10, Qt.AlignCenter, str(num_val))
                    num_val += 2
            elif x % (step * 2.5) == 0:
                painter.drawLine(x, self.height() - 8, x, self.height())
            else:
                painter.drawLine(x, self.height() - 5, x, self.height())


# -------------------------------------------------------------
# Left (Vertical) Ruler Widget
# -------------------------------------------------------------
class VerticalRulerWidget(QWidget):
    def __init__(self, width=22):
        super().__init__()
        self.setFixedWidth(width)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        painter.fillRect(self.rect(), QColor("#E5E7EB"))
        painter.setPen(QPen(QColor("#9CA3AF"), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        font = QFont("Segoe UI", 7)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#374151"), 1))

        step = 10
        major_step = 50
        num_val = 0

        for y in range(0, self.height(), step):
            if y % major_step == 0:
                painter.drawLine(self.width() - 12, y, self.width(), y)
                if y > 0:
                    painter.drawText(2, y - 8, 10, 14, Qt.AlignCenter, str(num_val))
                    num_val += 2
            elif y % (step * 2.5) == 0:
                painter.drawLine(self.width() - 8, y, self.width(), y)
            else:
                painter.drawLine(self.width() - 5, y, self.width(), y)


# -------------------------------------------------------------
# Fully Interactive Custom Layer Item Widget
# -------------------------------------------------------------
class LayerItemWidget(QFrame):
    item_selected = Signal(str)      # Emits Layer Name on selection
    visibility_toggled = Signal(str, bool) # Emits Layer Name, IsVisible
    check_toggled = Signal(str, bool)      # Emits Layer Name, IsChecked

    def __init__(self, layer_name, is_selected=False, is_checked=False, is_visible=True):
        super().__init__()
        self.layer_name = layer_name
        self.is_selected = is_selected
        self.is_visible = is_visible

        self.setFixedHeight(28)
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(8)

        # Eye Button Toggle
        self.eye_btn = QPushButton("👁" if is_visible else "❌")
        self.eye_btn.setFixedSize(20, 20)
        self.eye_btn.setFont(QFont("Segoe UI", 8))
        self.eye_btn.setCursor(Qt.PointingHandCursor)
        self.eye_btn.setStyleSheet("""
            QPushButton {
                background: transparent; border: none; color: #4B5563;
            }
            QPushButton:hover { color: #2563EB; }
        """)
        self.eye_btn.clicked.connect(self.toggle_eye)
        layout.addWidget(self.eye_btn)

        # Layer Name Label
        self.name_lbl = QLabel(layer_name)
        self.name_lbl.setFont(QFont("Segoe UI", 9))
        self.name_lbl.setStyleSheet("background: transparent;")
        layout.addWidget(self.name_lbl, stretch=1)

        # Interactive Checkbox
        self.chk = QCheckBox()
        self.chk.setChecked(is_checked)
        self.chk.setCursor(Qt.PointingHandCursor)
        self.chk.setStyleSheet("""
            QCheckBox::indicator {
                width: 13px; height: 13px;
                border: 1px solid #9CA3AF; background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #2563EB; border-color: #2563EB;
            }
        """)
        self.chk.toggled.connect(self.on_checkbox_toggled)
        layout.addWidget(self.chk)

        self.update_style()

    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("QFrame { background-color: #B2C8E6; border-radius: 2px; }")
            self.name_lbl.setStyleSheet("color: #1E3A8A; font-weight: bold; background: transparent;")
        else:
            self.setStyleSheet("QFrame { background-color: transparent; } QFrame:hover { background-color: #D1D5DB; }")
            self.name_lbl.setStyleSheet("color: #374151; background: transparent;")

    def set_selected(self, selected):
        self.is_selected = selected
        self.update_style()

    def toggle_eye(self):
        self.is_visible = not self.is_visible
        self.eye_btn.setText("👁" if self.is_visible else "❌")
        self.visibility_toggled.emit(self.layer_name, self.is_visible)

    def set_visible_state(self, visible):
        self.is_visible = visible
        self.eye_btn.setText("👁" if self.is_visible else "❌")

    def on_checkbox_toggled(self, checked):
        self.check_toggled.emit(self.layer_name, checked)

    def set_checked_state(self, checked):
        self.chk.blockSignals(True)
        self.chk.setChecked(checked)
        self.chk.blockSignals(False)

    def mousePressEvent(self, event):
        self.item_selected.emit(self.layer_name)
        super().mousePressEvent(event)


# -------------------------------------------------------------
# Logo Widget
# -------------------------------------------------------------
class InstantPVCLogo(QWidget):
    def __init__(self, size=40, is_white=True):
        super().__init__()
        self.setFixedSize(size, size)
        self.size_val = size
        self.is_white = is_white

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        center = self.size_val / 2
        radius = center - 3
        points = [
            QPointF(center + radius * math.cos(math.radians(60 * i - 30)),
                    center + radius * math.sin(math.radians(60 * i - 30)))
            for i in range(6)
        ]

        color = QColor("#FFFFFF") if self.is_white else QColor("#6B21A8")
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(QPolygonF(points))

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        s = self.size_val / 70
        painter.drawRoundedRect(22 * s, 22 * s, 26 * s, 18 * s, 2, 2)


# -------------------------------------------------------------
# Card Canvas Box
# -------------------------------------------------------------
class SelectableCardWidget(QWidget):
    clicked = Signal()

    def __init__(self, side_text):
        super().__init__()
        self.setFixedWidth(380)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        header_layout = QHBoxLayout()

        self.side_lbl = QLabel(side_text)
        self.side_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.side_lbl.setStyleSheet("color: #374151; background: transparent;")

        self.layer_lbl = QLabel("")
        self.layer_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.layer_lbl.setStyleSheet("color: #374151; background: transparent;")

        header_layout.addWidget(self.side_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.layer_lbl)

        layout.addLayout(header_layout)

        self.canvas_frame = QFrame()
        self.canvas_frame.setFixedHeight(310)
        self.canvas_frame.setStyleSheet("background-color: #E5E7EB; border: 1px solid #9CA3AF;")

        grid_layout = QGridLayout(self.canvas_frame)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(0)

        corner_box = QWidget()
        corner_box.setFixedSize(20, 20)
        corner_box.setStyleSheet("background-color: #D1D5DB; border-right: 1px solid #9CA3AF; border-bottom: 1px solid #9CA3AF;")
        grid_layout.addWidget(corner_box, 0, 0)

        grid_layout.addWidget(HorizontalRulerWidget(height=20), 0, 1)
        grid_layout.addWidget(VerticalRulerWidget(width=20), 1, 0)

        self.gray_box = QFrame()
        self.gray_box.setStyleSheet("background-color: #6B7280; border: none;")
        
        gray_layout = QVBoxLayout(self.gray_box)
        gray_layout.setContentsMargins(25, 30, 25, 30)

        self.white_card = QFrame()
        self.white_card.setFixedHeight(210)
        self.white_card.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #1F2937;
            border-radius: 12px;
        """)

        gray_layout.addWidget(self.white_card)
        grid_layout.addWidget(self.gray_box, 1, 1)

        layout.addWidget(self.canvas_frame)

    def set_layer_text(self, text):
        self.layer_lbl.setText(text)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


# -------------------------------------------------------------
# Card Designer View with Full Layers Tab Functionality
# -------------------------------------------------------------
class CardDesignerWidget(QWidget):
    def __init__(self, card_name="Credential Design 1", on_close_callback=None):
        super().__init__()
        self.on_close_callback = on_close_callback
        self.layer_widgets = {}

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Header Ribbon
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

        # 2. Toolbar
        toolbar = QFrame()
        toolbar.setFixedHeight(40)
        toolbar.setStyleSheet("background-color: #E5E7EB; border-bottom: 1px solid #D1D5DB;")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(10, 2, 10, 2)
        tb_layout.setSpacing(3)

        tools = [
            "↩", "↪", "📄+", "✂", "📋", "T", "T_i", "👤", "🖼", "📊", "〰", "||||", 
            "💳", "💻", "╱", "⬜", "⭕", "📱", "▦", "🔍+", "🔍-"
        ]
        
        for tool in tools:
            btn = QPushButton(tool)
            btn.setFixedSize(26, 26)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF; border: 1px solid #D1D5DB;
                    border-radius: 2px; font-size: 11px; font-weight: bold; color: #374151;
                }
                QPushButton:hover { background-color: #F3F4F6; border-color: #6B21A8; }
            """)
            tb_layout.addWidget(btn)

        tb_layout.addSpacing(8)
        zoom_combo = QComboBox()
        zoom_combo.addItems(["100%", "75%", "50%", "150%"])
        zoom_combo.setFixedWidth(65)
        zoom_combo.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; font-size: 11px;")
        tb_layout.addWidget(zoom_combo)

        tb_layout.addStretch()
        main_layout.addWidget(toolbar)

        # 3. Main Body
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Scroll Canvas
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setStyleSheet("background-color: #EFEFEF; border: none;")

        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(20, 20, 20, 20)

        cards_outer_layout = QHBoxLayout()
        cards_outer_layout.setSpacing(30)

        self.front_card = SelectableCardWidget("Front Side")
        self.back_card = SelectableCardWidget("Back Side")

        cards_outer_layout.addStretch()
        cards_outer_layout.addWidget(self.front_card)
        cards_outer_layout.addWidget(self.back_card)
        cards_outer_layout.addStretch()

        canvas_layout.addLayout(cards_outer_layout)
        canvas_layout.addStretch()

        canvas_scroll.setWidget(canvas_container)
        body_layout.addWidget(canvas_scroll, stretch=1)

        # Right Panel (Properties & Layers Tab)
        right_panel = QFrame()
        right_panel.setFixedWidth(270)
        right_panel.setStyleSheet("background-color: #E5E7EB; border-left: 1px solid #C0C0C0;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(6, 6, 6, 6)

        self.prop_tabs = QTabWidget()
        self.prop_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #C0C0C0;
                background-color: #E5E7EB;
                top: -1px;
            }
            QTabBar::tab {
                background: #D1D5DB; color: #374151; padding: 6px 20px;
                font-size: 11px; font-weight: bold; border: 1px solid #C0C0C0; margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #FFFFFF; border-bottom: 1px solid #FFFFFF; color: #111827;
            }
        """)

        # --- Properties Tab ---
        properties_page = QWidget()
        properties_page.setStyleSheet("background-color: #E5E7EB;")
        prop_page_layout = QVBoxLayout(properties_page)
        prop_page_layout.setContentsMargins(8, 12, 8, 12)

        prop_box = QFrame()
        prop_box.setStyleSheet("background-color: #DCDCDC; border: 1px solid #C0C0C0;")
        box_layout = QVBoxLayout(prop_box)
        box_layout.setContentsMargins(10, 10, 10, 10)
        box_layout.setSpacing(10)

        self.prop_title = QLabel("- Front Side Properties")
        self.prop_title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.prop_title.setStyleSheet("color: #1F2937; border: none; background: transparent;")
        box_layout.addWidget(self.prop_title)

        box_layout.addWidget(QCheckBox("Rotate print orientation 180 degrees"))
        box_layout.addWidget(QCheckBox("Tactile Impression Module"))

        prop_page_layout.addWidget(prop_box)
        prop_page_layout.addStretch()

        # --- Dynamic Layers Tab ---
        layers_page = QWidget()
        layers_page.setStyleSheet("background-color: #E5E7EB;")
        layers_page_layout = QVBoxLayout(layers_page)
        layers_page_layout.setContentsMargins(8, 12, 8, 12)

        layer_container = QFrame()
        layer_container.setStyleSheet("background-color: #E5E7EB; border: 1px solid #C0C0C0;")
        layer_box_layout = QVBoxLayout(layer_container)
        layer_box_layout.setContentsMargins(6, 8, 6, 8)
        layer_box_layout.setSpacing(2)

        self.layer_header_lbl = QLabel("Front Side")
        self.layer_header_lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.layer_header_lbl.setStyleSheet("color: #1F2937; border: none; background: transparent;")
        layer_box_layout.addWidget(self.layer_header_lbl)

        # Layer List Setup
        layer_data = [
            ("All layers", False, False),
            ("Background", False, False),
            ("Color", True, True),
            ("Black", False, False),
            ("Topcoat", False, True),
            ("Retransfer Material", False, False),
            ("Luster/Fluorescent", False, False),
            ("Non-printable area", False, False),
            ("Lamination", False, False),
            ("Emboss or indent", False, False),
            ("Magnetic stripe", False, False)
        ]

        for name, is_sel, is_chk in layer_data:
            item_w = LayerItemWidget(name, is_selected=is_sel, is_checked=is_chk)
            item_w.item_selected.connect(self.on_layer_selected)
            item_w.visibility_toggled.connect(self.on_layer_visibility_toggled)
            item_w.check_toggled.connect(self.on_layer_check_toggled)
            
            self.layer_widgets[name] = item_w
            layer_box_layout.addWidget(item_w)

        layer_box_layout.addStretch()
        layers_page_layout.addWidget(layer_container)

        self.prop_tabs.addTab(properties_page, "Properties")
        self.prop_tabs.addTab(layers_page, "Layers")

        right_layout.addWidget(self.prop_tabs)
        body_layout.addWidget(right_panel)

        main_layout.addLayout(body_layout, stretch=1)

        # 4. Footer Bar
        footer = QFrame()
        footer.setFixedHeight(36)
        footer.setStyleSheet("background-color: #E5E7EB; border-top: 1px solid #D1D5DB;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 0, 15, 0)
        footer_layout.setSpacing(6)

        btn_style = """
            QPushButton {
                background-color: #2563EB; color: white; font-weight: bold;
                font-size: 11px; border: none; border-radius: 3px; padding: 4px 12px;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(btn_style)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(btn_style)
        if self.on_close_callback:
            close_btn.clicked.connect(self.on_close_callback)

        footer_layout.addWidget(save_btn)
        footer_layout.addWidget(close_btn)
        footer_layout.addStretch()

        main_layout.addWidget(footer)

        self.front_card.clicked.connect(self.select_front_side)
        self.back_card.clicked.connect(self.select_back_side)

        self.select_front_side()

    # Layer Interactivity Slots
    def on_layer_selected(self, selected_layer_name):
        for name, widget in self.layer_widgets.items():
            widget.set_selected(name == selected_layer_name)

        if self.front_card.layer_lbl.text() != "":
            self.front_card.set_layer_text(f"Active Design Layer: {selected_layer_name}")
        elif self.back_card.layer_lbl.text() != "":
            self.back_card.set_layer_text(f"Active Design Layer: {selected_layer_name}")

    def on_layer_visibility_toggled(self, layer_name, visible):
        if layer_name == "All layers":
            for name, widget in self.layer_widgets.items():
                if name != "All layers":
                    widget.set_visible_state(visible)

    def on_layer_check_toggled(self, layer_name, checked):
        if layer_name == "All layers":
            for name, widget in self.layer_widgets.items():
                if name != "All layers":
                    widget.set_checked_state(checked)

    def select_front_side(self):
        self.front_card.set_layer_text("Active Design Layer: Color")
        self.back_card.set_layer_text("")
        self.prop_title.setText("- Front Side Properties")
        self.layer_header_lbl.setText("Front Side")

    def select_back_side(self):
        self.front_card.set_layer_text("")
        self.back_card.set_layer_text("Active Design Layer: Black")
        self.prop_title.setText("- Back Side Properties")
        self.layer_header_lbl.setText("Back Side")


# -------------------------------------------------------------
# Main Dashboard & Login
# -------------------------------------------------------------
class LoginWidget(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4C1D95, stop:1 #2E1065);")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        center_box = QWidget()
        center_box.setFixedWidth(420)
        box_layout = QVBoxLayout(center_box)
        box_layout.setSpacing(15)

        box_layout.addWidget(InstantPVCLogo(size=70, is_white=True), 0, Qt.AlignCenter)

        title_lbl = QLabel("INSTANT PVC")
        title_lbl.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; letter-spacing: 2px;")
        title_lbl.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(title_lbl)

        form_card = QFrame()
        form_card.setStyleSheet("""
            QFrame { background-color: #FFFFFF; border-radius: 8px; }
            QLabel { color: #4B5563; font-size: 13px; font-weight: 600; }
            QLineEdit {
                background-color: #F9FAFB; border: 1px solid #D1D5DB;
                border-radius: 6px; padding: 8px 10px; font-size: 13px; color: #111827;
            }
        """)
        
        card_layout = QVBoxLayout(form_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(10)

        card_layout.addWidget(QLabel("User ID"))
        self.user_entry = QLineEdit("admin")
        self.user_entry.setFixedHeight(38)
        card_layout.addWidget(self.user_entry)

        card_layout.addWidget(QLabel("Password"))
        self.pass_entry = QLineEdit("admin123")
        self.pass_entry.setEchoMode(QLineEdit.Password)
        self.pass_entry.setFixedHeight(38)
        card_layout.addWidget(self.pass_entry)

        box_layout.addWidget(form_card)

        login_btn = QPushButton("Sign In")
        login_btn.setFixedSize(120, 38)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("QPushButton { background-color: #2563EB; color: white; font-weight: bold; font-size: 14px; border: none; border-radius: 4px; }")
        login_btn.clicked.connect(self.check_login)
        box_layout.addWidget(login_btn, 0, Qt.AlignCenter)

        main_layout.addWidget(center_box)

    def check_login(self):
        if self.user_entry.text().strip() == "admin" and self.pass_entry.text().strip() == "admin123":
            self.on_login_success("admin")
        else:
            QMessageBox.critical(self, "Login Failed", "User ID သို့မဟုတ် Password မှားယွင်းနေပါသည်။")


class MainDashboardWidget(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        nav_bar = QFrame()
        nav_bar.setFixedHeight(45)
        nav_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(15, 0, 15, 0)

        brand_box = QHBoxLayout()
        brand_box.setSpacing(8)
        brand_box.addWidget(InstantPVCLogo(size=28, is_white=False))
        
        brand_title = QLabel("ENTRUST")
        brand_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        brand_title.setStyleSheet("color: #4C1D95;")
        brand_box.addWidget(brand_title)

        sub_brand = QLabel("Adaptive Issuance Instant ID")
        sub_brand.setFont(QFont("Segoe UI", 9))
        sub_brand.setStyleSheet("color: #6B21A8; padding-left: 5px; border-left: 1px solid #D1D5DB;")
        brand_box.addWidget(sub_brand)

        nav_layout.addLayout(brand_box)
        nav_layout.addStretch()

        self.design_btn = QPushButton("Design")
        self.design_btn.setStyleSheet("QPushButton { color: #6B21A8; font-weight: bold; background: transparent; border: none; }")
        self.design_btn.clicked.connect(self.open_create_card_flow)
        nav_layout.addWidget(self.design_btn)

        main_layout.addWidget(nav_bar)

        self.main_stack = QStackedWidget()
        self.dashboard_view = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_view)
        
        create_card_btn = QPushButton("+ Create Card Design")
        create_card_btn.setFixedSize(160, 40)
        create_card_btn.setStyleSheet("background-color: #2563EB; color: white; font-weight: bold; border-radius: 4px;")
        create_card_btn.clicked.connect(self.open_create_card_flow)
        dash_layout.addWidget(create_card_btn, 0, Qt.AlignCenter)

        self.main_stack.addWidget(self.dashboard_view)
        main_layout.addWidget(self.main_stack)

    def open_create_card_flow(self):
        designer_view = CardDesignerWidget(card_name="Credential Design 1", on_close_callback=self.close_designer_view)
        self.main_stack.addWidget(designer_view)
        self.main_stack.setCurrentWidget(designer_view)

    def close_designer_view(self):
        self.main_stack.setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance - Instant PVC")
        self.resize(1150, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_widget = LoginWidget(self.show_dashboard)
        self.stack.addWidget(self.login_widget)

    def show_dashboard(self, username):
        self.dashboard_widget = MainDashboardWidget(username)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.setCurrentWidget(self.dashboard_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
