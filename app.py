import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, QMessageBox,
    QToolButton
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
        title.setStyleSheet("color: #6B21A8; border: none; background: transparent;")
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
            QLineEdit:focus { border: 1.5px solid #6B21A8; }
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
            QLineEdit:focus { border: 1.5px solid #6B21A8; }
        """)
        self.pass_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.pass_input)

        card_layout.addSpacing(15)

        login_btn = QPushButton("Sign In")
        login_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B21A8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 9px;
            }
            QPushButton:hover { background-color: #581C87; }
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
        # BAR 1: Top White Bar
        # Logo | Title | Nav Tabs (Home, Design v, Printer Queues)
        # ---------------------------------------------------------
        top_bar = QFrame()
        top_bar.setFixedHeight(48)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(15, 0, 15, 0)
        top_layout.setSpacing(20)

        # Entrust Logo Icon Placeholder + Text
        logo_box = QHBoxLayout()
        logo_box.setSpacing(6)

        logo_icon = QLabel("⬡")
        logo_icon.setStyleSheet("color: #6B21A8; font-size: 20px; font-weight: bold;")

        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Segoe UI", 13, QFont.Bold))
        logo_text.setStyleSheet("color: #6B21A8; letter-spacing: 1px;")

        logo_box.addWidget(logo_icon)
        logo_box.addWidget(logo_text)
        top_layout.addLayout(logo_box)

        # Vertical Separator Line
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.VLine)
        sep1.setStyleSheet("color: #CBD5E0; max-height: 24px;")
        top_layout.addWidget(sep1)

        # Subtitle Text
        sub_title = QLabel("Adaptive Issuance\nInstant ID")
        sub_title.setFont(QFont("Segoe UI", 8, QFont.Bold))
        sub_title.setStyleSheet("color: #4A5568; line-height: 100%;")
        top_layout.addWidget(sub_title)

        top_layout.addSpacing(30)

        # Main Navigation Tabs
        nav_box = QHBoxLayout()
        nav_box.setSpacing(25)

        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Segoe UI", 9.5, QFont.Medium))
        home_btn.setStyleSheet("border: none; color: #4A5568; background: transparent;")
        home_btn.setCursor(Qt.PointingHandCursor)

        design_btn = QPushButton("Design ▾")
        design_btn.setFont(QFont("Segoe UI", 9.5, QFont.Medium))
        design_btn.setStyleSheet("border: none; color: #4A5568; background: transparent;")
        design_btn.setCursor(Qt.PointingHandCursor)

        printer_btn = QPushButton("Printer Queues")
        printer_btn.setFont(QFont("Segoe UI", 9.5, QFont.Medium))
        printer_btn.setStyleSheet("border: none; color: #4A5568; background: transparent;")
        printer_btn.setCursor(Qt.PointingHandCursor)

        nav_box.addWidget(home_btn)
        nav_box.addWidget(design_btn)
        nav_box.addWidget(printer_box := printer_btn)
        top_layout.addLayout(nav_box)

        top_layout.addStretch()
        main_layout.addWidget(top_bar)

        # ---------------------------------------------------------
        # BAR 2: Dark Purple Ribbon Bar
        # Sub-tabs (Credentials, Reports) | Info Text | User Icons
        # ---------------------------------------------------------
        purple_bar = QFrame()
        purple_bar.setFixedHeight(38)
        purple_bar.setStyleSheet("background-color: #6B1182;")  # Entrust Deep Purple

        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)
        purple_layout.setSpacing(0)

        # Left Tabs (Credentials, Reports)
        sub_tabs_layout = QHBoxLayout()
        sub_tabs_layout.setSpacing(2)

        cred_btn = QPushButton("Credentials")
        cred_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        cred_btn.setFixedHeight(38)
        cred_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #6B1182;
                border: none;
                padding: 0px 18px;
                border-top-left-radius: 2px;
                border-top-right-radius: 2px;
            }
        """)

        reports_btn = QPushButton("Reports")
        reports_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        reports_btn.setFixedHeight(38)
        reports_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #E9D5FF;
                border: none;
                padding: 0px 18px;
            }
            QPushButton:hover { color: #FFFFFF; }
        """)

        sub_tabs_layout.addWidget(cred_btn)
        sub_tabs_layout.addWidget(reports_btn)
        purple_layout.addLayout(sub_tabs_layout)

        purple_layout.addStretch()

        # Right Side Information & Action Icons
        right_info_box = QHBoxLayout()
        right_info_box.setSpacing(12)

        login_info = QLabel("Last Login: 08-MAY-2026 01:42 | IP: 192.168.56.1")
        login_info.setFont(QFont("Segoe UI", 8))
        login_info.setStyleSheet("color: #D8B4FE;")

        user_dropdown = QPushButton("admin ▾")
        user_dropdown.setFont(QFont("Segoe UI", 8.5))
        user_dropdown.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("color: #FFFFFF; font-size: 11px;")

        settings_icon = QLabel("⚙")
        settings_icon.setStyleSheet("color: #FFFFFF; font-size: 13px;")

        bell_icon = QLabel("🔔²")
        bell_icon.setStyleSheet("color: #FF5555; font-size: 12px; font-weight: bold;")

        question_icon = QLabel("❓")
        question_icon.setStyleSheet("color: #FFFFFF; font-size: 11px;")

        power_icon = QLabel("⏻")
        power_icon.setStyleSheet("color: #FFFFFF; font-size: 12px;")

        right_info_box.addWidget(login_info)
        right_info_box.addWidget(user_dropdown)
        right_info_box.addWidget(search_icon)
        right_info_box.addWidget(settings_icon)
        right_info_box.addWidget(bell_icon)
        right_info_box.addWidget(question_icon)
        right_info_box.addWidget(power_icon)

        purple_layout.addLayout(right_info_box)
        main_layout.addWidget(purple_bar)

        # ---------------------------------------------------------
        # BAR 3: Light Grey Action Bar (Grid / List View Icons)
        # ---------------------------------------------------------
        action_bar = QFrame()
        action_bar.setFixedHeight(34)
        action_bar.setStyleSheet("background-color: #E2E8F0; border-bottom: 1px solid #CBD5E0;")

        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(12, 0, 12, 0)
        action_layout.setSpacing(4)

        grid_btn = QToolButton()
        grid_btn.setText("田")
        grid_btn.setFixedSize(26, 24)
        grid_btn.setStyleSheet("""
            QToolButton {
                background-color: #CBD5E0;
                border: 1px solid #A0AEC0;
                border-radius: 2px;
                color: #2D3748;
            }
        """)

        list_btn = QToolButton()
        list_btn.setText("≡")
        list_btn.setFixedSize(26, 24)
        list_btn.setStyleSheet("""
            QToolButton {
                background-color: #EDF2F7;
                border: 1px solid #CBD5E0;
                border-radius: 2px;
                color: #4A5568;
            }
        """)

        action_layout.addWidget(grid_btn)
        action_layout.addWidget(list_btn)
        action_layout.addStretch()

        main_layout.addWidget(action_bar)

        # ---------------------------------------------------------
        # MAIN WORKSPACE AREA (Grey Grid Background)
        # ---------------------------------------------------------
        workspace = QFrame()
        workspace.setStyleSheet("background-color: #E5E7EB;")
        main_layout.addWidget(workspace, stretch=1)

        # ---------------------------------------------------------
        # BOTTOM STATUS BAR
        # ---------------------------------------------------------
        status_bar = QFrame()
        status_bar.setFixedHeight(28)
        status_bar.setStyleSheet("background-color: #E2E8F0; border-top: 1px solid #CBD5E0;")

        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 15, 0)
        status_layout.addStretch()

        queue_status_btn = QPushButton("🖨  Printer Queue Status")
        queue_status_btn.setFont(QFont("Segoe UI", 8.5))
        queue_status_btn.setStyleSheet("""
            QPushButton {
                background-color: #EDF2F7;
                color: #2D3748;
                border: 1px solid #CBD5E0;
                border-radius: 3px;
                padding: 2px 10px;
            }
            QPushButton:hover { background-color: #E2E8F0; }
        """)
        status_layout.addWidget(queue_status_btn)

        main_layout.addWidget(status_bar)


# -------------------------------------------------------------
# 3. Main Container
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrust Adaptive Issuance Instant ID")
        self.resize(1200, 750)

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
