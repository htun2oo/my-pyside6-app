import sys
import os
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QToolButton,
    QComboBox, QCheckBox, QScrollArea
)

# Sprite Sheet မှ Icon များကို Crop လုပ်ထုတ်ယူသည့် Helper Function
def get_sprite_icon(sprite_pixmap, x, y, width=28, height=28):
    if sprite_pixmap.isNull():
        return QIcon()
    cropped = sprite_pixmap.copy(QRect(x, y, width, height))
    return QIcon(cropped)


# -------------------------------------------------------------
# 1. View Mode Toggle Buttons Component (Grid vs List Buttons)
# -------------------------------------------------------------
class ViewToggleToolbar(QFrame):
    def __init__(self, sprite_pixmap):
        super().__init__()
        self.setFixedHeight(34)
        self.setStyleSheet("background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(2)

        # sprite_button_2.png ထဲမှ Icon များ၏ Coord (Grid & List Icon)
        grid_icon = get_sprite_icon(sprite_pixmap, 495, 270, 32, 32)
        list_icon = get_sprite_icon(sprite_pixmap, 598, 270, 32, 32)

        # Grid View Button (Active Dark Blue Style)
        self.grid_btn = QPushButton()
        self.grid_btn.setFixedSize(28, 26)
        self.grid_btn.setCursor(Qt.PointingHandCursor)
        if not grid_icon.isNull():
            self.grid_btn.setIcon(grid_icon)
        else:
            self.grid_btn.setText("▦")
            
        self.grid_btn.setStyleSheet("""
            QPushButton {
                background-color: #2F3E46;
                border: 1px solid #1D2A30;
                border-radius: 2px;
            }
        """)

        # List View Button (Inactive Grey Style)
        self.list_btn = QPushButton()
        self.list_btn.setFixedSize(28, 26)
        self.list_btn.setCursor(Qt.PointingHandCursor)
        if not list_icon.isNull():
            self.list_btn.setIcon(list_icon)
        else:
            self.list_btn.setText("≡")

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
# 2. Report Card Widget Component
# -------------------------------------------------------------
class ReportCardWidget(QFrame):
    def __init__(self, title, image_path="stock_report_preview.png"):
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

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            img_lbl.setPixmap(pixmap.scaled(120, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            img_lbl.setText("Image\nNot Found")
            img_lbl.setStyleSheet("color: white; font-size: 8pt;")

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
# 3. Home > Credentials View Widget (With Sprite Buttons)
# -------------------------------------------------------------
class HomeCredentialsWidget(QWidget):
    def __init__(self, sprite_pixmap):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        self.toolbar = ViewToggleToolbar(sprite_pixmap)
        layout.addWidget(self.toolbar)

        # Workspace Content Area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        info_lbl = QLabel("Home > Credentials Workspace Area")
        info_lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        info_lbl.setStyleSheet("color: #4A5568; font-size: 11pt;")
        content_layout.addWidget(info_lbl)
        
        layout.addWidget(content_area, stretch=1)


# -------------------------------------------------------------
# 4. Home > Reports View Widget (With Sprite Buttons)
# -------------------------------------------------------------
class HomeReportsWidget(QWidget):
    def __init__(self, sprite_pixmap, image_path="stock_report_preview.png"):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        self.toolbar = ViewToggleToolbar(sprite_pixmap)
        layout.addWidget(self.toolbar)

        # Reports Content Area
        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)
        content_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        card1 = ReportCardWidget("Credentials Issued", image_path)
        card2 = ReportCardWidget("Credentials Printed", image_path)

        content_layout.addWidget(card1)
        content_layout.addWidget(card2)

        layout.addWidget(content_area, stretch=1)


# -------------------------------------------------------------
# 5. Credential Design Editor View
# -------------------------------------------------------------
class CredentialDesignEditor(QWidget):
    def __init__(self, on_close_callback):
        super().__init__()
        self.on_close_callback = on_close_callback

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        purple_bar = QFrame()
        purple_bar.setFixedHeight(42)
        purple_bar.setStyleSheet("background-color: #7A0A8A;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        title_lbl = QLabel("Credential Design 1")
        title_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_lbl.setStyleSheet("color: white;")

        purple_layout.addWidget(title_lbl)
        purple_layout.addStretch()
        main_layout.addWidget(purple_bar)

        center_body = QLabel("Design Editor Content")
        center_body.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(center_body, stretch=1)

        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(40)
        bottom_bar.setStyleSheet("background-color: #F1F5F9; border-top: 1px solid #CBD5E0;")
        bottom_layout = QHBoxLayout(bottom_bar)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.on_close_callback)
        bottom_layout.addWidget(close_btn)
        bottom_layout.addStretch()

        main_layout.addWidget(bottom_bar)


# -------------------------------------------------------------
# 6. Main Dashboard Component
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.sprite = QPixmap("sprite_button_2.png")
        self.report_img_path = "stock_report_preview.png"

        self.root_stack = QStackedWidget(self)
        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(0, 0, 0, 0)
        main_box.addWidget(self.root_stack)

        self.dashboard_view = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_view)
        dash_layout.setContentsMargins(0, 0, 0, 0)
        dash_layout.setSpacing(0)

        # Top Navigation Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(54)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #DCDCDC;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(18, 0, 20, 0)

        logo_box = QHBoxLayout()
        logo_icon = QLabel("⬡")
        logo_icon.setStyleSheet("color: #7A0A8A; font-size: 24px; font-weight: bold;")
        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Segoe UI", 14, QFont.Bold))
        logo_text.setStyleSheet("color: #4A4A4A; letter-spacing: 1.5px;")
        logo_box.addWidget(logo_icon)
        logo_box.addWidget(logo_text)
        top_layout.addLayout(logo_box)

        sub_title = QLabel("  |  Adaptive Issuance™\n     Instant ID")
        sub_title.setFont(QFont("Segoe UI", 8, QFont.Bold))
        sub_title.setStyleSheet("color: #333333;")
        top_layout.addWidget(sub_title)
        top_layout.addSpacing(40)

        nav_box = QHBoxLayout()
        nav_box.setSpacing(25)

        self.home_btn = QPushButton("Home")
        self.home_btn.setCursor(Qt.PointingHandCursor)
        self.home_btn.clicked.connect(self.select_home_nav)

        self.design_btn = QPushButton("Design ▾")
        self.design_btn.setCursor(Qt.PointingHandCursor)
        self.design_btn.clicked.connect(self.select_design_nav)

        self.printer_btn = QPushButton("Printer Queues")
        self.printer_btn.setCursor(Qt.PointingHandCursor)
        self.printer_btn.clicked.connect(self.select_printer_nav)

        nav_box.addWidget(self.home_btn)
        nav_box.addWidget(self.design_btn)
        nav_box.addWidget(self.printer_btn)
        top_layout.addLayout(nav_box)
        top_layout.addStretch()

        dash_layout.addWidget(top_bar)

        # Purple Sub-Tabs Bar
        purple_bar = QFrame()
        purple_bar.setFixedHeight(36)
        purple_bar.setStyleSheet("background-color: #7A0A8A;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        self.sub_tabs_container = QWidget()
        self.sub_tabs_layout = QHBoxLayout(self.sub_tabs_container)
        self.sub_tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_tabs_layout.setSpacing(0)

        purple_layout.addWidget(self.sub_tabs_container)
        purple_layout.addStretch()

        login_info = QLabel("Last Login at Wed Sep 09 10:18:38 MMT 2026 from IP 192.168.56.1  admin ▾")
        login_info.setStyleSheet("color: #DDA0DD; font-size: 8pt;")
        purple_layout.addWidget(login_info)

        dash_layout.addWidget(purple_bar)

        # Create Button Toolbar (Design Tab Only)
        self.tool_bar = QFrame()
        self.tool_bar.setFixedHeight(34)
        self.tool_bar.setStyleSheet("background-color: #F3F4F6; border-bottom: 1px solid #E5E7EB;")
        tool_layout = QHBoxLayout(self.tool_bar)
        tool_layout.setContentsMargins(8, 0, 8, 0)

        self.create_btn = QPushButton("+ Create")
        self.create_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.create_btn.setFixedHeight(25)
        self.create_btn.setCursor(Qt.PointingHandCursor)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #222222;
                border: 1px solid #CBD5E0;
                border-radius: 2px;
                padding: 0px 12px;
            }
            QPushButton:hover { background-color: #F1F5F9; }
        """)
        self.create_btn.clicked.connect(self.open_editor_view)

        tool_layout.addWidget(self.create_btn)
        tool_layout.addStretch()
        dash_layout.addWidget(self.tool_bar)

        # Main Workspace Views Stack
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #FFFFFF;")

        # Home Sub-tab Workspaces
        self.home_cred_page = HomeCredentialsWidget(self.sprite)
        self.home_reports_page = HomeReportsWidget(self.sprite, self.report_img_path)

        # Design Sub-tab Workspaces
        self.design_cred_page = QLabel("Design > Credential Designs Workspace")
        self.design_cred_page.setAlignment(Qt.AlignCenter)
        self.design_workflows_page = QLabel("Design > Workflows Workspace")
        self.design_workflows_page.setAlignment(Qt.AlignCenter)
        self.design_reports_page = QLabel("Design > Reports Workspace")
        self.design_reports_page.setAlignment(Qt.AlignCenter)
        self.design_field_conn_page = QLabel("Design > Field Connections Workspace")
        self.design_field_conn_page.setAlignment(Qt.AlignCenter)

        # Printer Queues Workspace
        self.printer_queues_page = QLabel("Printer Queues Workspace Content")
        self.printer_queues_page.setAlignment(Qt.AlignCenter)

        self.content_stack.addWidget(self.home_cred_page)        # Index 0
        self.content_stack.addWidget(self.home_reports_page)     # Index 1
        self.content_stack.addWidget(self.design_cred_page)      # Index 2
        self.content_stack.addWidget(self.design_workflows_page) # Index 3
        self.content_stack.addWidget(self.design_reports_page)   # Index 4
        self.content_stack.addWidget(self.design_field_conn_page)# Index 5
        self.content_stack.addWidget(self.printer_queues_page)   # Index 6

        dash_layout.addWidget(self.content_stack, stretch=1)

        # Footer Status Bar
        self.status_bar = QFrame()
        self.status_bar.setFixedHeight(32)
        self.status_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        status_layout = QHBoxLayout(self.status_bar)
        status_layout.setContentsMargins(10, 0, 15, 0)
        status_layout.addStretch()

        self.queue_status_btn = QPushButton(" Printer Queue Status")
        self.queue_status_btn.setFont(QFont("Segoe UI", 8.5, QFont.Bold))
        self.queue_status_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #E2E8F0);
                color: #1E3A8A;
                border: 1px solid #CBD5E0;
                border-radius: 3px;
                padding: 4px 12px;
            }
            QPushButton:hover { background-color: #EDF2F7; }
        """)
        status_layout.addWidget(self.queue_status_btn)
        dash_layout.addWidget(self.status_bar)

        self.editor_view = CredentialDesignEditor(on_close_callback=self.close_editor_view)

        self.root_stack.addWidget(self.dashboard_view) # Index 0
        self.root_stack.addWidget(self.editor_view)    # Index 1

        self.sub_tab_buttons = []
        self.select_home_nav()

    # Dynamic Navigation Logic
    def update_top_nav_styles(self, active_nav):
        active_style = "border: none; color: #7A0A8A; font-weight: bold; font-size: 10pt; background: transparent;"
        inactive_style = "border: none; color: #222222; font-weight: bold; font-size: 10pt; background: transparent;"

        self.home_btn.setStyleSheet(active_style if active_nav == "Home" else inactive_style)
        self.design_btn.setStyleSheet(active_style if active_nav == "Design" else inactive_style)
        self.printer_btn.setStyleSheet(active_style if active_nav == "Printer" else inactive_style)

    def clear_sub_tabs(self):
        for btn in self.sub_tab_buttons:
            self.sub_tabs_layout.removeWidget(btn)
            btn.deleteLater()
        self.sub_tab_buttons = []

    def select_home_nav(self):
        self.update_top_nav_styles("Home")
        self.clear_sub_tabs()
        self.tool_bar.setVisible(False)
        self.queue_status_btn.setVisible(True)

        tabs_info = [("Credentials", 0), ("Reports", 1)]
        for text, page_idx in tabs_info:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
            btn.setFixedHeight(36)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=page_idx, b=btn: self.activate_sub_tab(idx, b))
            self.sub_tabs_layout.addWidget(btn)
            self.sub_tab_buttons.append(btn)

        self.activate_sub_tab(0, self.sub_tab_buttons[0])

    def select_design_nav(self):
        self.update_top_nav_styles("Design")
        self.clear_sub_tabs()
        self.tool_bar.setVisible(True)
        self.queue_status_btn.setVisible(False)

        tabs_info = [
            ("Credential Designs", 2),
            ("Workflows", 3),
            ("Reports", 4),
            ("Field Connections", 5)
        ]
        for text, page_idx in tabs_info:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
            btn.setFixedHeight(36)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=page_idx, b=btn: self.activate_sub_tab(idx, b))
            self.sub_tabs_layout.addWidget(btn)
            self.sub_tab_buttons.append(btn)

        self.activate_sub_tab(2, self.sub_tab_buttons[0])

    def select_printer_nav(self):
        self.update_top_nav_styles("Printer")
        self.clear_sub_tabs()
        self.tool_bar.setVisible(False)
        self.queue_status_btn.setVisible(True)
        self.content_stack.setCurrentIndex(6)

    def activate_sub_tab(self, target_index, active_btn):
        self.content_stack.setCurrentIndex(target_index)

        active_style = """
            QPushButton {
                background-color: #FFFFFF;
                color: #7A0A8A;
                border: none;
                padding: 0px 18px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }
        """
        inactive_style = """
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding: 0px 18px;
            }
            QPushButton:hover { color: #E0B0FF; }
        """

        for btn in self.sub_tab_buttons:
            if btn == active_btn:
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet(inactive_style)

    def open_editor_view(self):
        self.root_stack.setCurrentIndex(1)

    def close_editor_view(self):
        self.root_stack.setCurrentIndex(0)


# -------------------------------------------------------------
# 7. Main Window
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1280, 720)

        self.dashboard = EntrustDashboard()
        self.setCentralWidget(self.dashboard)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
