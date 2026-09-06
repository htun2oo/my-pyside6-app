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
# Main Application Dashboard
# -------------------------------------------------------------
class MainDashboardWidget(QWidget):
    def __init__(self, username, on_logout):
        super().__init__()
        self.username = username
        self.on_logout = on_logout

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Navigation Bar (Home | Design | Printer Queues)
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

        # 2. Purple User Info Bar (Last Login Time ကို ဖယ်ရှားထားပါသည်)
        purple_bar = QFrame()
        purple_bar.setFixedHeight(35)
        purple_bar.setStyleSheet("background-color: #6B21A8;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(20, 0, 20, 0)

        # ဘယ်ဘက်ခြမ်းကို ခဲထားပြီး ညာဘက်ခြမ်းတွင် User Info နှင့် Logout ကိုသာ ပြသထားပါသည်
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

        # 3. Main Views (Stacked Widget for Home View & Design View)
        self.main_stack = QStackedWidget()

        # --- A. HOME VIEW ---
        home_view = QWidget()
        home_layout = QVBoxLayout(home_view)
        home_layout.setContentsMargins(20, 15, 20, 15)

        home_tabs = QTabWidget()
        home_tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #E5E7EB; background-color: #FFFFFF; top: -1px; }
            QTabBar::tab { background-color: #E5E7EB; color: #4B5563; font-weight: bold; padding: 8px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 4px; }
            QTabBar::tab:selected { background-color: #FFFFFF; color: #1F2937; border-top: 3px solid #6B21A8; }
        """)

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

        empty_box = QLabel("No credentials available. Click 'Design' in top menu to manage templates.")
        empty_box.setAlignment(Qt.AlignCenter)
        empty_box.setStyleSheet("color: #9CA3AF; font-size: 14px; margin-top: 80px;")
        cred_layout.addWidget(empty_box)
        cred_layout.addStretch()

        system_logs_tab = QWidget()
        logs_layout = QVBoxLayout(system_logs_tab)
        logs_layout.addWidget(QLabel("System Logs Dashboard", alignment=Qt.AlignCenter))

        home_tabs.addTab(cred_tab, "Credentials")
        home_tabs.addTab(system_logs_tab, "System Logs")
        home_layout.addWidget(home_tabs)

        # --- B. DESIGN VIEW (Cards, Workflows, Reports, Field Connections Tabs) ---
        design_view = QWidget()
        design_layout = QVBoxLayout(design_view)
        design_layout.setContentsMargins(20, 15, 20, 15)

        self.design_tabs = QTabWidget()
        self.design_tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #E5E7EB; background-color: #FFFFFF; top: -1px; }
            QTabBar::tab { background-color: #E5E7EB; color: #4B5563; font-weight: bold; padding: 10px 24px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 4px; font-size: 13px; }
            QTabBar::tab:selected { background-color: #FFFFFF; color: #6B21A8; border-top: 3px solid #6B21A8; }
        """)

        # 1. Cards Tab
        cards_tab = QWidget()
        cards_layout = QVBoxLayout(cards_tab)
        cards_layout.addWidget(QLabel("Cards Design Canvas Area", alignment=Qt.AlignCenter))

        # 2. Workflows Tab
        workflows_tab = QWidget()
        workflows_layout = QVBoxLayout(workflows_tab)
        workflows_layout.addWidget(QLabel("Workflows & Issuance Rules Manager", alignment=Qt.AlignCenter))

        # 3. Reports Tab
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        reports_layout.addWidget(QLabel("Reports Template Generator", alignment=Qt.AlignCenter))

        # 4. Field Connections Tab
        field_conn_tab = QWidget()
        field_conn_layout = QVBoxLayout(field_conn_tab)
        field_conn_layout.addWidget(QLabel("Database & Field Connections Mapping Workspace", alignment=Qt.AlignCenter))

        self.design_tabs.addTab(cards_tab, "Cards")
        self.design_tabs.addTab(workflows_tab, "Workflows")
        self.design_tabs.addTab(reports_tab, "Reports")
        self.design_tabs.addTab(field_conn_tab, "Field Connections")

        design_layout.addWidget(self.design_tabs)

        # Add Views to Main Stack
        self.main_stack.addWidget(home_view)    # Index 0
        self.main_stack.addWidget(design_view)  # Index 1

        main_layout.addWidget(self.main_stack)
        
        # Show Home View by Default
        self.show_home_view()

    def set_nav_active(self, active_btn):
        active_style = "QPushButton { color: #6B21A8; border-bottom: 2px solid #6B21A8; font-weight: bold; padding: 14px 16px; background: transparent; }"
        normal_style = "QPushButton { color: #374151; border-bottom: 2px solid transparent; font-weight: 600; padding: 14px 16px; background: transparent; } QPushButton:hover { color: #6B21A8; }"

        self.home_btn.setStyleSheet(active_style if active_btn == "home" else normal_style)
        self.design_btn.setStyleSheet(active_style if active_btn == "design" else normal_style)
        self.printer_btn.setStyleSheet(normal_style)

    def show_home_view(self):
        self.set_nav_active("home")
        self.main_stack.setCurrentIndex(0)

    def show_design_view(self):
        self.set_nav_active("design")
        self.main_stack.setCurrentIndex(1)


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
        self.dashboard_widget = MainDashboardWidget(username, on_logout=self.show_login)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.setCurrentWidget(self.dashboard_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
