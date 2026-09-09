import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QPen
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView, QScrollBar
)

# -------------------------------------------------------------
# Custom Icon Helper Functions
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
    
    # Document outline
    p.setPen(QPen(QColor("#D1D5DB"), 1))
    p.drawRect(2, 2, 95, 55)
    
    # Green Bar Chart
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
# Toolbar Component
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
# Reports - Grid View Widget (Image 1)
# -------------------------------------------------------------
class ReportCardWidget(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setFixedSize(120, 115)
        self.setStyleSheet("""
            QFrame {
                background-color: #888888;
                border-radius: 4px;
                border: 1px solid #777777;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 6)
        layout.setSpacing(4)

        # Image Thumbnail
        img_lbl = QLabel()
        img_lbl.setPixmap(create_report_thumbnail())
        img_lbl.setAlignment(Qt.AlignCenter)
        img_lbl.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(img_lbl)

        # Title Label
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Arial", 8, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        # Run Button
        run_btn = QPushButton("  ▶  Run")
        run_btn.setFont(QFont("Arial", 8, QFont.Bold))
        run_btn.setFixedHeight(20)
        run_btn.setCursor(Qt.PointingHandCursor)
        run_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FFFFFF;
                border: none;
                text-align: right;
                padding-right: 10px;
            }
            QPushButton:hover { color: #E2E8F0; }
        """)
        layout.addWidget(run_btn)


class ReportsGridViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        card1 = ReportCardWidget("Credentials Issued")
        card2 = ReportCardWidget("Credentials Printed")

        layout.addWidget(card1)
        layout.addWidget(card2)


# -------------------------------------------------------------
# Reports - List View Widget (Image 2)
# -------------------------------------------------------------
class ReportsListViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(2)
        self.table.setFixedHeight(105)
        self.table.setHorizontalHeaderLabels([
            "Name", 
            "▲   Type", 
            "⬍   Description", 
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
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(3, 80)

        # Row 1 Data
        item1_0 = QTableWidgetItem("Credentials Issued")
        item1_1 = QTableWidgetItem("Stock")
        item1_2 = QTableWidgetItem("A report showing the credentials issued by each user")
        item1_3 = QTableWidgetItem("  ►")
        item1_3.setForeground(QColor("#4F46E5"))
        item1_3.setFont(QFont("Arial", 10, QFont.Bold))

        # Row 2 Data
        item2_0 = QTableWidgetItem("Credentials Printed")
        item2_1 = QTableWidgetItem("Stock")
        item2_2 = QTableWidgetItem("A report showing the credentials personalized by each printer")
        item2_3 = QTableWidgetItem("  ►")
        item2_3.setForeground(QColor("#4F46E5"))
        item2_3.setFont(QFont("Arial", 10, QFont.Bold))

        for item in [item1_0, item1_1, item1_2, item1_3, item2_0, item2_1, item2_2, item2_3]:
            item.setFlags(Qt.ItemIsEnabled)

        self.table.setItem(0, 0, item1_0)
        self.table.setItem(0, 1, item1_1)
        self.table.setItem(0, 2, item1_2)
        self.table.setItem(0, 3, item1_3)

        self.table.setItem(1, 0, item2_0)
        self.table.setItem(1, 1, item2_1)
        self.table.setItem(1, 2, item2_2)
        self.table.setItem(1, 3, item2_3)

        self.table.setRowHeight(0, 36)
        self.table.setRowHeight(1, 36)
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

        entries_lbl = QLabel("Showing 1 - 2 of 2 entries")
        entries_lbl.setFont(QFont("Arial", 8.5))
        entries_lbl.setStyleSheet("color: #333333; border: none; background: transparent;")

        p_layout.addWidget(entries_lbl)
        p_layout.addStretch()

        btn_first = QPushButton("First")
        btn_prev = QPushButton("Previous")
        btn_num = QPushButton("1")
        btn_next = QPushButton("Next")
        btn_last = QPushButton("Last")

        btn_num.setFixedSize(22, 22)
        btn_num.setStyleSheet("background-color: #FFFFFF; border: 1px solid #A0A0A0; font-weight: bold;")

        for btn in [btn_first, btn_prev, btn_next, btn_last]:
            btn.setFont(QFont("Arial", 8.5))
            btn.setStyleSheet("border: none; color: #555555; background: transparent; padding: 0 4px;")

        p_layout.addWidget(btn_first)
        p_layout.addWidget(btn_prev)
        p_layout.addWidget(btn_num)
        p_layout.addWidget(btn_next)
        p_layout.addWidget(btn_last)

        layout.addWidget(pagination_bar)

        # 3. Workspace Fill
        workspace_area = QWidget()
        workspace_area.setStyleSheet("background-color: #FFFFFF;")
        layout.addWidget(workspace_area, stretch=1)

        # 4. Scrollbar
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
            }
        """)
        scroll_layout.addWidget(scroll_bar)
        layout.addWidget(scroll_container)


# -------------------------------------------------------------
# Reports Main Container
# -------------------------------------------------------------
class HomeReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar(
            on_grid_click=self.show_grid_view,
            on_list_click=self.show_list_view,
            is_grid_active=True
        )
        layout.addWidget(self.toolbar)

        self.view_stack = QStackedWidget()
        self.grid_view = ReportsGridViewWidget()
        self.list_view = ReportsListViewWidget()

        self.view_stack.addWidget(self.grid_view)
        self.view_stack.addWidget(self.list_view)

        layout.addWidget(self.view_stack, stretch=1)

    def show_grid_view(self):
        self.view_stack.setCurrentIndex(0)
        self.toolbar.set_active_state(is_grid_active=True)

    def show_list_view(self):
        self.view_stack.setCurrentIndex(1)
        self.toolbar.set_active_state(is_grid_active=False)


# -------------------------------------------------------------
# Credentials Tab Wrapper
# -------------------------------------------------------------
class HomeCredentialsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar(is_grid_active=False)
        layout.addWidget(self.toolbar)

        blank = QWidget()
        blank.setStyleSheet("background-color: #FFFFFF;")
        layout.addWidget(blank, stretch=1)


# -------------------------------------------------------------
# App Main Window
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar
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

        for name in ["Home", "Design ▾", "Printer Queues"]:
            btn = QPushButton(name)
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setStyleSheet("border: none; color: #1A202C; background: transparent; padding: 0 6px;")
            top_layout.addWidget(btn)

        top_layout.addStretch()

        user_info = QLabel("admin ▾   ⚙ ▾   🔔²   ❓   ℹ")
        user_info.setStyleSheet("color: #2D3748; font-size: 8.5pt; font-weight: bold;")
        top_layout.addWidget(user_info)

        main_layout.addWidget(top_bar)

        # Purple Navigation
        purple_bar = QFrame()
        purple_bar.setFixedHeight(34)
        purple_bar.setStyleSheet("background-color: #7B0082;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(10, 0, 15, 0)

        self.cred_tab = QPushButton("Credentials")
        self.reports_tab = QPushButton("Reports")

        for btn in [self.cred_tab, self.reports_tab]:
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setFixedHeight(34)
            btn.setCursor(Qt.PointingHandCursor)

        self.cred_tab.clicked.connect(self.show_cred_page)
        self.reports_tab.clicked.connect(self.show_reports_page)

        purple_layout.addWidget(self.cred_tab)
        purple_layout.addWidget(self.reports_tab)
        purple_layout.addStretch()

        last_login = QLabel("Last Login at Wed Sep 09 18:33:05 MMT 2026 from IP 192.168.56.1")
        last_login.setFont(QFont("Arial", 8))
        last_login.setStyleSheet("color: #E9D5FF; border: none;")
        purple_layout.addWidget(last_login)

        main_layout.addWidget(purple_bar)

        # Main Body
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

        right_panel = QFrame()
        right_panel.setFixedWidth(200)
        right_panel.setStyleSheet("border-left: 1px solid #D1D5DB; background-color: #FFFFFF;")
        body_layout.addWidget(right_panel)

        main_layout.addWidget(body_container, stretch=1)

        # Bottom Status Bar
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

        # Show Reports Page by Default as requested
        self.show_reports_page()

    def show_cred_page(self):
        self.content_stack.setCurrentIndex(0)
        self.cred_tab.setStyleSheet("background-color: #FFFFFF; color: #7B0082; border: none; padding: 0 16px;")
        self.reports_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0 16px;")

    def show_reports_page(self):
        self.content_stack.setCurrentIndex(1)
        self.reports_tab.setStyleSheet("background-color: #FFFFFF; color: #7B0082; border: none; padding: 0 16px;")
        self.cred_tab.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0 16px;")


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
