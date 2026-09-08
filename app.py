import sys
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, QToolButton,
    QComboBox, QCheckBox, QScrollArea
)

def get_sprite_icon(sprite_pixmap, x, y, width=24, height=24):
    if sprite_pixmap.isNull():
        return QPixmap()
    return sprite_pixmap.copy(QRect(x, y, width, height))


# -------------------------------------------------------------
# 1. Credential Design Editor View (ဒုတိယပုံ UI)
# -------------------------------------------------------------
class CredentialDesignEditor(QWidget):
    def __init__(self, on_close_callback, sprite_pixmap):
        super().__init__()
        self.on_close_callback = on_close_callback
        self.sprite = sprite_pixmap

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Purple Ribbon Title Bar
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

        # 2. Design Tools Ribbon Bar
        tools_bar = QFrame()
        tools_bar.setFixedHeight(40)
        tools_bar.setStyleSheet("background-color: #E2E8F0; border-bottom: 1px solid #CBD5E0;")
        tools_layout = QHBoxLayout(tools_bar)
        tools_layout.setContentsMargins(10, 0, 10, 0)
        tools_layout.setSpacing(4)

        # Tool Buttons Mockup
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

        # 3. Canvas & Properties Sidebar Area
        center_body = QWidget()
        center_layout = QHBoxLayout(center_body)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        # Canvas Workspace Area (Front Side & Back Side)
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

        # Active Layer Info Bar
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

        # Right Side Properties Panel
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #F8FAFC; border-left: 1px solid #CBD5E0;")

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)

        # Properties / Layers Tab Header
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

        # Panel Content
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

        # 4. Bottom Action Footer Bar
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
# 2. Main Entrust Dashboard UI (ပထမပုံ UI)
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.sprite = QPixmap("sprite_button.png")

        self.root_stack = QStackedWidget(self)
        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(0, 0, 0, 0)
        main_box.addWidget(self.root_stack)

        # Base Dashboard View Container
        self.dashboard_view = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_view)
        dash_layout.setContentsMargins(0, 0, 0, 0)
        dash_layout.setSpacing(0)

        # ---------------- Top Bar ----------------
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
        self.home_btn.setStyleSheet("border: none; color: #222222; font-weight: bold;")
        self.design_btn = QPushButton("Design ▾")
        self.design_btn.setStyleSheet("border: none; color: #7A0A8A; font-weight: bold;")
        self.printer_btn = QPushButton("Printer Queues")
        self.printer_btn.setStyleSheet("border: none; color: #222222; font-weight: bold;")

        nav_box.addWidget(self.home_btn)
        nav_box.addWidget(self.design_btn)
        nav_box.addWidget(self.printer_btn)
        top_layout.addLayout(nav_box)
        top_layout.addStretch()

        dash_layout.addWidget(top_bar)

        # ---------------- Purple Ribbon Bar ----------------
        purple_bar = QFrame()
        purple_bar.setFixedHeight(36)
        purple_bar.setStyleSheet("background-color: #7A0A8A;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        tab1 = QPushButton("Credential Designs")
        tab1.setStyleSheet("background-color: white; color: #7A0A8A; border: none; font-weight: bold; padding: 8px 16px;")
        tab2 = QPushButton("Workflows")
        tab2.setStyleSheet("background-color: transparent; color: white; border: none; font-weight: bold; padding: 8px 16px;")
        tab3 = QPushButton("Reports")
        tab3.setStyleSheet("background-color: transparent; color: white; border: none; font-weight: bold; padding: 8px 16px;")
        tab4 = QPushButton("Field Connections")
        tab4.setStyleSheet("background-color: transparent; color: white; border: none; font-weight: bold; padding: 8px 16px;")

        purple_layout.addWidget(tab1)
        purple_layout.addWidget(tab2)
        purple_layout.addWidget(tab3)
        purple_layout.addWidget(tab4)
        purple_layout.addStretch()

        login_info = QLabel("Last Login at Tue Sep 08 01:41:31 MMT 2026 from IP 192.168.99.109  admin ▾")
        login_info.setStyleSheet("color: #DDA0DD; font-size: 8pt;")
        purple_layout.addWidget(login_info)

        dash_layout.addWidget(purple_bar)

        # ---------------- Light Grey Toolbar ----------------
        tool_bar = QFrame()
        tool_bar.setFixedHeight(34)
        tool_bar.setStyleSheet("background-color: #F3F4F6; border-bottom: 1px solid #E5E7EB;")
        tool_layout = QHBoxLayout(tool_bar)
        tool_layout.setContentsMargins(8, 0, 8, 0)

        # + Create Button
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
        # Click လုပ်ပါက Editor View သို့ ပြောင်းလဲရန် ချိတ်ဆက်ခြင်း
        self.create_btn.clicked.connect(self.open_editor_view)

        tool_layout.addWidget(self.create_btn)
        tool_layout.addStretch()
        dash_layout.addWidget(tool_bar)

        # Empty Canvas Workspace Area
        workspace = QWidget()
        workspace.setStyleSheet("background-color: #FFFFFF;")
        dash_layout.addWidget(workspace, stretch=1)

        # Editor View instance
        self.editor_view = CredentialDesignEditor(on_close_callback=self.close_editor_view, sprite_pixmap=self.sprite)

        # Root Stacked Widget ထဲသို့ ထည့်သွင်းခြင်း
        self.root_stack.addWidget(self.dashboard_view) # Index 0 (ပထမပုံ)
        self.root_stack.addWidget(self.editor_view)    # Index 1 (ဒုတိယပုံ)

    def open_editor_view(self):
        """ + Create button ကို နှိပ်ပါက Editor View သို့ ပြောင်းမည် """
        self.root_stack.setCurrentIndex(1)

    def close_editor_view(self):
        """ Editor View မှ Close button ကို နှိပ်ပါက မူလ ပထမ UI သို့ ပြန်သွားမည် """
        self.root_stack.setCurrentIndex(0)


# -------------------------------------------------------------
# 3. Main Application Window
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
