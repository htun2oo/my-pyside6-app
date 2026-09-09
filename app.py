import sys
import os
from PySide6.QtCore import Qt, QSize, QByteArray
from PySide6.QtGui import QFont, QPixmap, QIcon, QImage
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget
)

# -------------------------------------------------------------
# Inline Vector/Base64 Icon Data (External File မလိုဘဲ Icon ဖော်ပြရန်)
# -------------------------------------------------------------
GRID_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="white">
<rect x="1" y="1" width="6" height="6" rx="1"/>
<rect x="9" y="1" width="6" height="6" rx="1"/>
<rect x="1" y="9" width="6" height="6" rx="1"/>
<rect x="9" y="9" width="6" height="6" rx="1"/>
</svg>"""

LIST_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="#4A5568">
<rect x="1" y="2" width="14" height="2" rx="1"/>
<rect x="1" y="7" width="14" height="2" rx="1"/>
<rect x="1" y="12" width="14" height="2" rx="1"/>
</svg>"""

REPORT_DOC_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="#E2E8F0">
<path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
</svg>"""

def get_svg_icon(svg_str):
    pixmap = QPixmap()
    pixmap.loadFromData(QByteArray(svg_str.encode('utf-8')))
    return QIcon(pixmap)

def get_svg_pixmap(svg_str):
    pixmap = QPixmap()
    pixmap.loadFromData(QByteArray(svg_str.encode('utf-8')))
    return pixmap


# -------------------------------------------------------------
# 1. View Toggle Toolbar
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
        self.grid_btn.setIcon(get_svg_icon(GRID_ICON_SVG))
        self.grid_btn.setIconSize(QSize(14, 14))

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
        self.list_btn.setIcon(get_svg_icon(LIST_ICON_SVG))
        self.list_btn.setIconSize(QSize(14, 14))

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
# 2. Report Card Widget
# -------------------------------------------------------------
class ReportCardWidget(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setFixedSize(140, 150)
        self.setStyleSheet("QFrame { background-color: #888888; border-radius: 4px; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 8)
        layout.setSpacing(4)

        img_lbl = QLabel()
        img_lbl.setFixedHeight(75)
        img_lbl.setAlignment(Qt.AlignCenter)
        img_lbl.setStyleSheet("background-color: transparent; border: none;")
        img_lbl.setPixmap(get_svg_pixmap(REPORT_DOC_SVG))

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
# 3. Main Pages & Layout
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

        # Top Bar
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

        # Content Stack
        self.content_stack = QStackedWidget()
        self.cred_page = HomeCredentialsWidget()
        self.reports_page = HomeReportsWidget()

        self.content_stack.addWidget(self.cred_page)
        self.content_stack.addWidget(self.reports_page)

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
