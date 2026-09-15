import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView
)

class EntrustDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #FFFFFF;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top White Header Bar
        header_bar = QFrame()
        header_bar.setFixedHeight(50)
        header_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB;")
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(15, 0, 15, 0)
        header_layout.setSpacing(10)

        logo_label = QLabel("⬡ ENTRUST")
        logo_label.setFont(QFont("Arial", 14, QFont.Bold))
        logo_label.setStyleSheet("color: #7B0082;")
        header_layout.addWidget(logo_label)

        sub_title = QLabel("Adaptive Issuance™\nInstant ID")
        sub_title.setFont(QFont("Arial", 8))
        sub_title.setStyleSheet("color: #4B5563;")
        header_layout.addWidget(sub_title)

        header_layout.addStretch()

        # Navigation Buttons (Now grouped to the right)
        nav_frame = QFrame()
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(5)

        self.home_btn = QPushButton("Home")
        self.design_btn = QPushButton("Design")
        self.queues_btn = QPushButton("Printer Queues")

        for btn in [self.home_btn, self.design_btn, self.queues_btn]:
            btn.setFont(QFont("Arial", 9, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #111827;
                    border: none;
                    padding: 8px 12px;
                }
                QPushButton:hover {
                    color: #7B0082;
                }
            """)
        
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.design_btn)
        nav_layout.addWidget(self.queues_btn)
        
        # Spacer before buttons effectively moves them to the right edge
        # BUT user requested them Left of the vertical separator line (the right panel boundary)
        # In this layout, the Right stretch pushes them against the separator.
        
        header_layout.addWidget(nav_frame)

        # Right-side icons (admin dropdown, notifications, help, info)
        icon_frame = QFrame()
        icon_layout = QHBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(12)

        user_label = QLabel("admin")
        user_label.setStyleSheet("font-weight: bold; color: #374151;")
        
        # Simplified icons for demo purposes
        icons = ["⚙", "🔔", "❓", "ℹ"]
        for icon_str in icons:
            lbl = QLabel(icon_str)
            lbl.setFont(QFont("Arial", 11))
            lbl.setStyleSheet("color: #4B5563;")
            icon_layout.addWidget(lbl)
        
        icon_layout.insertWidget(0, user_label)
        header_layout.addWidget(icon_frame)

        main_layout.addWidget(header_bar)

        # 2. Purple Banner Section
        purple_banner = QFrame()
        purple_banner.setFixedHeight(40)
        purple_banner.setStyleSheet("background-color: #7B0082; border-bottom: 1px solid #D1D5DB;")
        banner_layout = QHBoxLayout(purple_banner)
        banner_layout.setContentsMargins(15, 0, 15, 0)
        banner_layout.setSpacing(10)

        title_lbl = QLabel("Credential Designs")
        title_lbl.setFont(QFont("Arial", 11, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF;")
        banner_layout.addWidget(title_lbl)

        last_login_lbl = QLabel("Last Login at Wed Sep 09 18:33:05 MMT 2026 from IP 192.168.56.1")
        last_login_lbl.setFont(QFont("Arial", 8))
        last_login_lbl.setStyleSheet("color: #D1D5DB;")
        banner_layout.addWidget(last_login_lbl)

        main_layout.addWidget(purple_banner)

        # 3. Middle Body Section (Table, Pagination)
        body_layout = QHBoxLayout()
        main_layout.addLayout(body_layout)

        # 3a. Table and Actions Area (occupies remaining width)
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #FFFFFF;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(15, 15, 15, 0)
        body_layout.addWidget(content_frame, stretch=1)

        # Action Buttons (Create, Search)
        action_layout = QHBoxLayout()
        create_btn = QPushButton("+ Create")
        create_btn.setStyleSheet("""
            background-color: #7B0082;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        """)
        action_layout.addWidget(create_btn)
        action_layout.addStretch()
        search_lbl = QLabel("🔍 Search:")
        search_lbl.setStyleSheet("color: #4B5563;")
        action_layout.addWidget(search_lbl)
        content_layout.addLayout(action_layout)

        # Table Control
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Description", "Actions"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table.setRowCount(1)
        # Empty row data
        empty_item = QTableWidgetItem("No data available in table")
        empty_item.setTextAlignment(Qt.AlignCenter)
        empty_item.setFlags(Qt.NoItemFlags)
        self.table.setItem(0, 0, empty_item)
        self.table.setSpan(0, 0, 1, 4)

        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #D1D5DB;
                gridline-color: #E5E7EB;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #D1D5DB;
                font-weight: bold;
                color: #374151;
            }
        """)
        content_layout.addWidget(self.table)

        # Pagination controls
        pagination_layout = QHBoxLayout()
        pagination_layout.setContentsMargins(0, 5, 0, 5)
        pagination_lbl = QLabel("Showing 0 to 0 of 0 entries")
        pagination_lbl.setStyleSheet("color: #4B5563;")
        pagination_layout.addWidget(pagination_lbl)
        pagination_layout.addStretch()
        prev_btn = QPushButton("Previous")
        next_btn = QPushButton("Next")
        for btn in [prev_btn, next_btn]:
             btn.setStyleSheet("padding: 5px 10px; border: 1px solid #D1D5DB; background-color: white; color: #374151;")
        pagination_layout.addWidget(prev_btn)
        pagination_layout.addWidget(next_btn)
        content_layout.addLayout(pagination_layout)
        
        # Create horizontal separator line at the bottom boundary of the table area
        horiz_sep = QFrame()
        horiz_sep.setFrameShape(QFrame.HLine)
        horiz_sep.setStyleSheet("color: #D1D5DB;")
        content_layout.addWidget(horiz_sep)
        
        content_layout.addStretch()

        # 3b. Empty Right Panel (User interface boundary)
        right_panel = QFrame()
        right_panel.setFixedWidth(200) # Give it some width to act as user interface boundary
        right_panel.setStyleSheet("border-left: 1px solid #D1D5DB; background-color: #FFFFFF;")
        body_layout.addWidget(right_panel)

        # 4. Status Bar (Bottom fixed bar)
        status_bar = QFrame()
        status_bar.setFixedHeight(30)
        status_bar.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #D1D5DB;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(15, 0, 0, 0)
        
        queue_status_lbl = QLabel("🖨️ Printer Queue Status")
        queue_status_lbl.setFont(QFont("Arial", 9))
        queue_status_lbl.setStyleSheet("color: #111827; font-weight: bold;")
        status_layout.addWidget(queue_status_lbl)
        status_layout.addStretch()
        
        main_layout.addWidget(status_bar)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EntrustDashboard()
    window.show()
    sys.exit(app.exec())
