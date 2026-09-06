import sys
import math
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QStackedWidget
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

        subtitle_lbl = QLabel("Card Issuance Suite")
        subtitle_lbl.setFont(QFont("Segoe UI", 11))
        subtitle_lbl.setStyleSheet("color: #DDD6FE; margin-bottom: 5px;")
        subtitle_lbl.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(subtitle_lbl)

        form_card = QFrame()
        form_card.setStyleSheet("""
            QFrame { background-color: #FFFFFF; border-radius: 8px; }
            QLabel { color: #4B5563; font-size: 13px; font-weight: 600; }
            QLineEdit {
                background-color: #F9FAFB; border: 1px solid #D1D5DB;
                border-radius: 6px; padding: 8px 10px; font-size: 13px; color: #111827;
            }
            QLineEdit:focus { border: 2px solid #7C3AED; background-color: #FFFFFF; }
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

        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.setStyleSheet("background: transparent; color: #E9D5FF; font-size: 12px; border: none;")
        box_layout.addWidget(forgot_btn, 0, Qt.AlignCenter)

        login_btn = QPushButton("Sign In")
        login_btn.setFixedSize(120, 38)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton { background-color: #2563EB; color: white; font-weight: bold; font-size: 14px; border: none; border-radius: 4px; }
            QPushButton:hover { background-color: #1D4ED8; }
        """)
        login_btn.clicked.connect(self.check_login)
        box_layout.addWidget(login_btn, 0, Qt.AlignCenter)

        main_layout.addWidget(center_box)

    def check_login(self):
        if self.user_entry.text().strip() == "admin" and self.pass_entry.text().strip() == "admin123":
            self.on_login_success("admin")
        else:
            QMessageBox.critical(self, "Login Failed", "User ID သို့မဟုတ် Password မှားယွင်းနေပါသည်။\n(Default: admin / admin123)")


# -------------------------------------------------------------
# Main Application Dashboard
# -------------------------------------------------------------
class MainDashboardWidget(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Navigation Bar (White Area)
        nav_bar = QFrame()
        nav_bar.setFixedHeight(50)
        nav_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 0, 20, 0)

        brand_box = QHBoxLayout()
        brand_box.setSpacing(8)
        brand_box.addWidget(InstantPVCLogo(size=32, is_white=False))
        
        brand_title = QLabel("INSTANT PVC")
        brand_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        brand_title.setStyleSheet("color: #4C1D95;")
        brand_box.addWidget(brand_title)

        sub_brand = QLabel("Card Issuance")
        sub_brand.setFont(QFont("Segoe UI", 9))
        sub_brand.setStyleSheet("color: #6B7280; padding-left: 5px; border-left: 1px solid #D1D5DB;")
        brand_box.addWidget(sub_brand)

        nav_layout.addLayout(brand_box)
        nav_layout.addSpacing(25)

        nav_btn_style = """
            QPushButton { 
                background: transparent; 
                border: none; 
                color: #374151; 
                font-size: 13px; 
                font-weight: 600; 
                padding: 14px 16px;
                border-bottom: 2px solid transparent;
            } 
            QPushButton:hover { 
                color: #6B21A8; 
            }
        """

        self.home_btn = QPushButton("Home")
        self.home_btn.setCursor(Qt.PointingHandCursor)
        self.home_btn.setStyleSheet(nav_btn_style)
        self.home_btn.clicked.connect(self.show_home_view)

        self.design_btn = QPushButton("Design")
        self.design_btn.setCursor(Qt.PointingHandCursor)
        self.design_btn.setStyleSheet(nav_btn_style)
        self.design_btn.clicked.connect(self.show_design_view)

        self.printer_btn = QPushButton("Printer Queues")
        self.printer_btn.setCursor(Qt.PointingHandCursor)
        self.printer_btn.setStyleSheet(nav_btn_style)

        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.design_btn)
        nav_layout.addWidget(self.printer_btn)
        nav_layout.addStretch()

        main_layout.addWidget(nav_bar)

        # 2. Purple Ribbon Bar (ခရမ်းရောင်တန်း)
        purple_bar = QFrame()
        purple_bar.setFixedHeight(42)
        purple_bar.setStyleSheet("background-color: #6B21A8;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(20, 0, 20, 0)
        purple_layout.setSpacing(10)

        # Purple Tabs (Home & Design Sub-tabs)
        self.purple_tab_stack = QStackedWidget()

        # Home Sub-tabs (Credentials, System Logs)
        home_tabs_bar = QFrame()
        home_tabs_layout = QHBoxLayout(home_tabs_bar)
        home_tabs_layout.setContentsMargins(0, 0, 0, 0)
        home_tabs_layout.setSpacing(4)

        self.cred_tab_btn = QPushButton("Credentials")
        self.logs_tab_btn = QPushButton("System Logs")

        # Design Sub-tabs (Cards, Workflows, Reports, Field Connections)
        design_tabs_bar = QFrame()
        design_tabs_layout = QHBoxLayout(design_tabs_bar)
        design_tabs_layout.setContentsMargins(0, 0, 0, 0)
        design_tabs_layout.setSpacing(4)

        self.cards_tab_btn = QPushButton("Cards")
        self.workflows_tab_btn = QPushButton("Workflows")
        self.reports_tab_btn = QPushButton("Reports")
        self.field_conn_tab_btn = QPushButton("Field Connections")

        # Style Sub-Tabs on Purple Bar
        purple_tab_style = """
            QPushButton {
                background-color: #7C3AED;
                color: #EDE9FE;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8B5CF6;
                color: #FFFFFF;
            }
        """
        for btn in [self.cred_tab_btn, self.logs_tab_btn, self.cards_tab_btn, self.workflows_tab_btn, self.reports_tab_btn, self.field_conn_tab_btn]:
            btn.setStyleSheet(purple_tab_style)
            btn.setCursor(Qt.PointingHandCursor)

        home_tabs_layout.addWidget(self.cred_tab_btn)
        home_tabs_layout.addWidget(self.logs_tab_btn)
        home_tabs_layout.addStretch()

        design_tabs_layout.addWidget(self.cards_tab_btn)
        design_tabs_layout.addWidget(self.workflows_tab_btn)
        design_tabs_layout.addWidget(self.reports_tab_btn)
        design_tabs_layout.addWidget(self.field_conn_tab_btn)
        design_tabs_layout.addStretch()

        self.purple_tab_stack.addWidget(home_tabs_bar)    # Index 0
        self.purple_tab_stack.addWidget(design_tabs_bar)  # Index 1

        purple_layout.addWidget(self.purple_tab_stack)
        purple_layout.addStretch()

        # (ညာဘက်ခြမ်းမှ admin, notification နှင့် logout ခလုပ်များကို ဖျက်ထားပါသည်)

        main_layout.addWidget(purple_bar)

        # 3. Content Body
        self.content_stack = QStackedWidget()

        # --- A. HOME PAGES ---
        self.home_content_stack = QStackedWidget()

        # 1. Credentials Content Page
        cred_page = QWidget()
        cred_layout = QVBoxLayout(cred_page)
        cred_layout.setContentsMargins(20, 15, 20, 15)

        toolbar_layout = QHBoxLayout()
        grid_btn = QPushButton("田")
        grid_btn.setFixedSize(32, 32)
        grid_btn.setStyleSheet("background-color: #E2E8F0; border: 1px solid #CBD5E1; border-radius: 3px; font-size: 16px;")
        list_btn = QPushButton("≡")
        list_btn.setFixedSize(32, 32)
        list_btn.setStyleSheet("background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 3px; font-size: 16px;")
        toolbar_layout.addWidget(grid_btn)
        toolbar_layout.addWidget(list_btn)
        toolbar_layout.addStretch()

        cred_layout.addLayout(toolbar_layout)

        empty_box = QLabel("No credentials available. Click 'Design' in top menu to manage templates.")
        empty_box.setAlignment(Qt.AlignCenter)
        empty_box.setStyleSheet("color: #9CA3AF; font-size: 14px; margin-top: 80px;")
        cred_layout.addWidget(empty_box)
        cred_layout.addStretch()

        # 2. System Logs Content Page
        logs_page = QWidget()
        logs_layout = QVBoxLayout(logs_page)
        logs_layout.addWidget(QLabel("System Logs Dashboard", alignment=Qt.AlignCenter))

        self.home_content_stack.addWidget(cred_page) # Index 0
        self.home_content_stack.addWidget(logs_page) # Index 1

        # --- B. DESIGN PAGES ---
        self.design_content_stack = QStackedWidget()

        cards_page = QWidget()
        cards_layout = QVBoxLayout(cards_page)
        cards_layout.addWidget(QLabel("Cards Design Canvas Area", alignment=Qt.AlignCenter))

        workflows_page = QWidget()
        workflows_layout = QVBoxLayout(workflows_page)
        workflows_layout.addWidget(QLabel("Workflows & Issuance Rules Manager", alignment=Qt.AlignCenter))

        reports_page = QWidget()
        reports_layout = QVBoxLayout(reports_page)
        reports_layout.addWidget(QLabel("Reports Template Generator", alignment=Qt.AlignCenter))

        field_conn_page = QWidget()
        field_conn_layout = QVBoxLayout(field_conn_page)
        field_conn_layout.addWidget(QLabel("Database & Field Connections Mapping Workspace", alignment=Qt.AlignCenter))

        self.design_content_stack.addWidget(cards_page)      # Index 0
        self.design_content_stack.addWidget(workflows_page)  # Index 1
        self.design_content_stack.addWidget(reports_page)    # Index 2
        self.design_content_stack.addWidget(field_conn_page) # Index 3

        # Add Stack Pages
        self.content_stack.addWidget(self.home_content_stack)   # Index 0
        self.content_stack.addWidget(self.design_content_stack) # Index 1

        main_layout.addWidget(self.content_stack)

        # Tab Button Connections
        self.cred_tab_btn.clicked.connect(lambda: self.switch_home_tab(0, self.cred_tab_btn))
        self.logs_tab_btn.clicked.connect(lambda: self.switch_home_tab(1, self.logs_tab_btn))

        self.cards_tab_btn.clicked.connect(lambda: self.switch_design_tab(0, self.cards_tab_btn))
        self.workflows_tab_btn.clicked.connect(lambda: self.switch_design_tab(1, self.workflows_tab_btn))
        self.reports_tab_btn.clicked.connect(lambda: self.switch_design_tab(2, self.reports_tab_btn))
        self.field_conn_tab_btn.clicked.connect(lambda: self.switch_design_tab(3, self.field_conn_tab_btn))

        # Show Home View by Default
        self.show_home_view()

    def update_purple_tab_active(self, active_btn, btn_group):
        active_style = """
            QPushButton {
                background-color: #FFFFFF;
                color: #6B21A8;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 12px;
            }
        """
        normal_style = """
            QPushButton {
                background-color: #7C3AED;
                color: #EDE9FE;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8B5CF6;
                color: #FFFFFF;
            }
        """
        for btn in btn_group:
            btn.setStyleSheet(active_style if btn == active_btn else normal_style)

    def switch_home_tab(self, index, btn):
        self.home_content_stack.setCurrentIndex(index)
        self.update_purple_tab_active(btn, [self.cred_tab_btn, self.logs_tab_btn])

    def switch_design_tab(self, index, btn):
        self.design_content_stack.setCurrentIndex(index)
        self.update_purple_tab_active(btn, [self.cards_tab_btn, self.workflows_tab_btn, self.reports_tab_btn, self.field_conn_tab_btn])

    def set_nav_active(self, active_btn):
        active_style = "QPushButton { color: #6B21A8; border-bottom: 2px solid #6B21A8; font-weight: bold; padding: 14px 16px; background: transparent; }"
        normal_style = "QPushButton { color: #374151; border-bottom: 2px solid transparent; font-weight: 600; padding: 14px 16px; background: transparent; } QPushButton:hover { color: #6B21A8; }"

        self.home_btn.setStyleSheet(active_style if active_btn == "home" else normal_style)
        self.design_btn.setStyleSheet(active_style if active_btn == "design" else normal_style)
        self.printer_btn.setStyleSheet(normal_style)

    def show_home_view(self):
        self.set_nav_active("home")
        self.purple_tab_stack.setCurrentIndex(0)
        self.content_stack.setCurrentIndex(0)
        self.switch_home_tab(0, self.cred_tab_btn)

    def show_design_view(self):
        self.set_nav_active("design")
        self.purple_tab_stack.setCurrentIndex(1)
        self.content_stack.setCurrentIndex(1)
        self.switch_design_tab(0, self.cards_tab_btn)


# -------------------------------------------------------------
# Main Application Controller
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instant PVC")
        self.resize(1200, 720)

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
