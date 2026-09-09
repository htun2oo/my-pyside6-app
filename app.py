import sys
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QPen, QBrush
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget
)

# -------------------------------------------------------------
# Dynamic Drawing Functions (Keeping working parts intact)
# -------------------------------------------------------------
def draw_grid_icon(size=14, color="#374151"):
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

def draw_list_icon(size=14, color="#4B5563"):
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

def draw_bar_chart_preview(width=110, height=55):
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)

    paper_rect = QRectF(5, 2, width - 10, height - 4)
    p.setBrush(QBrush(QColor("#FFFFFF")))
    p.setPen(QPen(QColor("#D1D5DB"), 1))
    p.drawRoundedRect(paper_rect, 4, 4)

    bar_color = QColor("#00875A")
    p.setBrush(QBrush(bar_color))
    p.setPen(Qt.NoPen)

    bars = [
        (22, 28, 8, 14),
        (34, 23, 8, 19),
        (46, 17, 8, 25),
        (58, 15, 8, 27),
        (70, 15, 8, 27),
        (82, 21, 8, 21)
    ]
    for x, y, w, h in bars:
        p.drawRect(x, y, w, h)

    p.setPen(QPen(QColor("#9CA3AF")))
    font = QFont("Arial", 6)
    p.setFont(font)
    p.drawText(paper_rect.adjusted(0, 36, 0, -2), Qt.AlignCenter, "Week 30, 2013")

    p.end()
    return pixmap


# -------------------------------------------------------------
# Sub-Components
# -------------------------------------------------------------
class ViewToggleToolbar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #F3F4F6; border-bottom: 1px solid #E5E7EB;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(4)

        self.grid_btn = QPushButton()
        self.grid_btn.setFixedSize(24, 22)
        self.grid_btn.setCursor(Qt.PointingHandCursor)
        self.grid_btn.setIcon(draw_grid_icon(12, "#374151"))
        self.grid_btn.setIconSize(QSize(12, 12))
        self.grid_btn.setStyleSheet("""
            QPushButton {
                background-color: #D1D5DB;
                border: 1px solid #9CA3AF;
                border-radius: 1px;
            }
        """)

        self.list_btn = QPushButton()
        self.list_btn.setFixedSize(24, 22)
        self.list_btn.setCursor(Qt.PointingHandCursor)
        self.list_btn.setIcon(draw_list_icon(12, "#4B5563"))
        self.list_btn.setIconSize(QSize(12, 12))
        self.list_btn.setStyleSheet("""
            QPushButton {
                background-color: #E5E7EB;
                border: 1px solid #D1D5DB;
                border-radius: 1px;
            }
            QPushButton:hover { background-color: #D1D5DB; }
        """)

        layout.addWidget(self.grid_btn)
        layout.addWidget(self.list_btn)
        layout.addStretch()


class ReportCardWidget(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setFixedSize(142, 135)
        self.setStyleSheet("QFrame { background-color: #838383; border-radius: 4px; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        img_lbl = QLabel()
        img_lbl.setFixedHeight(55)
        img_lbl.setAlignment(Qt.AlignCenter)
        img_lbl.setStyleSheet("background: transparent; border: none;")
        img_lbl.setPixmap(draw_bar_chart_preview(120, 55))
        layout.addWidget(img_lbl)

        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Arial", 9, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        layout.addStretch()

        run_btn = QPushButton(" ▶   Run")
        run_btn.setFont(QFont("Arial", 8, QFont.Bold))
        run_btn.setCursor(Qt.PointingHandCursor)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding-right: 4px;
            }
            QPushButton:hover { color: #E5E7EB; }
        """)
        layout.addWidget(run_btn, alignment=Qt.AlignRight)


# -------------------------------------------------------------
# Main Navigation & Pages
# -------------------------------------------------------------
class HomeCredentialsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar()
        layout.addWidget(self.toolbar)

        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(15, 15, 15, 15)
        lbl = QLabel("Credentials Workspace Area")
        lbl.setStyleSheet("color: #4B5568; font-size: 10pt;")
        c_layout.addWidget(lbl)
        layout.addWidget(content, stretch=1)


class HomeReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar()
        layout.addWidget(self.toolbar)

        content = QWidget()
        content.setStyleSheet("background-color: #FFFFFF;")
        c_layout = QHBoxLayout(content)
        c_layout.setContentsMargins(15, 15, 15, 15)
        c_layout.setSpacing(12)
        c_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        card1 = ReportCardWidget("Credentials Issued")
        card2 = ReportCardWidget("Credentials Printed")

        c_layout.addWidget(card1)
        c_layout.addWidget(card2)

        layout.addWidget(content, stretch=1)


class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -------------------------------------------------------------
        # EXACT MATCH TOP HEADER (Refined as requested)
        # -------------------------------------------------------------
        top_bar = QFrame()
        top_bar.setFixedHeight(44)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 15, 0)
        top_layout.setSpacing(12)

        # Left Section: ENTRUST Logo + Divider
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 12, 0)
        logo_layout.setSpacing(6)

        logo_hex = QLabel("⬡")
        logo_hex.setStyleSheet("color: #7B0082; font-size: 20px; font-weight: bold;")
        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Arial", 12, QFont.Bold))
        logo_text.setStyleSheet("color: #374151; letter-spacing: 0.5px;")

        logo_layout.addWidget(logo_hex)
        logo_layout.addWidget(logo_text)
        
        logo_container.setStyleSheet("border-right: 1px solid #D1D5DB;")
        top_layout.addWidget(logo_container)

        # Sub-title
        sub_text = QLabel("Adaptive Issuance™\nInstant ID")
        sub_text.setFont(QFont("Arial", 7, QFont.Bold))
        sub_text.setStyleSheet("color: #374151; border: none;")
        top_layout.addWidget(sub_text)

        top_layout.addSpacing(60)

        # Top Navigation Items
        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Arial", 9, QFont.Bold))
        home_btn.setStyleSheet("border: none; color: #374151; background: transparent; padding: 0 8px;")
        top_layout.addWidget(home_btn)

        design_btn = QPushButton("Design ▾")
        design_btn.setFont(QFont("Arial", 9, QFont.Bold))
        design_btn.setStyleSheet("border: none; color: #374151; background: transparent; padding: 0 8px;")
        top_layout.addWidget(design_btn)

        queue_btn = QPushButton("Printer Queues")
        queue_btn.setFont(QFont("Arial", 9, QFont.Bold))
        queue_btn.setStyleSheet("border: none; color: #374151; background: transparent; padding: 0 8px;")
        top_layout.addWidget(queue_btn)

        top_layout.addStretch()
        main_layout.addWidget(top_bar)

        # -------------------------------------------------------------
        # Purple Tab Navigation (Preserved as requested)
        # -------------------------------------------------------------
        purple_bar = QFrame()
        purple_bar.setFixedHeight(34)
        purple_bar.setStyleSheet("background-color: #7B0082;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(12, 0, 15, 0)

        self.cred_tab = QPushButton("Credentials")
        self.cred_tab.setFont(QFont("Arial", 9, QFont.Bold))
        self.cred_tab.setFixedHeight(34)
        self.cred_tab.setCursor(Qt.PointingHandCursor)
        self.cred_tab.clicked.connect(self.show_cred_page)

        self.reports_tab = QPushButton("Reports")
        self.reports_tab.setFont(QFont("Arial", 9, QFont.Bold))
        self.reports_tab.setFixedHeight(34)
        self.reports_tab.setCursor(Qt.PointingHandCursor)
        self.reports_tab.clicked.connect(self.show_reports_page)

        purple_layout.addWidget(self.cred_tab)
        purple_layout.addWidget(self.reports_tab)
        purple_layout.addStretch()

        login_info = QLabel("Last Login at Tue Sep 08 01:41:31 MMT 2026 from IP 192.168.99.109   admin ▾  ⚙  🔔2  ❓  ℹ")
        login_info.setStyleSheet("color: #E9D5FF; font-size: 8pt;")
        purple_layout.addWidget(login_info)

        main_layout.addWidget(purple_bar)

        # Central View Stack
        self.content_stack = QStackedWidget()
        self.cred_page = HomeCredentialsWidget()
        self.reports_page = HomeReportsWidget()

        self.content_stack.addWidget(self.cred_page)
        self.content_stack.addWidget(self.reports_page)

        main_layout.addWidget(self.content_stack, stretch=1)

        # Bottom Status Bar
        status_bar = QFrame()
        status_bar.setFixedHeight(30)
        status_bar.setStyleSheet("background-color: #F9FAFB; border-top: 1px solid #E5E7EB;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 10, 0)
        status_layout.addStretch()

        queue_status_btn = QPushButton(" 🖨   Printer Queue Status")
        queue_status_btn.setFont(QFont("Arial", 8, QFont.Bold))
        queue_status_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0E7FF;
                color: #1E40AF;
                border: 1px solid #C7D2FE;
                border-radius: 2px;
                padding: 3px 10px;
            }
        """)
        status_layout.addWidget(queue_status_btn)
        main_layout.addWidget(status_bar)

        self.show_reports_page()

    def show_cred_page(self):
        self.content_stack.setCurrentIndex(0)
        self.cred_tab.setStyleSheet("""
            background-color: #FFFFFF; color: #7B0082; border: none;
            padding: 0px 16px; border-top-left-radius: 3px; border-top-right-radius: 3px;
        """)
        self.reports_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0px 16px;")

    def show_reports_page(self):
        self.content_stack.setCurrentIndex(1)
        self.reports_tab.setStyleSheet("""
            background-color: #FFFFFF; color: #7B0082; border: none;
            padding: 0px 16px; border-top-left-radius: 3px; border-top-right-radius: 3px;
        """)
        self.cred_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0px 16px;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1100, 650)
        self.setCentralWidget(EntrustDashboard())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
