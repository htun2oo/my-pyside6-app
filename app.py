import sys
import math
from PySide6.QtCore import Qt, QPointF, QSize
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QStackedWidget,
    QDialog, QComboBox, QDoubleSpinBox, QRadioButton, QButtonGroup, QGridLayout,
    QTabWidget, QCheckBox, QScrollArea
)

# -------------------------------------------------------------
# Instant PVC Vector Logo
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
# Card Canvas Box (Front Side / Back Side Card Representation)
# -------------------------------------------------------------
class CardCanvasWidget(QFrame):
    def __init__(self, title_text):
        super().__init__()
        self.setStyleSheet("background-color: #A3A3A3; border-radius: 4px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 20)

        # Title Label (Front Side / Back Side)
        lbl = QLabel(title_text)
        lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        lbl.setStyleSheet("color: #374151; background: transparent;")
        layout.addWidget(lbl)

        # Inner Card White Area (CR80 Aspect Ratio)
        card_white_box = QFrame()
        card_white_box.setFixedSize(280, 175)  # CR80 Proportional Size
        card_white_box.setStyleSheet("""
            background-color: #FFFFFF;
            border: 2px solid #525252;
            border-radius: 12px;
        """)
        
        layout.addWidget(card_white_box, 0, Qt.AlignCenter)
        layout.addStretch()


# -------------------------------------------------------------
# Card Designer View (Image ပါအတိုင်း Design လုပ်သည့် Canvas)
# -------------------------------------------------------------
class CardDesignerWidget(QWidget):
    def __init__(self, card_name="Credential Design 1", on_close_callback=None):
        super().__init__()
        self.on_close_callback = on_close_callback

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Purple Header Ribbon
        purple_ribbon = QFrame()
        purple_ribbon.setFixedHeight(40)
        purple_ribbon.setStyleSheet("background-color: #6B21A8;")
        purple_layout = QHBoxLayout(purple_ribbon)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        title_lbl = QLabel(f"{card_name} ✏")
        title_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF;")
        purple_layout.addWidget(title_lbl)
        purple_layout.addStretch()

        main_layout.addWidget(purple_ribbon)

        # 2. Designer Toolbar (Icons Bar)
        toolbar = QFrame()
        toolbar.setFixedHeight(45)
        toolbar.setStyleSheet("background-color: #E5E7EB; border-bottom: 1px solid #D1D5DB;")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(10, 4, 10, 4)
        tb_layout.setSpacing(4)

        tools = ["↩", "↪", "✂", "📋", "🔤", "🖼", "📊", "⎯", "⬜", "⭕", "▦", "🔍+", "🔍-"]
        for tool in tools:
            btn = QPushButton(tool)
            btn.setFixedSize(32, 32)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    border: 1px solid #C0C0C0;
                    border-radius: 3px;
                    font-size: 14px;
                    font-weight: bold;
                    color: #374151;
                }
                QPushButton:hover {
                    background-color: #F3F4F6;
                    border-color: #7C3AED;
                }
            """)
            tb_layout.addWidget(btn)

        tb_layout.addSpacing(15)
        zoom_lbl = QLabel("Zoom:")
        zoom_lbl.setStyleSheet("color: #374151; font-weight: bold;")
        tb_layout.addWidget(zoom_lbl)

        zoom_combo = QComboBox()
        zoom_combo.addItems(["100%", "75%", "50%", "150%", "200%"])
        zoom_combo.setFixedWidth(75)
        zoom_combo.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; padding: 2px;")
        tb_layout.addWidget(zoom_combo)

        tb_layout.addStretch()

        main_layout.addWidget(toolbar)

        # 3. Canvas & Right Properties Area
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Middle Canvas Area (Gray Background)
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setStyleSheet("background-color: #D4D4D4; border: none;")

        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(20, 15, 20, 15)

        # Active Layer Status
        active_layer_lbl = QLabel("Active Design Layer: Color")
        active_layer_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        active_layer_lbl.setStyleSheet("color: #374151;")
        active_layer_lbl.setAlignment(Qt.AlignCenter)
        canvas_layout.addWidget(active_layer_lbl)

        # Cards Side-by-Side (Front Side & Back Side)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)

        self.front_card = CardCanvasWidget("Front Side")
        self.back_card = CardCanvasWidget("Back Side")

        cards_layout.addWidget(self.front_card)
        cards_layout.addWidget(self.back_card)

        canvas_layout.addLayout(cards_layout)
        canvas_layout.addStretch()

        canvas_scroll.setWidget(canvas_container)
        body_layout.addWidget(canvas_scroll, stretch=1)

        # Right Properties Panel
        right_panel = QFrame()
        right_panel.setFixedWidth(260)
        right_panel.setStyleSheet("background-color: #F9FAFB; border-left: 1px solid #D1D5DB;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        prop_tabs = QTabWidget()
        prop_tabs.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background: #E5E7EB;
                color: #374151;
                padding: 8px 16px;
                font-weight: bold;
                border: 1px solid #D1D5DB;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                border-bottom: 2px solid #7C3AED;
            }
        """)

        # Tab 1: Properties
        properties_page = QWidget()
        prop_page_layout = QVBoxLayout(properties_page)
        prop_page_layout.setContentsMargins(15, 15, 15, 15)

        prop_title = QLabel("— Front Side Properties")
        prop_title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        prop_title.setStyleSheet("color: #374151;")
        prop_page_layout.addWidget(prop_title)

        chk1 = QCheckBox("Hopper print orientation 180 degrees")
        chk1.setStyleSheet("color: #4B5563; font-size: 11px;")
        prop_page_layout.addWidget(chk1)

        chk2 = QCheckBox("Tactile Impression Module")
        chk2.setStyleSheet("color: #4B5563; font-size: 11px;")
        prop_page_layout.addWidget(chk2)

        prop_page_layout.addStretch()

        # Tab 2: Layers
        layers_page = QWidget()
        layers_layout = QVBoxLayout(layers_page)
        layers_layout.addWidget(QLabel("Layer 1: Color\nLayer 2: Overlay", alignment=Qt.AlignTop))

        prop_tabs.addTab(properties_page, "Properties")
        prop_tabs.addTab(layers_page, "Layers")

        right_layout.addWidget(prop_tabs)
        body_layout.addWidget(right_panel)

        main_layout.addLayout(body_layout, stretch=1)

        # 4. Bottom Footer Action Buttons
        footer = QFrame()
        footer.setFixedHeight(45)
        footer.setStyleSheet("background-color: #E5E7EB; border-top: 1px solid #D1D5DB;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 0, 15, 0)
        footer_layout.setSpacing(10)

        btn_style = """
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-radius: 3px;
                padding: 6px 16px;
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
        close_btn.setEnabled(False)
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


# -------------------------------------------------------------
# Create New Card Dialog (Pop-up Window)
# -------------------------------------------------------------
class CreateCardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Card Template")
        self.setFixedSize(480, 380)
        self.setStyleSheet("""
            QDialog { background-color: #FFFFFF; }
            QLabel { color: #374151; font-size: 13px; font-weight: 600; }
            QLineEdit, QComboBox, QDoubleSpinBox {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                color: #111827;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header_lbl = QLabel("New Card Template")
        header_lbl.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_lbl.setStyleSheet("color: #4C1D95;")
        layout.addWidget(header_lbl)

        form_grid = QGridLayout()
        form_grid.setSpacing(12)

        form_grid.addWidget(QLabel("Card Name:"), 0, 0)
        self.card_name_input = QLineEdit()
        self.card_name_input.setText("Credential Design 1")
        form_grid.addWidget(self.card_name_input, 0, 1)

        form_grid.addWidget(QLabel("Preset Size:"), 1, 0)
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["CR80 Standard ID Card (85.60 x 53.98 mm)"])
        form_grid.addWidget(self.preset_combo, 1, 1)

        layout.addLayout(form_grid)
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(90, 36)
        cancel_btn.setStyleSheet("background-color: #E5E7EB; color: #374151; font-weight: 600; border: none; border-radius: 6px;")
        cancel_btn.clicked.connect(self.reject)

        create_btn = QPushButton("Create")
        create_btn.setFixedSize(110, 36)
        create_btn.setStyleSheet("background-color: #6B21A8; color: white; font-weight: bold; border: none; border-radius: 6px;")
        create_btn.clicked.connect(self.accept)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(create_btn)
        layout.addLayout(btn_layout)

    def get_card_name(self):
        return self.card_name_input.text().strip() or "Credential Design 1"


# -------------------------------------------------------------
# Login Window
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
        self.user_entry = QLineEdit()
        self.user_entry.setFixedHeight(38)
        card_layout.addWidget(self.user_entry)

        card_layout.addWidget(QLabel("Password"))
        self.pass_entry = QLineEdit()
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
            QMessageBox.critical(self, "Login Failed", "User ID သို့မဟုတ် Password မှားယွင်းနေပါသည်။\n(Default: admin / admin123)")


# -------------------------------------------------------------
# Main Dashboard Widget
# -------------------------------------------------------------
class MainDashboardWidget(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Navigation Bar
        nav_bar = QFrame()
        nav_bar.setFixedHeight(50)
        nav_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 0, 20, 0)

        brand_box = QHBoxLayout()
        brand_box.setSpacing(8)
        brand_box.addWidget(InstantPVCLogo(size=32, is_white=False))
        
        brand_title = QLabel("ENTRUST")
        brand_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        brand_title.setStyleSheet("color: #4C1D95;")
        brand_box.addWidget(brand_title)

        sub_brand = QLabel("Adaptive Issuance Instant ID")
        sub_brand.setFont(QFont("Segoe UI", 9))
        sub_brand.setStyleSheet("color: #6B7280; padding-left: 5px; border-left: 1px solid #D1D5DB;")
        brand_box.addWidget(sub_brand)

        nav_layout.addLayout(brand_box)
        nav_layout.addSpacing(25)

        nav_btn_style = "QPushButton { background: transparent; border: none; color: #374151; font-size: 13px; font-weight: 600; padding: 14px 16px; } QPushButton:hover { color: #6B21A8; }"

        self.home_btn = QPushButton("Home")
        self.home_btn.setStyleSheet(nav_btn_style)
        self.home_btn.clicked.connect(self.show_home_view)

        self.design_btn = QPushButton("Design")
        self.design_btn.setStyleSheet(nav_btn_style)
        self.design_btn.clicked.connect(self.show_design_view)

        self.printer_btn = QPushButton("Printer Queues")
        self.printer_btn.setStyleSheet(nav_btn_style)

        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.design_btn)
        nav_layout.addWidget(self.printer_btn)
        nav_layout.addStretch()

        main_layout.addWidget(nav_bar)

        # 2. Main Stack Container
        self.main_stack = QStackedWidget()

        # Dashboard View Area (With Tabs)
        self.dashboard_view = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_view)
        dash_layout.setContentsMargins(0, 0, 0, 0)
        dash_layout.setSpacing(0)

        # Purple Ribbon Bar
        purple_bar = QFrame()
        purple_bar.setFixedHeight(42)
        purple_bar.setStyleSheet("background-color: #6B21A8;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(20, 0, 20, 0)

        self.purple_tab_stack = QStackedWidget()

        home_tabs_bar = QFrame()
        home_tabs_layout = QHBoxLayout(home_tabs_bar)
        home_tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.cred_tab_btn = QPushButton("Credentials")
        self.logs_tab_btn = QPushButton("System Logs")

        design_tabs_bar = QFrame()
        design_tabs_layout = QHBoxLayout(design_tabs_bar)
        design_tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_tab_btn = QPushButton("Cards")
        self.workflows_tab_btn = QPushButton("Workflows")

        purple_tab_style = "QPushButton { background-color: #7C3AED; color: #EDE9FE; border: none; border-top-left-radius: 4px; border-top-right-radius: 4px; padding: 6px 16px; font-weight: bold; font-size: 12px; }"
        for btn in [self.cred_tab_btn, self.logs_tab_btn, self.cards_tab_btn, self.workflows_tab_btn]:
            btn.setStyleSheet(purple_tab_style)

        home_tabs_layout.addWidget(self.cred_tab_btn)
        home_tabs_layout.addWidget(self.logs_tab_btn)
        home_tabs_layout.addStretch()

        design_tabs_layout.addWidget(self.cards_tab_btn)
        design_tabs_layout.addWidget(self.workflows_tab_btn)
        design_tabs_layout.addStretch()

        self.purple_tab_stack.addWidget(home_tabs_bar)
        self.purple_tab_stack.addWidget(design_tabs_bar)

        purple_layout.addWidget(self.purple_tab_stack)
        dash_layout.addWidget(purple_bar)

        # Content Pages
        self.content_stack = QStackedWidget()

        cards_page = QWidget()
        cards_layout = QVBoxLayout(cards_page)
        cards_layout.setContentsMargins(20, 20, 20, 20)

        cards_action_bar = QHBoxLayout()
        cards_title = QLabel("Card Templates")
        cards_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        cards_action_bar.addWidget(cards_title)
        cards_action_bar.addStretch()

        create_card_btn = QPushButton("+ Create Card")
        create_card_btn.setFixedSize(130, 36)
        create_card_btn.setCursor(Qt.PointingHandCursor)
        create_card_btn.setStyleSheet("QPushButton { background-color: #2563EB; color: white; font-weight: bold; border-none; border-radius: 6px; }")
        create_card_btn.clicked.connect(self.open_create_card_flow)
        cards_action_bar.addWidget(create_card_btn)

        cards_layout.addLayout(cards_action_bar)
        cards_layout.addStretch()

        self.content_stack.addWidget(cards_page)
        dash_layout.addWidget(self.content_stack)

        self.main_stack.addWidget(self.dashboard_view) # Index 0: Standard Dashboard

        main_layout.addWidget(self.main_stack)

        self.show_home_view()

    def open_create_card_flow(self):
        dialog = CreateCardDialog(self)
        if dialog.exec() == QDialog.Accepted:
            card_name = dialog.get_card_name()
            # Open Designer Canvas View
            designer_view = CardDesignerWidget(card_name=card_name, on_close_callback=self.close_designer_view)
            self.main_stack.addWidget(designer_view)
            self.main_stack.setCurrentWidget(designer_view)

    def close_designer_view(self):
        self.main_stack.setCurrentIndex(0)

    def show_home_view(self):
        self.purple_tab_stack.setCurrentIndex(0)

    def show_design_view(self):
        self.purple_tab_stack.setCurrentIndex(1)


# -------------------------------------------------------------
# Main Window Controller
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance - Instant PVC")
        self.resize(1200, 750)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.show_login()

    def show_login(self):
        self.login_widget = LoginWidget(self.show_dashboard)
        self.stack.addWidget(self.login_widget)
        self.stack.setCurrentWidget(self.login_widget)

    def show_dashboard(self, username):
        self.dashboard_widget = MainDashboardWidget(username)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.setCurrentWidget(self.dashboard_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
