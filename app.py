import sys
import os
import math
from PySide6.QtCore import Qt, QSize, QPointF
from PySide6.QtGui import QIcon, QPixmap, QFont, QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit,
    QDialog, QFrame, QMessageBox, QTabWidget, QStackedWidget
)

# -------------------------------------------------------------
# Instant PVC Vector Logo (Small version for Navigation Header)
# -------------------------------------------------------------
class InstantPVCLogo(QWidget):
    def __init__(self, size=40, is_white=True, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.size_val = size
        self.is_white = is_white

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        center = self.size_val / 2
        radius = (self.size_val / 2) - 3
        points = []
        for i in range(6):
            angle_rad = math.radians(60 * i - 30)
            x = center + radius * math.cos(angle_rad)
            y = center + radius * math.sin(angle_rad)
            points.append(QPointF(x, y))

        color = QColor("#FFFFFF") if self.is_white else QColor("#6B21A8")
        pen = QPen(color, 2)
        painter.setPen(pen)
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
        
        self.setStyleSheet("""
            QWidget#LoginMain {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4C1D95, stop:1 #2E1065);
            }
        """)
        self.setObjectName("LoginMain")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        center_box = QWidget()
        center_box.setFixedWidth(420)
        box_layout = QVBoxLayout(center_box)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(15)

        logo_container = QHBoxLayout()
        logo_container.addWidget(InstantPVCLogo(size=70, is_white=True), 0, Qt.AlignCenter)
        box_layout.addLayout(logo_container)

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
            QFrame {
                background-color: #FFFFFF;
                border-radius: 8px;
            }
            QLabel {
                color: #4B5563;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 13px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #7C3AED;
                background-color: #FFFFFF;
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

        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.setStyleSheet("QPushButton { background: transparent; color: #E9D5FF; font-size: 12px; border: none; } QPushButton:hover { color: #FFFFFF; text-decoration: underline; }")
        box_layout.addWidget(forgot_btn, 0, Qt.AlignCenter)

        login_btn = QPushButton("Sign In")
        login_btn.setFixedWidth(120)
        login_btn.setFixedHeight(38)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
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
# Main Dashboard (Refreshed according to the screenshot)
# -------------------------------------------------------------
class DashboardWidget(QWidget):
    def __init__(self, username, on_logout, on_open_designer):
        super().__init__()
        self.username = username
        self.on_logout = on_logout
        self.on_open_designer = on_open_designer

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top White Navigation Header Bar
        nav_bar = QFrame()
        nav_bar.setFixedHeight(50)
        nav_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        nav_layout.setSpacing(25)

        # Brand Logo & Title
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
        nav_layout.addSpacing(30)

        # Navigation Links
        nav_style = """
            QPushButton {
                background: transparent;
                border: none;
                color: #374151;
                font-size: 13px;
                font-weight: 600;
                padding: 5px 10px;
            }
            QPushButton:hover {
                color: #6B21A8;
            }
        """
        home_btn = QPushButton("Home")
        home_btn.setStyleSheet(nav_style + "QPushButton { color: #6B21A8; border-bottom: 2px solid #6B21A8; }")
        
        design_btn = QPushButton("Design ▾")
        design_btn.setStyleSheet(nav_style)
        design_btn.clicked.connect(self.on_open_designer)

        printer_btn = QPushButton("Printer Queues")
        printer_btn.setStyleSheet(nav_style)

        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(design_btn)
        nav_layout.addWidget(printer_btn)
        nav_layout.addStretch()

        main_layout.addWidget(nav_bar)

        # 2. Top Purple Status & User Info Bar
        purple_bar = QFrame()
        purple_bar.setFixedHeight(35)
        purple_bar.setStyleSheet("background-color: #6B21A8;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(20, 0, 20, 0)

        # Last Login Info Text
        login_info = QLabel(f"Last Login at Sun Sep 06 13:00:15 MMT 2026 from 127.0.0.1")
        login_info.setStyleSheet("color: #E9D5FF; font-size: 11px;")
        purple_layout.addWidget(login_info)
        purple_layout.addStretch()

        # User Controls (Notification, User Profile, Logout)
        user_controls = QHBoxLayout()
        user_controls.setSpacing(12)

        user_lbl = QLabel(f"{self.username} ▾")
        user_lbl.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold;")

        notif_btn = QPushButton("🔔 2")
        notif_btn.setStyleSheet("background-color: #EF4444; color: white; border-radius: 10px; font-size: 10px; font-weight: bold; padding: 2px 6px; border: none;")

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("background: transparent; color: #FCA5A5; font-size: 11px; border: none; font-weight: bold;")
        logout_btn.clicked.connect(self.on_logout)

        user_controls.addWidget(user_lbl)
        user_controls.addWidget(notif_btn)
        user_controls.addWidget(logout_btn)

        purple_layout.addLayout(user_controls)
        main_layout.addWidget(purple_bar)

        # 3. Main Workspace with Tabs (Credentials / Reports)
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #F9FAFB;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 15, 20, 15)

        # Custom Tab Widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E5E7EB;
                background-color: #FFFFFF;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #E5E7EB;
                color: #4B5563;
                font-weight: bold;
                padding: 8px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                color: #1F2937;
                border-top: 3px solid #6B21A8;
            }
        """)

        # Tab 1: Credentials
        cred_tab = QWidget()
        cred_layout = QVBoxLayout(cred_tab)
        cred_layout.setContentsMargins(15, 15, 15, 15)

        # Grid / List View Toggle Buttons
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

        # Empty Credentials View Area
        empty_box = QLabel("No credentials available. Click 'Design' in top menu to create one.")
        empty_box.setAlignment(Qt.AlignCenter)
        empty_box.setStyleSheet("color: #9CA3AF; font-size: 14px; margin-top: 80px;")
        cred_layout.addWidget(empty_box)
        cred_layout.addStretch()

        # Tab 2: Reports
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        reports_layout.addWidget(QLabel("Reports Dashboard", alignment=Qt.AlignCenter))

        tabs.addTab(cred_tab, "Credentials")
        tabs.addTab(reports_tab, "Reports")

        content_layout.addWidget(tabs)
        main_layout.addWidget(content_area)


# -------------------------------------------------------------
# Credential Designer Interface
# -------------------------------------------------------------
class CredentialDesignerWidget(QWidget):
    def __init__(self, on_close):
        super().__init__()
        self.on_close = on_close
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        ribbon = QFrame()
        ribbon.setFixedHeight(60)
        ribbon.setStyleSheet("background-color: #6B21A8;")
        ribbon_layout = QHBoxLayout(ribbon)
        ribbon_layout.setContentsMargins(15, 0, 15, 0)

        title_lbl = QLabel("Credential Design Workspace")
        title_lbl.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        ribbon_layout.addWidget(title_lbl)
        ribbon_layout.addStretch()

        back_btn = QPushButton("Back to Home")
        back_btn.setStyleSheet("background-color: #581C87; color: white; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold;")
        back_btn.clicked.connect(self.on_close)
        ribbon_layout.addWidget(back_btn)

        main_layout.addWidget(ribbon)

        # Workspace Placeholder
        ws = QLabel("Card Canvas Design Area")
        ws.setAlignment(Qt.AlignCenter)
        ws.setStyleSheet("background-color: #E5E7EB; font-size: 16px; color: #4B5563;")
        main_layout.addWidget(ws)


# -------------------------------------------------------------
# Main Application Stack Manager
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
        self.dashboard_widget = DashboardWidget(username, on_logout=self.show_login, on_open_designer=self.show_designer)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.setCurrentWidget(self.dashboard_widget)

    def show_designer(self):
        self.designer_widget = CredentialDesignerWidget(on_close=lambda: self.stack.setCurrentWidget(self.dashboard_widget))
        self.stack.addWidget(self.designer_widget)
        self.stack.setCurrentWidget(self.designer_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
