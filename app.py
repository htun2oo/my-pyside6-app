import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView, QScrollBar
)

# -------------------------------------------------------------
# Icons Drawing Functions
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


# -------------------------------------------------------------
# View Toggle Toolbar Component
# -------------------------------------------------------------
class ViewToggleToolbar(QFrame):
    def __init__(self, on_grid_click=None, on_list_click=None, is_list_active=True):
        super().__init__()
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #D1D5DB;
            }
        """)
        
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

        if is_list_active:
            self.grid_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; border: 1px solid #9CA3AF; border-radius: 1px; }")
            self.list_btn.setStyleSheet("QPushButton { background-color: #C5D1DF; border: 1px solid #4B5563; border-radius: 1px; }")
        else:
            self.grid_btn.setStyleSheet("QPushButton { background-color: #C5D1DF; border: 1px solid #4B5563; border-radius: 1px; }")
            self.list_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; border: 1px solid #9CA3AF; border-radius: 1px; }")

        if on_grid_click:
            self.grid_btn.clicked.connect(on_grid_click)
        if on_list_click:
            self.list_btn.clicked.connect(on_list_click)

        layout.addWidget(self.grid_btn)
        layout.addWidget(self.list_btn)
        layout.addStretch()


# -------------------------------------------------------------
# Credentials List Table View Widget (Image Exact Match)
# -------------------------------------------------------------
class CredentialsListViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Main Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(1)
        self.table.setFixedHeight(68)
        self.table.setHorizontalHeaderLabels([
            "Credential Design Name", 
            "▲   Workflow Name", 
            "⬍   Workflow Notes", 
            "Actions"
        ])

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: none;
                gridline-color: #F3F4F6;
            }
            QHeaderView::section {
                background-color: #FFFFFF;
                color: #374151;
                font-family: Arial;
                font-size: 8.5pt;
                padding: 4px 8px;
                border: none;
                border-bottom: 1px solid #D1D5DB;
                border-right: 1px solid #E5E7EB;
                text-align: left;
            }
            QHeaderView::section:last {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F9FAFB, stop:1 #E5E7EB);
            }
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(3, 95)

        empty_item = QTableWidgetItem("No data is available.")
        empty_item.setTextAlignment(Qt.AlignCenter)
        empty_item.setFlags(Qt.NoItemFlags)
        
        self.table.setItem(0, 0, empty_item)
        self.table.setSpan(0, 0, 1, 4)
        self.table.setRowHeight(0, 38)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

        # 2. Pagination Bar
        pagination_bar = QFrame()
        pagination_bar.setFixedHeight(34)
        pagination_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #EEEEEE, stop:1 #D6D6D6);
                border-top: 1px solid #C0C0C0;
                border-bottom: 1px solid #C0C0C0;
            }
        """)
        p_layout = QHBoxLayout(pagination_bar)
        p_layout.setContentsMargins(12, 0, 12, 0)

        entries_lbl = QLabel("Showing 0 - 0 of 0 entries")
        entries_lbl.setFont(QFont("Arial", 8.5))
        entries_lbl.setStyleSheet("color: #333333; border: none; background: transparent;")

        prev_btn = QPushButton("Previous")
        prev_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
        prev_btn.setStyleSheet("border: none; color: #555555; background: transparent;")

        next_btn = QPushButton("Next")
        next_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
        next_btn.setStyleSheet("border: none; color: #555555; background: transparent; margin-left: 12px;")

        p_layout.addWidget(entries_lbl)
        p_layout.addStretch()
        p_layout.addWidget(prev_btn)
        p_layout.addWidget(next_btn)

        layout.addWidget(pagination_bar)

        # 3. Middle Blank Workspace Area
        workspace_area = QWidget()
        workspace_area.setStyleSheet("background-color: #FFFFFF;")
        layout.addWidget(workspace_area, stretch=1)

        # 4. Thin Scrollbar at Bottom Edge
        scroll_container = QWidget()
        scroll_container.setFixedHeight(22)
        scroll_layout = QHBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_bar = QScrollBar(Qt.Horizontal)
        scroll_bar.setRange(0, 100)
        scroll_bar.setValue(0)
        scroll_bar.setStyleSheet("""
            QScrollBar:horizontal {
                height: 12px;
                background: #FFFFFF;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background: #888888;
                min-width: 400px;
                border-radius: 0px;
            }
            QScrollBar::add-line:horizontal {
                border: none;
                background: #FFFFFF;
                width: 10px;
                subcontrol-position: right;
            }
            QScrollBar::sub-line:horizontal {
                border: none;
                background: #FFFFFF;
                width: 10px;
                subcontrol-position: left;
            }
        """)
        scroll_layout.addWidget(scroll_bar)
        layout.addWidget(scroll_container)


# -------------------------------------------------------------
# Home Credentials Workspace Container
# -------------------------------------------------------------
class HomeCredentialsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar(
            on_grid_click=self.show_grid_view,
            on_list_click=self.show_list_view,
            is_list_active=True
        )
        layout.addWidget(self.toolbar)

        self.view_stack = QStackedWidget()
        
        grid_view = QWidget()
        grid_view.setStyleSheet("background-color: #FFFFFF;")
        
        self.list_view = CredentialsListViewWidget()

        self.view_stack.addWidget(grid_view)
        self.view_stack.addWidget(self.list_view)
        
        self.view_stack.setCurrentIndex(1)

        layout.addWidget(self.view_stack, stretch=1)

    def show_grid_view(self):
        self.view_stack.setCurrentIndex(0)
        self.toolbar.grid_btn.setStyleSheet("QPushButton { background-color: #C5D1DF; border: 1px solid #4B5563; border-radius: 1px; }")
        self.toolbar.list_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; border: 1px solid #9CA3AF; border-radius: 1px; }")

    def show_list_view(self):
        self.view_stack.setCurrentIndex(1)
        self.toolbar.grid_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; border: 1px solid #9CA3AF; border-radius: 1px; }")
        self.toolbar.list_btn.setStyleSheet("QPushButton { background-color: #C5D1DF; border: 1px solid #4B5563; border-radius: 1px; }")


class HomeReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar(is_list_active=False)
        layout.addWidget(self.toolbar)

        content = QWidget()
        content.setStyleSheet("background-color: #FFFFFF;")
        layout.addWidget(content, stretch=1)


# -------------------------------------------------------------
# Main Dashboard Window
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top White Header Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(42)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 15, 0)
        top_layout.setSpacing(8)

        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 10, 0)
        logo_layout.setSpacing(6)

        logo_hex = QLabel("⬡")
        logo_hex.setStyleSheet("color: #7B0082; font-size: 19px; font-weight: bold;")
        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Arial", 11, QFont.Bold))
        logo_text.setStyleSheet("color: #2D3748; letter-spacing: 0.5px;")

        logo_layout.addWidget(logo_hex)
        logo_layout.addWidget(logo_text)
        logo_container.setStyleSheet("border-right: 1px solid #D1D5DB;")
        top_layout.addWidget(logo_container)

        sub_text = QLabel("Adaptive Issuance™\nInstant ID")
        sub_text.setFont(QFont("Arial", 7, QFont.Bold))
        sub_text.setStyleSheet("color: #4A5568; border: none;")
        top_layout.addWidget(sub_text)

        top_layout.addSpacing(40)

        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
        home_btn.setStyleSheet("border: none; color: #1A202C; background: transparent; padding: 0 6px;")
        top_layout.addWidget(home_btn)

        design_btn = QPushButton("Design ▾")
        design_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
        design_btn.setStyleSheet("border: none; color: #1A202C; background: transparent; padding: 0 6px;")
        top_layout.addWidget(design_btn)

        queue_btn = QPushButton("Printer Queues")
        queue_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
        queue_btn.setStyleSheet("border: none; color: #1A202C; background: transparent; padding: 0 6px;")
        top_layout.addWidget(queue_btn)

        top_layout.addStretch()

        user_info = QLabel("admin ▾   ⚙ ▾   🔔²   ❓   ℹ")
        user_info.setStyleSheet("color: #2D3748; font-size: 8.5pt; font-weight: bold;")
        top_layout.addWidget(user_info)

        main_layout.addWidget(top_bar)

        # 2. Purple Header Bar with Pattern & Last Login Text
        purple_bar = QFrame()
        purple_bar.setFixedHeight(34)
        purple_bar.setStyleSheet("background-color: #7B0082;")

        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(10, 0, 15, 0)

        self.cred_tab = QPushButton("Credentials")
        self.cred_tab.setFont(QFont("Arial", 8.5, QFont.Bold))
        self.cred_tab.setFixedHeight(34)
        self.cred_tab.setCursor(Qt.PointingHandCursor)
        self.cred_tab.clicked.connect(self.show_cred_page)

        self.reports_tab = QPushButton("Reports")
        self.reports_tab.setFont(QFont("Arial", 8.5, QFont.Bold))
        self.reports_tab.setFixedHeight(34)
        self.reports_tab.setCursor(Qt.PointingHandCursor)
        self.reports_tab.clicked.connect(self.show_reports_page)

        purple_layout.addWidget(self.cred_tab)
        purple_layout.addWidget(self.reports_tab)
        purple_layout.addStretch()

        last_login_lbl = QLabel("Last Login at Wed Sep 09 15:11:29 MMT 2026 from IP 192.168.56.1")
        last_login_lbl.setFont(QFont("Arial", 8))
        last_login_lbl.setStyleSheet("color: #E9D5FF; background: transparent; border: none; margin-right: 12px;")
        purple_layout.addWidget(last_login_lbl)

        main_layout.addWidget(purple_bar)

        # 3. Content Body
        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.content_stack = QStackedWidget()
        self.cred_page = HomeCredentialsWidget()
        self.reports_page = HomeReportsWidget()

        self.content_stack.addWidget(self.cred_page)
        self.content_stack.addWidget(self.reports_page)

        body_layout.addWidget(self.content_stack, stretch=1)

        # Right Blank Side Panel
        right_panel_line = QFrame()
        right_panel_line.setFixedWidth(200)
        right_panel_line.setStyleSheet("border-left: 1px solid #D1D5DB; background-color: #FFFFFF;")
        body_layout.addWidget(right_panel_line)

        main_layout.addWidget(body_container, stretch=1)

        # 4. Bottom Printer Queue Bar
        status_bar = QFrame()
        status_bar.setFixedHeight(30)
        status_bar.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #D1D5DB;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(0)

        status_layout.addStretch()

        queue_status_btn = QPushButton(" 🖨   Printer Queue Status")
        queue_status_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
        queue_status_btn.setFixedHeight(30)
        queue_status_btn.setFixedWidth(200)
        queue_status_btn.setCursor(Qt.PointingHandCursor)
        queue_status_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E2ECF7, stop:1 #BCCFE3);
                color: #0F172A;
                border: none;
                border-left: 1px solid #D1D5DB;
                padding: 0px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D2ECF7, stop:1 #ACCDE3);
            }
        """)
        status_layout.addWidget(queue_status_btn)

        main_layout.addWidget(status_bar)

        self.show_cred_page()

    def show_cred_page(self):
        self.content_stack.setCurrentIndex(0)
        self.cred_tab.setStyleSheet("""
            background-color: #FFFFFF; color: #7B0082; border: none;
            padding: 0px 16px; border-top-left-radius: 2px; border-top-right-radius: 2px;
        """)
        self.reports_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0px 16px;")

    def show_reports_page(self):
        self.content_stack.setCurrentIndex(1)
        self.reports_tab.setStyleSheet("""
            background-color: #FFFFFF; color: #7B0082; border: none;
            padding: 0px 16px; border-top-left-radius: 2px; border-top-right-radius: 2px;
        """)
        self.cred_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0px 16px;")


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
