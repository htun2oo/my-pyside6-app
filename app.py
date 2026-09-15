import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QPen
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView, QScrollBar, QMenu
)

# -------------------------------------------------------------
# Icons and Graphics Helpers
# -------------------------------------------------------------
def draw_grid_icon(size=14, color="#1E293B"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, False)
    p.setBrush(QBrush(QColor(color)))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 0, 6, 6)
    p.drawRect(8, 0, 6, 6)
    p.drawRect(0, 8, 6, 6)
    p.drawRect(8, 8, 6, 6)
    p.end()
    return QIcon(pixmap)

def draw_list_icon(size=14, color="#1E293B"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, False)
    p.setBrush(QBrush(QColor(color)))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 1, 14, 3)
    p.drawRect(0, 6, 14, 3)
    p.drawRect(0, 11, 14, 3)
    p.end()
    return QIcon(pixmap)

def create_report_thumbnail():
    pixmap = QPixmap(100, 60)
    pixmap.fill(QColor("#FFFFFF"))
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QPen(QColor("#D1D5DB"), 1))
    p.drawRect(2, 2, 95, 55)
    p.setBrush(QBrush(QColor("#059669")))
    p.setPen(Qt.NoPen)
    bars = [(15, 20, 8, 25), (28, 15, 8, 30), (41, 10, 8, 35), (54, 18, 8, 27), (67, 8, 8, 37)]
    for x, y, w, h in bars:
        p.drawRect(x, y + 5, w, h)
    p.setFont(QFont("Arial", 5))
    p.setPen(QPen(QColor("#6B7280")))
    p.drawText(QRectF(0, 42, 100, 12), Qt.AlignCenter, "Week 30, 2013")
    p.end()
    return pixmap


# -------------------------------------------------------------
# Reusable Toolbar Widget
# -------------------------------------------------------------
class ViewToggleToolbar(QFrame):
    def __init__(self, on_grid_click=None, on_list_click=None, is_grid_active=True):
        super().__init__()
        self.setFixedHeight(30)
        self.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB; }")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(3)

        self.grid_btn = QPushButton()
        self.grid_btn.setFixedSize(24, 22)
        self.grid_btn.setCursor(Qt.PointingHandCursor)

        self.list_btn = QPushButton()
        self.list_btn.setFixedSize(24, 22)
        self.list_btn.setCursor(Qt.PointingHandCursor)

        self.grid_btn.setIcon(draw_grid_icon(12, "#1F2937"))
        self.list_btn.setIcon(draw_list_icon(12, "#1F2937"))

        self.set_active_state(is_grid_active)

        if on_grid_click:
            self.grid_btn.clicked.connect(on_grid_click)
        if on_list_click:
            self.list_btn.clicked.connect(on_list_click)

        layout.addWidget(self.grid_btn)
        layout.addWidget(self.list_btn)
        layout.addStretch()

    def set_active_state(self, is_grid_active):
        if is_grid_active:
            self.grid_btn.setStyleSheet("QPushButton { background-color: #C5D1DF; border: 1px solid #4B5563; border-radius: 1px; }")
            self.list_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; border: 1px solid #9CA3AF; border-radius: 1px; }")
        else:
            self.grid_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; border: 1px solid #9CA3AF; border-radius: 1px; }")
            self.list_btn.setStyleSheet("QPushButton { background-color: #C5D1DF; border: 1px solid #4B5563; border-radius: 1px; }")


# -------------------------------------------------------------
# Placeholder Workspace View
# -------------------------------------------------------------
class GenericWorkspace(QWidget):
    def __init__(self, title_text="Workspace"):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        toolbar = ViewToggleToolbar(is_grid_active=False)
        layout.addWidget(toolbar)

        content = QLabel(f" {title_text} View Content")
        content.setFont(QFont("Arial", 11))
        content.setStyleSheet("color: #6B7280; padding: 20px;")
        content.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(content, stretch=1)


# -------------------------------------------------------------
# Main Application Dashboard
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(42)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 15, 0)

        logo_hex = QLabel("⬡")
        logo_hex.setStyleSheet("color: #7B0082; font-size: 19px; font-weight: bold;")
        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Arial", 11, QFont.Bold))
        logo_text.setStyleSheet("color: #2D3748; padding-right: 8px; border-right: 1px solid #D1D5DB;")

        sub_text = QLabel("Adaptive Issuance™\nInstant ID")
        sub_text.setFont(QFont("Arial", 7, QFont.Bold))

        top_layout.addWidget(logo_hex)
        top_layout.addWidget(logo_text)
        top_layout.addWidget(sub_text)
        top_layout.addSpacing(30)

        # Main Nav Buttons
        self.home_nav_btn = QPushButton("Home")
        self.design_nav_btn = QPushButton("Design ▾")
        self.queue_nav_btn = QPushButton("Printer Queues")

        for btn in [self.home_nav_btn, self.design_nav_btn, self.queue_nav_btn]:
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("border: none; color: #1A202C; background: transparent; padding: 0 6px;")

        self.home_nav_btn.clicked.connect(self.switch_to_home_section)
        self.design_nav_btn.clicked.connect(self.switch_to_design_section)

        # Dropdown Menu for Design
        design_menu = QMenu(self)
        design_menu.addAction("Credential Designs", lambda: self.switch_to_design_section(0))
        design_menu.addAction("Workflows", lambda: self.switch_to_design_section(1))
        design_menu.addAction("Reports", lambda: self.switch_to_design_section(2))
        design_menu.addAction("Field Connections", lambda: self.switch_to_design_section(3))
        self.design_nav_btn.setMenu(design_menu)

        top_layout.addWidget(self.home_nav_btn)
        top_layout.addWidget(self.design_nav_btn)
        top_layout.addWidget(self.queue_nav_btn)
        top_layout.addStretch()

        user_info = QLabel("admin ▾   ⚙ ▾   🔔²   ❓   ℹ")
        user_info.setStyleSheet("color: #2D3748; font-size: 8.5pt; font-weight: bold;")
        top_layout.addWidget(user_info)

        main_layout.addWidget(top_bar)

        # 2. Purple Secondary Navigation Bar
        self.purple_bar = QFrame()
        self.purple_bar.setFixedHeight(34)
        self.purple_bar.setStyleSheet("background-color: #7B0082;")
        self.purple_layout = QHBoxLayout(self.purple_bar)
        self.purple_layout.setContentsMargins(10, 0, 15, 0)
        self.purple_layout.setSpacing(0)

        main_layout.addWidget(self.purple_bar)

        # 3. Middle Body Content (Stacked Pages)
        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.section_stack = QStackedWidget()

        # Build Home View Stack (Credentials, Reports)
        self.home_stack = QStackedWidget()
        self.home_credentials_page = GenericWorkspace("Home -> Credentials")
        self.home_reports_page = GenericWorkspace("Home -> Reports")
        self.home_stack.addWidget(self.home_credentials_page)
        self.home_stack.addWidget(self.home_reports_page)

        # Build Design View Stack (Credential Designs, Workflows, Reports, Field Connections)
        self.design_stack = QStackedWidget()
        self.design_cred_page = GenericWorkspace("Design -> Credential Designs")
        self.design_workflow_page = GenericWorkspace("Design -> Workflows")
        self.design_reports_page = GenericWorkspace("Design -> Reports")
        self.design_fields_page = GenericWorkspace("Design -> Field Connections")

        self.design_stack.addWidget(self.design_cred_page)
        self.design_stack.addWidget(self.design_workflow_page)
        self.design_stack.addWidget(self.design_reports_page)
        self.design_stack.addWidget(self.design_fields_page)

        self.section_stack.addWidget(self.home_stack)
        self.section_stack.addWidget(self.design_stack)

        body_layout.addWidget(self.section_stack, stretch=1)

        # Right Blank Side Panel
        right_panel = QFrame()
        right_panel.setFixedWidth(200)
        right_panel.setStyleSheet("border-left: 1px solid #D1D5DB; background-color: #FFFFFF;")
        body_layout.addWidget(right_panel)

        main_layout.addWidget(body_container, stretch=1)

        # 4. Bottom Status Bar
        status_bar = QFrame()
        status_bar.setFixedHeight(30)
        status_bar.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #D1D5DB;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.addStretch()

        queue_status_btn = QPushButton(" 🖨   Printer Queue Status")
        queue_status_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
        queue_status_btn.setFixedHeight(30)
        queue_status_btn.setFixedWidth(200)
        queue_status_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E2ECF7, stop:1 #BCCFE3);
                color: #0F172A;
                border: none;
                border-left: 1px solid #D1D5DB;
            }
        """)
        status_layout.addWidget(queue_status_btn)
        main_layout.addWidget(status_bar)

        # Start at Home Section
        self.switch_to_home_section()

    def clear_purple_bar(self):
        while self.purple_layout.count() > 0:
            item = self.purple_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # --- HOME SECTION NAVIGATION ---
    def switch_to_home_section(self):
        self.section_stack.setCurrentIndex(0)
        self.clear_purple_bar()

        btn_credentials = QPushButton("Credentials")
        btn_reports = QPushButton("Reports")

        for btn in [btn_credentials, btn_reports]:
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setFixedHeight(34)
            btn.setCursor(Qt.PointingHandCursor)

        btn_credentials.clicked.connect(lambda: self.set_sub_tab(self.home_stack, 0, [btn_credentials, btn_reports]))
        btn_reports.clicked.connect(lambda: self.set_sub_tab(self.home_stack, 1, [btn_credentials, btn_reports]))

        self.purple_layout.addWidget(btn_credentials)
        self.purple_layout.addWidget(btn_reports)
        self.purple_layout.addStretch()

        last_login = QLabel("Last Login at Wed Sep 09 18:33:05 MMT 2026 from IP 192.168.56.1")
        last_login.setFont(QFont("Arial", 8))
        last_login.setStyleSheet("color: #E9D5FF; border: none;")
        self.purple_layout.addWidget(last_login)

        # Select first tab by default
        self.set_sub_tab(self.home_stack, 0, [btn_credentials, btn_reports])

    # --- DESIGN SECTION NAVIGATION ---
    def switch_to_design_section(self, target_tab_index=0):
        self.section_stack.setCurrentIndex(1)
        self.clear_purple_bar()

        btn_cred_designs = QPushButton("Credential Designs")
        btn_workflows = QPushButton("Workflows")
        btn_reports = QPushButton("Reports")
        btn_fields = QPushButton("Field Connections")

        tab_buttons = [btn_cred_designs, btn_workflows, btn_reports, btn_fields]

        for idx, btn in enumerate(tab_buttons):
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setFixedHeight(34)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self.set_sub_tab(self.design_stack, i, tab_buttons))
            self.purple_layout.addWidget(btn)

        self.purple_layout.addStretch()

        last_login = QLabel("Last Login at Wed Sep 09 18:33:05 MMT 2026 from IP 192.168.56.1")
        last_login.setFont(QFont("Arial", 8))
        last_login.setStyleSheet("color: #E9D5FF; border: none;")
        self.purple_layout.addWidget(last_login)

        # Select specified sub-tab
        self.set_sub_tab(self.design_stack, target_tab_index, tab_buttons)

    # Helper function to switch tabs and update active tab UI style
    def set_sub_tab(self, stack_widget, index, button_list):
        stack_widget.setCurrentIndex(index)
        for i, btn in enumerate(button_list):
            if i == index:
                btn.setStyleSheet("""
                    background-color: #FFFFFF; 
                    color: #7B0082; 
                    border: none; 
                    padding: 0 16px;
                    border-top-left-radius: 2px;
                    border-top-right-radius: 2px;
                """)
            else:
                btn.setStyleSheet("""
                    background-color: transparent; 
                    color: #FFFFFF; 
                    border: none; 
                    padding: 0 16px;
                """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1120, 640)
        self.setCentralWidget(EntrustDashboard())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
