import sys
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, QToolButton,
    QMessageBox
)

# -------------------------------------------------------------
# Sprite Image Helper Function
# -------------------------------------------------------------
def get_sprite_icon(sprite_pixmap, x, y, width=24, height=24):
    """ sprite_button.png ထဲမှ သက်ဆိုင်ရာ Coordinate အတိုင်း Icon ဖြတ်ယူသည့် Function """
    if sprite_pixmap.isNull():
        return QPixmap()
    return sprite_pixmap.copy(QRect(x, y, width, height))


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
# 2. Main Entrust Dashboard UI (Sprite Icons Integration)
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Sprite Sheet Image Load မည် (file path: sprite_button.png)
        self.sprite = QPixmap("sprite_button.png")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------------------------------------------------
        # BAR 1: Top White Header Bar
        # ---------------------------------------------------------
        top_bar = QFrame()
        top_bar.setFixedHeight(54)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #DCDCDC;")

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(18, 0, 20, 0)
        top_layout.setSpacing(18)

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

        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #CCCCCC; max-height: 28px;")
        top_layout.addWidget(sep)

        sub_title = QLabel("Adaptive Issuance™\nInstant ID")
        sub_title.setFont(QFont("Segoe UI", 8, QFont.Bold))
        sub_title.setStyleSheet("color: #333333; line-height: 110%;")
        top_layout.addWidget(sub_title)

        top_layout.addSpacing(60)

        nav_box = QHBoxLayout()
        nav_box.setSpacing(35)

        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        home_btn.setStyleSheet("border: none; color: #222222; background: transparent;")

        design_btn = QPushButton("Design ▾")
        design_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        design_btn.setStyleSheet("border: none; color: #222222; background: transparent;")

        printer_btn = QPushButton("Printer Queues")
        printer_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        printer_btn.setStyleSheet("border: none; color: #222222; background: transparent;")

        nav_box.addWidget(home_btn)
        nav_box.addWidget(design_btn)
        nav_box.addWidget(printer_btn)
        top_layout.addLayout(nav_box)

        top_layout.addStretch()
        main_layout.addWidget(top_bar)

        # ---------------------------------------------------------
        # BAR 2: Deep Purple Ribbon Bar (With Sprite Icons)
        # ---------------------------------------------------------
        purple_bar = QFrame()
        purple_bar.setFixedHeight(36)
        purple_bar.setStyleSheet("background-color: #7A0A8A;")

        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)
        purple_layout.setSpacing(0)

        sub_tabs_layout = QHBoxLayout()
        sub_tabs_layout.setSpacing(0)

        self.cred_tab_btn = QPushButton("Credentials")
        self.cred_tab_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.cred_tab_btn.setFixedHeight(36)

        self.reports_tab_btn = QPushButton("Reports")
        self.reports_tab_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.reports_tab_btn.setFixedHeight(36)

        sub_tabs_layout.addWidget(self.cred_tab_btn)
        sub_tabs_layout.addWidget(self.reports_tab_btn)
        purple_layout.addLayout(sub_tabs_layout)

        purple_layout.addStretch()

        right_info = QHBoxLayout()
        right_info.setSpacing(12)

        login_info = QLabel("Last Login at Tue Sep 08 01:41:31 MMT 2026 from IP 192.168.99.109")
        login_info.setFont(QFont("Segoe UI", 8))
        login_info.setStyleSheet("color: #DDA0DD;")

        user_btn = QPushButton("admin ▾")
        user_btn.setFont(QFont("Segoe UI", 8.5))
        user_btn.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")

        # Sprite Icons Extraction for Header Right Icons
        settings_icon = QLabel()
        settings_icon.setPixmap(get_sprite_icon(self.sprite, 810, 12, 18, 18))  # Gear Icon

        badge_container = QWidget()
        badge_container.setFixedSize(22, 20)
        
        bell_lbl = QLabel(badge_container)
        bell_lbl.setPixmap(get_sprite_icon(self.sprite, 850, 12, 16, 16))       # Bell Icon
        bell_lbl.move(0, 3)

        num_badge = QLabel("2", badge_container)
        num_badge.setFont(QFont("Segoe UI", 6.5, QFont.Bold))
        num_badge.setStyleSheet("background-color: #E53E3E; color: white; border-radius: 5px; padding: 1px 3px;")
        num_badge.move(9, 0)

        help_icon = QLabel()
        help_icon.setPixmap(get_sprite_icon(self.sprite, 885, 12, 16, 16))      # Question Icon

        info_icon = QLabel()
        info_icon.setPixmap(get_sprite_icon(self.sprite, 915, 12, 16, 16))      # Info Icon

        right_info.addWidget(login_info)
        right_info.addWidget(user_btn)
        right_info.addWidget(settings_icon)
        right_info.addWidget(badge_container)
        right_info.addWidget(help_icon)
        right_info.addWidget(info_icon)

        purple_layout.addLayout(right_info)
        main_layout.addWidget(purple_bar)

        # ---------------------------------------------------------
        # BAR 3: Light Grey Grid/List View Toolbar (Sprite Icons)
        # ---------------------------------------------------------
        tool_bar = QFrame()
        tool_bar.setFixedHeight(34)
        tool_bar.setStyleSheet("background-color: #F3F4F6; border-bottom: 1px solid #E5E7EB;")

        tool_layout = QHBoxLayout(tool_bar)
        tool_layout.setContentsMargins(8, 0, 8, 0)
        tool_layout.setSpacing(4)

        grid_btn = QToolButton()
        grid_btn.setIcon(get_sprite_icon(self.sprite, 0, 122, 18, 18))  # Grid Icon Row 3
        grid_btn.setFixedSize(28, 25)
        grid_btn.setStyleSheet("""
            QToolButton {
                background-color: #94A3B8;
                border: 1px solid #64748B;
                border-radius: 2px;
            }
        """)

        list_btn = QToolButton()
        list_btn.setIcon(get_sprite_icon(self.sprite, 245, 122, 18, 18)) # List Icon Row 3
        list_btn.setFixedSize(28, 25)
        list_btn.setStyleSheet("""
            QToolButton {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E0;
                border-radius: 2px;
            }
        """)

        tool_layout.addWidget(grid_btn)
        tool_layout.addWidget(list_btn)
        tool_layout.addStretch()

        main_layout.addWidget(tool_bar)

        # ---------------------------------------------------------
        # MAIN WORKSPACE CANVAS
        # ---------------------------------------------------------
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #FFFFFF;")

        self.credentials_page = QWidget()
        self.reports_page = QWidget()

        reports_layout = QHBoxLayout(self.reports_page)
        reports_layout.setContentsMargins(15, 15, 15, 15)
        reports_layout.setSpacing(15)
        reports_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        card1 = self.create_report_card("Credentials Issued", self.run_issued_report)
        card2 = self.create_report_card("Credentials Printed", self.run_printed_report)

        reports_layout.addWidget(card1)
        reports_layout.addWidget(card2)

        self.content_stack.addWidget(self.credentials_page)
        self.content_stack.addWidget(self.reports_page)

        main_layout.addWidget(self.content_stack, stretch=1)

        # ---------------------------------------------------------
        # BOTTOM STATUS BAR (With Printer Queue Sprite Icon)
        # ---------------------------------------------------------
        status_bar = QFrame()
        status_bar.setFixedHeight(32)
        status_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")

        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 15, 0)
        status_layout.addStretch()

        queue_status_btn = QPushButton(" Printer Queue Status")
        queue_status_btn.setIcon(get_sprite_icon(self.sprite, 915, 0, 20, 20)) # Printer Icon Row 1
        queue_status_btn.setFont(QFont("Segoe UI", 8.5, QFont.Bold))
        queue_status_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #E2E8F0);
                color: #1E3A8A;
                border: 1px solid #CBD5E0;
                border-radius: 3px;
                padding: 4px 12px;
            }
            QPushButton:hover { background-color: #EDF2F7; }
        """)
        status_layout.addWidget(queue_status_btn)

        main_layout.addWidget(status_bar)

        # Tab Switching Signals
        self.cred_tab_btn.clicked.connect(lambda: self.switch_sub_tab(0))
        self.reports_tab_btn.clicked.connect(lambda: self.switch_sub_tab(1))

        self.switch_sub_tab(1)

    def create_report_card(self, title_text, run_callback):
        card = QFrame()
        card.setFixedSize(175, 185)
        card.setStyleSheet("background-color: #8C8C8C; border-radius: 4px;")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        chart_box = QFrame()
        chart_box.setFixedHeight(85)
        chart_box.setStyleSheet("background-color: #FFFFFF; border-radius: 2px;")
        
        chart_layout = QVBoxLayout(chart_box)
        chart_layout.setAlignment(Qt.AlignCenter)

        # Chart Icon from Sprite Sheet
        chart_icon = QLabel()
        chart_icon.setPixmap(get_sprite_icon(self.sprite, 440, 0, 40, 30))
        chart_layout.addWidget(chart_icon, alignment=Qt.AlignCenter)

        sub_chart_lbl = QLabel("Week 30, 2013")
        sub_chart_lbl.setFont(QFont("Segoe UI", 6.5))
        sub_chart_lbl.setStyleSheet("color: #888888;")
        sub_chart_lbl.setAlignment(Qt.AlignCenter)
        chart_layout.addWidget(sub_chart_lbl)

        layout.addWidget(chart_box)

        title_lbl = QLabel(title_text)
        title_lbl.setFont(QFont("Segoe UI", 9.5, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; background: transparent;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        # Run Button with Sprite Play Arrow
        run_btn = QPushButton(" Run")
        run_btn.setIcon(get_sprite_icon(self.sprite, 0, 0, 14, 14))
        run_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        run_btn.setCursor(Qt.PointingHandCursor)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding: 4px;
            }
            QPushButton:hover { color: #E2E8F0; }
        """)
        run_btn.clicked.connect(run_callback)
        layout.addWidget(run_btn, alignment=Qt.AlignCenter)

        return card

    def switch_sub_tab(self, index):
        self.content_stack.setCurrentIndex(index)
        if index == 0:
            self.cred_tab_btn.setStyleSheet("""
                background-color: #FFFFFF; color: #7A0A8A; border: none;
                padding: 0px 20px; border-top-left-radius: 3px; border-top-right-radius: 3px;
            """)
            self.reports_tab_btn.setStyleSheet("""
                background-color: transparent; color: #FFFFFF; border: none; padding: 0px 20px;
            """)
        else:
            self.reports_tab_btn.setStyleSheet("""
                background-color: #FFFFFF; color: #7A0A8A; border: none;
                padding: 0px 20px; border-top-left-radius: 3px; border-top-right-radius: 3px;
            """)
            self.cred_tab_btn.setStyleSheet("""
                background-color: transparent; color: #FFFFFF; border: none; padding: 0px 20px;
            """)

    def run_issued_report(self):
        QMessageBox.information(self, "Report Executed", "Generating Credentials Issued Report...")

    def run_printed_report(self):
        QMessageBox.information(self, "Report Executed", "Generating Credentials Printed Report...")


# -------------------------------------------------------------
# 3. Main Window
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

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dashboard_page)

        self.stacked_widget.setCurrentIndex(0)

    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
