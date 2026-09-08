import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, QToolButton
)

# -------------------------------------------------------------
# 1. Login Screen Widget
# -------------------------------------------------------------
class LoginWidget(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setStyleSheet("background-color: #1E2530;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(360, 380)
        card.setStyleSheet("background-color: #FFFFFF; border-radius: 8px;")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(12)

        title = QLabel("ENTRUST Instant ID")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #7A0A8A; border: none; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(10)

        user_lbl = QLabel("Username:")
        user_lbl.setStyleSheet("color: #4A5568; font-weight: bold; border: none;")
        card_layout.addWidget(user_lbl)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter username")
        self.user_input.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #CBD5E0;
                border-radius: 4px;
                padding: 8px;
                background-color: #FAFAFA;
                color: #1A202C;
            }
            QLineEdit:focus { border: 1.5px solid #7A0A8A; }
        """)
        card_layout.addWidget(self.user_input)

        pass_lbl = QLabel("Password:")
        pass_lbl.setStyleSheet("color: #4A5568; font-weight: bold; border: none;")
        card_layout.addWidget(pass_lbl)

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Enter password")
        self.pass_input.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #CBD5E0;
                border-radius: 4px;
                padding: 8px;
                background-color: #FAFAFA;
                color: #1A202C;
            }
            QLineEdit:focus { border: 1.5px solid #7A0A8A; }
        """)
        self.pass_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.pass_input)

        card_layout.addSpacing(15)

        login_btn = QPushButton("Sign In")
        login_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #7A0A8A;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 9px;
            }
            QPushButton:hover { background-color: #630571; }
        """)
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)

        layout.addWidget(card)

    def handle_login(self):
        self.on_login_success()


# -------------------------------------------------------------
# 2. Main Entrust Dashboard UI (Exact Match with Provided Image)
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------------------------------------------------
        # BAR 1: Top White Header Bar
        # Logo | Subtitle | Home | Design v | Printer Queues
        # ---------------------------------------------------------
        top_bar = QFrame()
        top_bar.setFixedHeight(54)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #DCDCDC;")

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(18, 0, 20, 0)
        top_layout.setSpacing(18)

        # ENTRUST Cube Icon Logo + Text
        logo_box = QHBoxLayout()
        logo_box.setSpacing(8)

        logo_icon = QLabel("⬡")
        logo_icon.setStyleSheet("color: #7A0A8A; font-size: 24px; font-weight: bold;")

        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Segoe UI", 14, QFont.Bold))
        logo_text.setStyleSheet("color: #4A4A4A; letter-spacing: 1.5px;")

        logo_box.addWidget(logo_icon)
        logo_box.addWidget(logo_text)
        top_layout.addLayout(logo_box)

        # Vertical Divider Line
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #CCCCCC; max-height: 28px;")
        top_layout.addWidget(sep)

        # Subtitle Text (Adaptive Issuance™ Instant ID)
        sub_title = QLabel("Adaptive Issuance™\nInstant ID")
        sub_title.setFont(QFont("Segoe UI", 8, QFont.Bold))
        sub_title.setStyleSheet("color: #333333; line-height: 110%;")
        top_layout.addWidget(sub_title)

        top_layout.addSpacing(60)

        # Navigation Bar Buttons
        nav_box = QHBoxLayout()
        nav_box.setSpacing(35)

        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        home_btn.setStyleSheet("border: none; color: #222222; background: transparent;")
        home_btn.setCursor(Qt.PointingHandCursor)

        design_btn = QPushButton("Design ▾")
        design_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        design_btn.setStyleSheet("border: none; color: #222222; background: transparent;")
        design_btn.setCursor(Qt.PointingHandCursor)

        printer_btn = QPushButton("Printer Queues")
        printer_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        printer_btn.setStyleSheet("border: none; color: #222222; background: transparent;")
        printer_btn.setCursor(Qt.PointingHandCursor)

        nav_box.addWidget(home_btn)
        nav_box.addWidget(design_btn)
        nav_box.addWidget(printer_btn)
        top_layout.addLayout(nav_box)

        top_layout.addStretch()
        main_layout.addWidget(top_bar)

        # ---------------------------------------------------------
        # BAR 2: Deep Magenta / Purple Ribbon Bar
        # Credentials, Reports | Info & Profile Icons
        # ---------------------------------------------------------
        purple_bar = QFrame()
        purple_bar.setFixedHeight(36)
        purple_bar.setStyleSheet("background-color: #7A0A8A;")  # Exact Entrust Purple

        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)
        purple_layout.setSpacing(0)

        # Sub-tabs (Credentials, Reports)
        sub_tabs_layout = QHBoxLayout()
        sub_tabs_layout.setSpacing(0)

        cred_btn = QPushButton("Credentials")
        cred_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        cred_btn.setFixedHeight(36)
        cred_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #7A0A8A;
                border: none;
                padding: 0px 20px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }
        """)

        reports_btn = QPushButton("Reports")
        reports_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        reports_btn.setFixedHeight(36)
        reports_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding: 0px 20px;
            }
            QPushButton:hover { color: #E0B0FF; }
        """)

        sub_tabs_layout.addWidget(cred_btn)
        sub_tabs_layout.addWidget(reports_btn)
        purple_layout.addLayout(sub_tabs_layout)

        purple_layout.addStretch()

        # Right Side Info & Status Area
        right_info = QHBoxLayout()
        right_info.setSpacing(14)

        login_info = QLabel("Last Login at Tue Sep 08 01:41:31 MMT 2026 from IP 192.168.99.109")
        login_info.setFont(QFont("Segoe UI", 8))
        login_info.setStyleSheet("color: #DDA0DD;")

        user_btn = QPushButton("admin ▾")
        user_btn.setFont(QFont("Segoe UI", 8.5))
        user_btn.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")

        settings_icon = QLabel("⚙")
        settings_icon.setStyleSheet("color: #FFFFFF; font-size: 13px;")

        # Red Notification Badge Overlay Container
        badge_container = QWidget()
        badge_container.setFixedSize(22, 20)
        
        bell_lbl = QLabel("🔔", badge_container)
        bell_lbl.setStyleSheet("color: #FFFFFF; font-size: 11px;")
        bell_lbl.move(0, 3)

        num_badge = QLabel("2", badge_container)
        num_badge.setFont(QFont("Segoe UI", 6.5, QFont.Bold))
        num_badge.setStyleSheet("background-color: #E53E3E; color: white; border-radius: 5px; padding: 1px 3px;")
        num_badge.move(9, 0)

        help_icon = QLabel("❓")
        help_icon.setStyleSheet("color: #FFFFFF; font-size: 11px;")

        info_icon = QLabel("ℹ")
        info_icon.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: bold;")

        right_info.addWidget(login_info)
        right_info.addWidget(user_btn)
        right_info.addWidget(settings_icon)
        right_info.addWidget(badge_container)
        right_info.addWidget(help_icon)
        right_info.addWidget(info_icon)

        purple_layout.addLayout(right_info)
        main_layout.addWidget(purple_bar)

        # ---------------------------------------------------------
        # BAR 3: Light Grey Grid/List Toggle Toolbar
        # ---------------------------------------------------------
        tool_bar = QFrame()
        tool_bar.setFixedHeight(34)
        tool_bar.setStyleSheet("background-color: #F3F4F6; border-bottom: 1px solid #E5E7EB;")

        tool_layout = QHBoxLayout(tool_bar)
        tool_layout.setContentsMargins(8, 0, 8, 0)
        tool_layout.setSpacing(4)

        grid_btn = QToolButton()
        grid_btn.setText("田")
        grid_btn.setFixedSize(28, 25)
        grid_btn.setStyleSheet("""
            QToolButton {
                background-color: #94A3B8;
                border: 1px solid #64748B;
                border-radius: 2px;
                color: #FFFFFF;
                font-weight: bold;
            }
        """)

        list_btn = QToolButton()
        list_btn.setText("≡")
        list_btn.setFixedSize(28, 25)
        list_btn.setStyleSheet("""
            QToolButton {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E0;
                border-radius: 2px;
                color: #334155;
                font-weight: bold;
            }
        """)

        tool_layout.addWidget(grid_btn)
        tool_layout.addWidget(list_btn)
        tool_layout.addStretch()

        main_layout.addWidget(tool_bar)

        # ---------------------------------------------------------
        # MAIN WORKSPACE CANVAS
        # ---------------------------------------------------------
        workspace = QFrame()
        workspace.setStyleSheet("background-color: #FFFFFF;")
        main_layout.addWidget(workspace, stretch=1)

        # ---------------------------------------------------------
        # BOTTOM STATUS BAR
        # ---------------------------------------------------------
        status_bar = QFrame()
        status_bar.setFixedHeight(32)
        status_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")

        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 15, 0)
        status_layout.addStretch()

        queue_status_btn = QPushButton("🖨   Printer Queue Status")
        queue_status_btn.setFont(QFont("Segoe UI", 8.5, QFont.Bold))
        queue_status_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #E2E8F0);
                color: #1E3A8A;
                border: 1px solid #CBD5E0;
                border-radius: 3px;
                padding: 4px 14px;
            }
            QPushButton:hover { background-color: #EDF2F7; }
        """)
        status_layout.addWidget(queue_status_btn)

        main_layout.addWidget(status_bar)


# -------------------------------------------------------------
# 3. Main Container
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1280, 720)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_page = LoginWidget(on_login_success=self.show_dashboard)
        self.dashboard_page = EntrustDashboard()

        self.stacked_widget.addWidget(self.login_page)     # Index 0
        self.stacked_widget.addWidget(self.dashboard_page)  # Index 1

        self.stacked_widget.setCurrentIndex(0)

    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
