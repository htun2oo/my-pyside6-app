import sys
import math
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QTabWidget,
    QStackedWidget
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
# Main Dashboard Window
# -------------------------------------------------------------
class DashboardWidget(QWidget):
    def __init__(self, username, on_logout, on_open_tab):
        super().__init__()
        self.username = username
        self.on_logout = on_logout
        self.on_open_tab = on_open_tab

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Navigation Bar (With Direct Tabs)
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
                padding: 6px 12px; 
            } 
            QPushButton:hover { 
                color: #6B21A8; 
                background-color: #F3E8FF;
                border-radius: 4px;
            }
        """

        # Direct Tabs
        home_btn = QPushButton("Home")
        home_btn.setStyleSheet(nav_btn_style + "QPushButton { color: #6B21A8; border-bottom: 2px solid #6B21A8; border-radius: 0px; }")

        cards_btn = QPushButton("Cards")
        cards_btn.setStyleSheet(nav_btn_style)
        cards_btn.clicked.connect(lambda: self.on_open_tab(0))

        workflows_btn = QPushButton("Workflows")
        workflows_btn.setStyleSheet(nav_btn_style)
        workflows_btn.clicked.connect(lambda: self.on_open_tab(1))

        reports_btn = QPushButton("Reports")
        reports_btn.setStyleSheet(nav_btn_style)
        reports_btn.clicked.connect(lambda: self.on_open_tab(2))

        field_conn_btn = QPushButton("Field Connections")
        field_conn_btn.setStyleSheet(nav_btn_style)
        field_conn_btn.clicked.connect(lambda: self.on_open_tab(3))

        printer_btn = QPushButton("Printer Queues")
        printer_btn.setStyleSheet(nav_btn_style)

        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(cards_btn)
        nav_layout.addWidget(workflows_btn)
        nav_layout.addWidget(reports_btn)
        nav_layout.addWidget(field_conn_btn)
        nav_layout.addWidget(printer_btn)
        nav_layout.addStretch()

        main_layout.addWidget(nav_bar)

        # 2. Purple User Info Bar
        purple_bar = QFrame()
        purple_bar.setFixedHeight(35)
        purple_bar.setStyleSheet("background-color: #6B21A8;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(20, 0, 20, 0)

        login_info = QLabel("Last Login at Sun Sep 06 13:00:15 MMT 2026 from 127.0.0.1")
        login_info.setStyleSheet("color: #E9D5FF; font-size: 11px;")
        purple_layout.addWidget(login_info)
        purple_layout.addStretch()

        user_lbl = QLabel(f"{self.username}")
        user_lbl.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold;")

        notif_btn = QPushButton("🔔 2")
        notif_btn.setStyleSheet("background-color: #EF4444; color: white; border-radius: 10px; font-size: 10px; font-weight: bold; padding: 2px 6px; border: none;")

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("background: transparent; color: #FCA5A5; font-size: 11px; border: none; font-weight: bold;")
        logout_btn.clicked.connect(self.on_logout)

        purple_layout.addWidget(user_lbl)
        purple_layout.addWidget(notif_btn)
        purple_layout.addWidget(logout_btn)

        main_layout.addWidget(purple_bar)

        # 3. Main Home Content Area
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #F9FAFB;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 15, 20, 15)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #E5E7EB; background-color: #FFFFFF; top: -1px; }
            QTabBar::tab { background-color: #E5E7EB; color: #4B5563; font-weight: bold; padding: 8px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 4px; }
            QTabBar::tab:selected { background-color: #FFFFFF; color: #1F2937; border-top: 3px solid #6B21A8; }
        """)

        # Credentials Sub-Tab
        cred_tab = QWidget()
        cred_layout = QVBoxLayout(cred_tab)
        cred_layout.setContentsMargins(15, 15, 15, 15)

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

        empty_box = QLabel("No credentials available. Select Cards, Workflows, Reports or Field Connections from top menu.")
        empty_box.setAlignment(Qt.AlignCenter)
        empty_box.setStyleSheet("color: #9CA3AF; font-size: 14px; margin-top: 80px;")
        cred_layout.addWidget(empty_box)
        cred_layout.addStretch()

        # System Reports Sub-Tab
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        reports_layout.addWidget(QLabel("Reports Dashboard", alignment=Qt.AlignCenter))

        tabs.addTab(cred_tab, "Credentials")
        tabs.addTab(reports_tab, "System Logs")

        content_layout.addWidget(tabs)
        main_layout.addWidget(content_area)


# -------------------------------------------------------------
# Main Design & Configuration Workspace (Tabs)
# -------------------------------------------------------------
class DesignWorkspaceWidget(QWidget):
    def __init__(self, on_close, initial_tab=0):
        super().__init__()
        self.on_close = on_close
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Banner
        ribbon = QFrame()
        ribbon.setFixedHeight(50)
        ribbon.setStyleSheet("background-color: #6B21A8;")
        ribbon_layout = QHBoxLayout(ribbon)
        ribbon_layout.setContentsMargins(15, 0, 15, 0)

        title_lbl = QLabel("Design & Management Workspace")
        title_lbl.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        ribbon_layout.addWidget(title_lbl)
        ribbon_layout.addStretch()

        back_btn = QPushButton("Back to Home")
        back_btn.setStyleSheet("background-color: #581C87; color: white; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold;")
        back_btn.clicked.connect(self.on_close)
        ribbon_layout.addWidget(back_btn)

        main_layout.addWidget(ribbon)

        # Tab Views for Cards, Workflows, Reports, Field Connections
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background-color: #F9FAFB; }
            QTabBar::tab { background-color: #E5E7EB; color: #4B5563; font-weight: bold; padding: 12px 28px; margin-right: 2px; font-size: 13px; }
            QTabBar::tab:selected { background-color: #FFFFFF; color: #6B21A8; border-bottom: 3px solid #6B21A8; }
        """)

        # 1. Cards
        cards_widget = QWidget()
        cards_layout = QVBoxLayout(cards_widget)
        cards_layout.addWidget(QLabel("Cards Canvas & ID Design Area", alignment=Qt.AlignCenter))
        
        # 2. Workflows
        workflows_widget = QWidget()
        workflows_layout = QVBoxLayout(workflows_widget)
        workflows_layout.addWidget(QLabel("Workflows & Issuance Process Configuration", alignment=Qt.AlignCenter))

        # 3. Reports
        reports_widget = QWidget()
        reports_layout = QVBoxLayout(reports_widget)
        reports_layout.addWidget(QLabel("Custom Design Reports & Analytics", alignment=Qt.AlignCenter))

        # 4. Field Connections
        field_conn_widget = QWidget()
        field_conn_layout = QVBoxLayout(field_conn_widget)
        field_conn_layout.addWidget(QLabel("Database & Field Connections Mapping Workspace", alignment=Qt.AlignCenter))

        self.tabs.addTab(cards_widget, "Cards")
        self.tabs.addTab(workflows_widget, "Workflows")
        self.tabs.addTab(reports_widget, "Reports")
        self.tabs.addTab(field_conn_widget, "Field Connections")

        self.tabs.setCurrentIndex(initial_tab)
        main_layout.addWidget(self.tabs)


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
        self.dashboard_widget = DashboardWidget(username, on_logout=self.show_login, on_open_tab=self.show_design_tab)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.setCurrentWidget(self.dashboard_widget)

    def show_design_tab(self, tab_index=0):
        self.design_workspace = DesignWorkspaceWidget(on_close=lambda: self.stack.setCurrentWidget(self.dashboard_widget), initial_tab=tab_index)
        self.stack.addWidget(self.design_workspace)
        self.stack.setCurrentWidget(self.design_workspace)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
