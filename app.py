import sys
import os
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QPen
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget
)

# -------------------------------------------------------------
# 1. GitHub Actions / PyInstaller Compatible Path Resolver
# -------------------------------------------------------------
def get_resource_path(relative_path):
    """ PyInstaller / Executable build သောအခါ temp path ကို တိကျစွာ ရယူပေးသည့် Function """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

GRID_ICON_PATH = get_resource_path(os.path.join("assets", "icons", "grid.png"))
LIST_ICON_PATH = get_resource_path(os.path.join("assets", "icons", "list.png"))
REPORT_PREVIEW_PATH = get_resource_path(os.path.join("assets", "icons", "report.png"))


# -------------------------------------------------------------
# 2. Vector Icon Fallbacks (Image File မရှိပါက ပေါ်လာစေရန်)
# -------------------------------------------------------------
def draw_fallback_grid_icon(color="#2F3E46"):
    pix = QPixmap(16, 16)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setBrush(QColor(color))
    p.setPen(Qt.NoPen)
    p.drawRect(1, 1, 6, 6)
    p.drawRect(9, 1, 6, 6)
    p.drawRect(1, 9, 6, 6)
    p.drawRect(9, 9, 6, 6)
    p.end()
    return QIcon(pix)

def draw_fallback_list_icon(color="#2D3748"):
    pix = QPixmap(16, 16)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    pen = QPen(QColor(color), 2)
    pen.setCapStyle(Qt.RoundCap)
    p.setPen(pen)
    p.drawLine(2, 3, 14, 3)
    p.drawLine(2, 8, 14, 8)
    p.drawLine(2, 13, 14, 13)
    p.end()
    return QIcon(pix)


# -------------------------------------------------------------
# 3. View Toggle Toolbar
# -------------------------------------------------------------
class ViewToggleToolbar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(34)
        self.setStyleSheet("background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(4)

        # Grid Button
        self.grid_btn = QPushButton()
        self.grid_btn.setFixedSize(28, 26)
        self.grid_btn.setCursor(Qt.PointingHandCursor)
        
        if os.path.exists(GRID_ICON_PATH):
            self.grid_btn.setIcon(QIcon(GRID_ICON_PATH))
            self.grid_btn.setIconSize(QSize(16, 16))
        else:
            self.grid_btn.setIcon(draw_fallback_grid_icon("#FFFFFF"))

        self.grid_btn.setStyleSheet("""
            QPushButton {
                background-color: #2F3E46;
                border: 1px solid #1D2A30;
                border-radius: 2px;
            }
        """)

        # List Button
        self.list_btn = QPushButton()
        self.list_btn.setFixedSize(28, 26)
        self.list_btn.setCursor(Qt.PointingHandCursor)
        
        if os.path.exists(LIST_ICON_PATH):
            self.list_btn.setIcon(QIcon(LIST_ICON_PATH))
            self.list_btn.setIconSize(QSize(16, 16))
        else:
            self.list_btn.setIcon(draw_fallback_list_icon("#2D3748"))

        self.list_btn.setStyleSheet("""
            QPushButton {
                background-color: #CBD5E0;
                border: 1px solid #A0AEC0;
                border-radius: 2px;
            }
            QPushButton:hover { background-color: #E2E8F0; }
        """)

        layout.addWidget(self.grid_btn)
        layout.addWidget(self.list_btn)
        layout.addStretch()


# -------------------------------------------------------------
# 4. Report Card Component
# -------------------------------------------------------------
class ReportCardWidget(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setFixedSize(140, 150)
        self.setStyleSheet("QFrame { background-color: #888888; border-radius: 4px; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 8)
        layout.setSpacing(6)

        img_lbl = QLabel()
        img_lbl.setFixedHeight(80)
        img_lbl.setAlignment(Qt.AlignCenter)
        img_lbl.setStyleSheet("background-color: transparent; border: none;")

        if os.path.exists(REPORT_PREVIEW_PATH):
            pixmap = QPixmap(REPORT_PREVIEW_PATH)
            img_lbl.setPixmap(pixmap.scaled(120, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            img_lbl.setText("📄\nReport Preview")
            img_lbl.setStyleSheet("color: white; font-size: 9pt; font-weight: bold;")

        layout.addWidget(img_lbl)

        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        run_btn = QPushButton(" ▶  Run")
        run_btn.setFont(QFont("Segoe UI", 8.5))
        run_btn.setCursor(Qt.PointingHandCursor)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
            }
            QPushButton:hover { color: #E2E8F0; }
        """)
        layout.addWidget(run_btn, alignment=Qt.AlignRight)


# -------------------------------------------------------------
# 5. Workspaces & Main Window
# -------------------------------------------------------------
class HomeCredentialsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar()
        layout.addWidget(self.toolbar)

        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        info_lbl = QLabel("Home > Credentials Workspace Area")
        info_lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        info_lbl.setStyleSheet("color: #4A5568; font-size: 11pt;")
        content_layout.addWidget(info_lbl)
        
        layout.addWidget(content_area, stretch=1)


class HomeReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar()
        layout.addWidget(self.toolbar)

        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)
        content_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        card1 = ReportCardWidget("Credentials Issued")
        card2 = ReportCardWidget("Credentials Printed")

        content_layout.addWidget(card1)
        content_layout.addWidget(card2)

        layout.addWidget(content_area, stretch=1)


class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(54)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #DCDCDC;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(18, 0, 20, 0)

        logo_icon = QLabel("⬡")
        logo_icon.setStyleSheet("color: #7A0A8A; font-size: 24px; font-weight: bold;")
        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Segoe UI", 14, QFont.Bold))
        logo_text.setStyleSheet("color: #4A4A4A; letter-spacing: 1.5px;")
        
        top_layout.addWidget(logo_icon)
        top_layout.addWidget(logo_text)

        sub_title = QLabel("  |  Adaptive Issuance™\n     Instant ID")
        sub_title.setFont(QFont("Segoe UI", 8, QFont.Bold))
        sub_title.setStyleSheet("color: #333333;")
        top_layout.addWidget(sub_title)
        top_layout.addSpacing(40)

        self.home_btn = QPushButton("Home")
        self.home_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.home_btn.setStyleSheet("border: none; color: #7A0A8A; background: transparent;")
        top_layout.addWidget(self.home_btn)

        design_btn = QPushButton("Design ▾")
        design_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        design_btn.setStyleSheet("border: none; color: #222222; background: transparent;")
        top_layout.addWidget(design_btn)

        printer_btn = QPushButton("Printer Queues")
        printer_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        printer_btn.setStyleSheet("border: none; color: #222222; background: transparent;")
        top_layout.addWidget(printer_btn)

        top_layout.addStretch()
        main_layout.addWidget(top_bar)

        # Purple Tab Bar
        purple_bar = QFrame()
        purple_bar.setFixedHeight(36)
        purple_bar.setStyleSheet("background-color: #7A0A8A;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        self.cred_tab = QPushButton("Credentials")
        self.cred_tab.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.cred_tab.setFixedHeight(36)
        self.cred_tab.setCursor(Qt.PointingHandCursor)
        self.cred_tab.clicked.connect(self.show_cred_page)

        self.reports_tab = QPushButton("Reports")
        self.reports_tab.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.reports_tab.setFixedHeight(36)
        self.reports_tab.setCursor(Qt.PointingHandCursor)
        self.reports_tab.clicked.connect(self.show_reports_page)

        purple_layout.addWidget(self.cred_tab)
        purple_layout.addWidget(self.reports_tab)
        purple_layout.addStretch()

        login_info = QLabel("Last Login at Wed Sep 09 10:18:38 MMT 2026 from IP 192.168.56.1  admin ▾")
        login_info.setStyleSheet("color: #DDA0DD; font-size: 8pt;")
        purple_layout.addWidget(login_info)

        main_layout.addWidget(purple_bar)

        # Workspace Stack
        self.content_stack = QStackedWidget()
        self.cred_page = HomeCredentialsWidget()
        self.reports_page = HomeReportsWidget()

        self.content_stack.addWidget(self.cred_page)    # Index 0
        self.content_stack.addWidget(self.reports_page) # Index 1

        main_layout.addWidget(self.content_stack, stretch=1)

        # Status Bar
        status_bar = QFrame()
        status_bar.setFixedHeight(32)
        status_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 15, 0)
        status_layout.addStretch()

        queue_btn = QPushButton(" Printer Queue Status")
        queue_btn.setFont(QFont("Segoe UI", 8.5, QFont.Bold))
        queue_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #E2E8F0);
                color: #1E3A8A;
                border: 1px solid #CBD5E0;
                border-radius: 3px;
                padding: 4px 12px;
            }
        """)
        status_layout.addWidget(queue_btn)
        main_layout.addWidget(status_bar)

        self.show_reports_page()

    def show_cred_page(self):
        self.content_stack.setCurrentIndex(0)
        self.cred_tab.setStyleSheet("""
            background-color: #FFFFFF; color: #7A0A8A; border: none;
            padding: 0px 18px; border-top-left-radius: 3px; border-top-right-radius: 3px;
        """)
        self.reports_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0px 18px;")

    def show_reports_page(self):
        self.content_stack.setCurrentIndex(1)
        self.reports_tab.setStyleSheet("""
            background-color: #FFFFFF; color: #7A0A8A; border: none;
            padding: 0px 18px; border-top-left-radius: 3px; border-top-right-radius: 3px;
        """)
        self.cred_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0px 18px;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1280, 720)
        self.setCentralWidget(EntrustDashboard())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
