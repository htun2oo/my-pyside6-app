import sys
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, QToolButton,
    QComboBox, QCheckBox, QScrollArea, QMessageBox
)

def get_sprite_icon(sprite_pixmap, x, y, width=24, height=24):
    if sprite_pixmap.isNull():
        return QPixmap()
    return sprite_pixmap.copy(QRect(x, y, width, height))


# -------------------------------------------------------------
# 1. Credential Design Editor View
# -------------------------------------------------------------
class CredentialDesignEditor(QWidget):
    def __init__(self, on_close_callback, sprite_pixmap):
        super().__init__()
        self.on_close_callback = on_close_callback
        self.sprite = sprite_pixmap

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Purple Ribbon Title Bar
        purple_bar = QFrame()
        purple_bar.setFixedHeight(42)
        purple_bar.setStyleSheet("background-color: #7A0A8A;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        title_lbl = QLabel("Credential Design 1")
        title_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_lbl.setStyleSheet("color: white;")

        edit_icon = QLabel(" ✏️")
        edit_icon.setStyleSheet("color: white; font-size: 14px;")

        purple_layout.addWidget(title_lbl)
        purple_layout.addWidget(edit_icon)
        purple_layout.addStretch()
        main_layout.addWidget(purple_bar)

        # Design Tools Ribbon Bar
        tools_bar = QFrame()
        tools_bar.setFixedHeight(40)
        tools_bar.setStyleSheet("background-color: #E2E8F0; border-bottom: 1px solid #CBD5E0;")
        tools_layout = QHBoxLayout(tools_bar)
        tools_layout.setContentsMargins(10, 0, 10, 0)
        tools_layout.setSpacing(4)

        tool_icons = ["↩", "↪", "|", "📋", "✂", "📄", "|", "T", "T₂", "👤", "🖼", "📈", "🏁", "║║", "💳", "▦", "▤", "/", "▢", "◯", "📐", "▦", "|", "🔍-", "🔍+", "100%", "⊞"]
        for item in tool_icons:
            if item == "|":
                sep = QFrame()
                sep.setFrameShape(QFrame.VLine)
                sep.setStyleSheet("color: #A0AEC0; max-height: 20px;")
                tools_layout.addWidget(sep)
            elif item == "100%":
                combo = QComboBox()
                combo.addItems(["100%", "75%", "50%", "150%"])
                combo.setStyleSheet("background: white; border: 1px solid #CBD5E0; border-radius: 2px; padding: 2px;")
                tools_layout.addWidget(combo)
            else:
                btn = QToolButton()
                btn.setText(item)
                btn.setFixedSize(26, 26)
                btn.setStyleSheet("QToolButton { background: white; border: 1px solid #CBD5E0; border-radius: 2px; font-weight: bold; } QToolButton:hover { background: #EDF2F7; }")
                tools_layout.addWidget(btn)

        tools_layout.addStretch()
        main_layout.addWidget(tools_bar)

        # Canvas & Properties Sidebar Area
        center_body = QWidget()
        center_layout = QHBoxLayout(center_body)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setStyleSheet("background-color: #FFFFFF; border: none;")

        canvas_content = QWidget()
        canvas_layout = QHBoxLayout(canvas_content)
        canvas_layout.setContentsMargins(20, 20, 20, 20)
        canvas_layout.setSpacing(25)
        canvas_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Front Side Container
        front_box = QVBoxLayout()
        front_lbl = QLabel("Front Side")
        front_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        front_lbl.setStyleSheet("color: #2D3748;")
        
        front_card_bg = QFrame()
        front_card_bg.setFixedSize(320, 420)
        front_card_bg.setStyleSheet("background-color: #A0AEC0; border-radius: 4px;")
        f_card_layout = QVBoxLayout(front_card_bg)
        f_card_layout.setAlignment(Qt.AlignCenter)

        front_card = QFrame()
        front_card.setFixedSize(260, 160)
        front_card.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 12px;")
        f_card_layout.addWidget(front_card)

        front_box.addWidget(front_lbl)
        front_box.addWidget(front_card_bg)

        active_layer_lbl = QLabel("Active Design Layer: Color")
        active_layer_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        active_layer_lbl.setStyleSheet("color: #2D3748;")

        # Back Side Container
        back_box = QVBoxLayout()
        back_lbl = QLabel("Back Side")
        back_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        back_lbl.setStyleSheet("color: #2D3748;")

        back_card_bg = QFrame()
        back_card_bg.setFixedSize(320, 420)
        back_card_bg.setStyleSheet("background-color: #A0AEC0; border-radius: 4px;")
        b_card_layout = QVBoxLayout(back_card_bg)
        b_card_layout.setAlignment(Qt.AlignCenter)

        back_card = QFrame()
        back_card.setFixedSize(260, 160)
        back_card.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 12px;")
        b_card_layout.addWidget(back_card)

        back_box.addWidget(back_lbl)
        back_box.addWidget(back_card_bg)

        canvas_layout.addLayout(front_box)
        canvas_layout.addWidget(active_layer_lbl, alignment=Qt.AlignTop)
        canvas_layout.addLayout(back_box)

        canvas_scroll.setWidget(canvas_content)
        center_layout.addWidget(canvas_scroll, stretch=1)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #F8FAFC; border-left: 1px solid #CBD5E0;")

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)

        tab_header = QFrame()
        tab_header.setFixedHeight(32)
        tab_header.setStyleSheet("background-color: #EDF2F7; border-bottom: 1px solid #CBD5E0;")
        tab_header_layout = QHBoxLayout(tab_header)
        tab_header_layout.setContentsMargins(0, 0, 0, 0)

        prop_tab = QPushButton("Properties")
        prop_tab.setStyleSheet("background: white; border: none; font-weight: bold; color: #2B6CB0;")
        layers_tab = QPushButton("Layers")
        layers_tab.setStyleSheet("background: transparent; border: none; color: #4A5568;")

        tab_header_layout.addWidget(prop_tab)
        tab_header_layout.addWidget(layers_tab)
        side_layout.addWidget(tab_header)

        prop_content = QWidget()
        prop_layout = QVBoxLayout(prop_content)
        prop_layout.setContentsMargins(10, 10, 10, 10)
        prop_layout.setSpacing(10)

        group_title = QLabel("- Front Side Properties")
        group_title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        group_title.setStyleSheet("color: #2D3748;")
        prop_layout.addWidget(group_title)

        chk1 = QCheckBox("Rotate print orientation 180\ndegrees")
        chk1.setStyleSheet("color: #4A5568; font-size: 8.5pt;")
        chk2 = QCheckBox("Tactile Impression Module")
        chk2.setStyleSheet("color: #4A5568; font-size: 8.5pt;")

        prop_layout.addWidget(chk1)
        prop_layout.addWidget(chk2)
        prop_layout.addStretch()

        side_layout.addWidget(prop_content)
        center_layout.addWidget(sidebar)

        main_layout.addWidget(center_body, stretch=1)

        # Bottom Action Footer Bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(40)
        bottom_bar.setStyleSheet("background-color: #F1F5F9; border-top: 1px solid #CBD5E0;")
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(10, 0, 10, 0)
        bottom_layout.setSpacing(8)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("background-color: #3182CE; color: white; font-weight: bold; padding: 5px 18px; border-radius: 2px;")
        
        save_as_btn = QPushButton("Save As...")
        save_as_btn.setStyleSheet("background-color: #E2E8F0; color: #2D3748; padding: 5px 14px; border-radius: 2px;")

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #E2E8F0; color: #2D3748; padding: 5px 14px; border-radius: 2px;")
        close_btn.clicked.connect(self.on_close_callback)

        print_btn = QPushButton("Print Sample")
        print_btn.setStyleSheet("background-color: #E2E8F0; color: #2D3748; padding: 5px 14px; border-radius: 2px;")

        quick_btn = QPushButton("Quick Start")
        quick_btn.setEnabled(False)
        quick_btn.setStyleSheet("background-color: #EDF2F7; color: #A0AEC0; padding: 5px 14px; border-radius: 2px;")

        bottom_layout.addWidget(save_btn)
        bottom_layout.addWidget(save_as_btn)
        bottom_layout.addWidget(close_btn)
        bottom_layout.addWidget(print_btn)
        bottom_layout.addWidget(quick_btn)
        bottom_layout.addStretch()

        main_layout.addWidget(bottom_bar)


# -------------------------------------------------------------
# 2. Main Dashboard with Interactive Navigation
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.sprite = QPixmap("sprite_button.png")

        self.root_stack = QStackedWidget(self)
        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(0, 0, 0, 0)
        main_box.addWidget(self.root_stack)

        self.dashboard_view = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_view)
        dash_layout.setContentsMargins(0, 0, 0, 0)
        dash_layout.setSpacing(0)

        # ---------------- BAR 1: Top Navigation Bar ----------------
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

        # Top Main Navigation Tabs (Home, Design, Printer Queues)
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

        # ---------------- BAR 2: Purple Ribbon Sub-Tabs Bar ----------------
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

        login_info = QLabel("Last Login at Tue Sep 08 01:41:31 MMT 2026 from IP 192.168.99.109  admin ▾")
        login_info.setStyleSheet("color: #DDA0DD; font-size: 8pt;")
        purple_layout.addWidget(login_info)

        dash_layout.addWidget(purple_bar)

        # ---------------- BAR 3: Light Grey Toolbar ----------------
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

        # ---------------- MAIN CONTENT STACKED WORKSPACE ----------------
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #FFFFFF;")

        # Workspaces for Home
        self.home_cred_page = QLabel("Home > Credentials Workspace Content")
        self.home_cred_page.setAlignment(Qt.AlignCenter)
        self.home_reports_page = QLabel("Home > Reports Workspace Content")
        self.home_reports_page.setAlignment(Qt.AlignCenter)

        # Workspaces for Design
        self.design_cred_page = QLabel("Design > Credential Designs Workspace")
        self.design_cred_page.setAlignment(Qt.AlignCenter)
        self.design_workflows_page = QLabel("Design > Workflows Workspace")
        self.design_workflows_page.setAlignment(Qt.AlignCenter)
        self.design_reports_page = QLabel("Design > Reports Workspace")
        self.design_reports_page.setAlignment(Qt.AlignCenter)
        self.design_field_conn_page = QLabel("Design > Field Connections Workspace")
        self.design_field_conn_page.setAlignment(Qt.AlignCenter)

        # Workspace for Printer Queues
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

        # Status Bar
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

        self.editor_view = CredentialDesignEditor(on_close_callback=self.close_editor_view, sprite_pixmap=self.sprite)

        self.root_stack.addWidget(self.dashboard_view) # Index 0
        self.root_stack.addWidget(self.editor_view)    # Index 1

        self.sub_tab_buttons = []
        self.select_design_nav()

    # ---------------- Navigation & Switch Methods ----------------
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
# 3. Main Window
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
