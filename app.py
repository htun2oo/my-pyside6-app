import sys
import os
import math
from PIL import Image
from PySide6.QtCore import Qt, QSize, QPointF
from PySide6.QtGui import QIcon, QPixmap, QFont, QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit,
    QDialog, QFrame, QMessageBox
)

# -------------------------------------------------------------
# Helper Function for Local File Icons
# -------------------------------------------------------------
def get_pixmap(icon_name, size=(24, 24)):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [
        os.path.join(current_script_dir, "assets", "icons", icon_name),
        os.path.join(current_script_dir, "src", "assets", "icons", icon_name),
        os.path.join(os.getcwd(), "src", "assets", "icons", icon_name),
        os.path.join(os.getcwd(), "assets", "icons", icon_name)
    ]
    
    for path in paths:
        if os.path.exists(path):
            pix = QPixmap(path)
            if not pix.isNull():
                return pix.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return None


# -------------------------------------------------------------
# Instant PVC Vector Logo
# -------------------------------------------------------------
class InstantPVCLogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(70, 70)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        center_x, center_y, radius = 35, 35, 30
        points = []
        for i in range(6):
            angle_rad = math.radians(60 * i - 30)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append(QPointF(x, y))

        pen = QPen(QColor("#FFFFFF"), 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(QPolygonF(points))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawRoundedRect(22, 22, 26, 18, 3, 3)
        
        painter.setBrush(QColor("#4C1D95"))
        painter.drawRect(25, 26, 7, 7)
        painter.drawRect(34, 26, 11, 2)
        painter.drawRect(34, 30, 11, 2)
        painter.drawRect(25, 35, 20, 2)


# -------------------------------------------------------------
# Login Window (Redesigned for Instant PVC)
# -------------------------------------------------------------
class LoginWidget(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        
        self.setStyleSheet("""
            QWidget#LoginMain {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4C1D95, stop:1 #2E1065);
            }
        """)
        self.setObjectName("LoginMain")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        center_box = QWidget()
        center_box.setFixedWidth(420)
        box_layout = QVBoxLayout(center_box)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(15)

        logo_container = QHBoxLayout()
        logo_container.addWidget(InstantPVCLogo(), 0, Qt.AlignCenter)
        box_layout.addLayout(logo_container)

        title_lbl = QLabel("INSTANT PVC")
        title_lbl.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; letter-spacing: 2px;")
        title_lbl.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(title_lbl)

        subtitle_lbl = QLabel("Card Issuance Suite")
        subtitle_lbl.setFont(QFont("Segoe UI", 11))
        subtitle_lbl.setStyleSheet("color: #DDD6FE; margin-bottom: 5px;")
        subtitle_lbl.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(subtitle_lbl)

        form_card = QFrame()
        form_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 8px;
            }
            QLabel {
                color: #4B5563;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 13px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #7C3AED;
                background-color: #FFFFFF;
            }
        """)
        
        card_layout = QVBoxLayout(form_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(10)

        card_layout.addWidget(QLabel("User ID"))
        self.user_entry = QLineEdit()
        self.user_entry.setFixedHeight(38)
        card_layout.addWidget(self.user_entry)

        card_layout.addWidget(QLabel("Password"))
        self.pass_entry = QLineEdit()
        self.pass_entry.setEchoMode(QLineEdit.Password)
        self.pass_entry.setFixedHeight(38)
        card_layout.addWidget(self.pass_entry)

        box_layout.addWidget(form_card)

        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #E9D5FF;
                font-size: 12px;
                font-weight: 500;
                border: none;
            }
            QPushButton:hover {
                color: #FFFFFF;
                text-decoration: underline;
            }
        """)
        box_layout.addWidget(forgot_btn, 0, Qt.AlignCenter)

        login_btn = QPushButton("Sign In")
        login_btn.setFixedWidth(120)
        login_btn.setFixedHeight(38)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
        """)
        login_btn.clicked.connect(self.check_login)
        box_layout.addWidget(login_btn, 0, Qt.AlignCenter)

        main_layout.addWidget(center_box)

    def check_login(self):
        if self.user_entry.text().strip() == "admin" and self.pass_entry.text().strip() == "admin123":
            self.on_login_success("admin")
        else:
            QMessageBox.critical(self, "Login Failed", "User ID သို့မဟုတ် Password မှားယွင်းနေပါသည်။\n(Default: admin / admin123)")


# -------------------------------------------------------------
# Edit Properties Pop-up Dialog
# -------------------------------------------------------------
class EditPropertiesDialog(QDialog):
    def __init__(self, parent, current_title, on_save):
        super().__init__(parent)
        self.setWindowTitle("Edit Properties")
        self.setFixedSize(450, 580)
        self.setModal(True)
        self.on_save = on_save

        self.setStyleSheet("""
            QDialog { background-color: #F3F4F6; }
            QLabel { font-size: 12px; color: #374151; }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 3px;
                padding: 4px;
                color: #1F2937;
            }
            QCheckBox { font-size: 12px; color: #374151; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setFixedHeight(40)
        header.setStyleSheet("background-color: #6B21A8;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 10, 0)
        
        header_title = QLabel("Edit Properties")
        header_title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        header_layout.addWidget(header_title)
        
        close_btn = QPushButton("✖")
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet("QPushButton { color: white; border: none; background: transparent; } QPushButton:hover { background-color: #581C87; }")
        close_btn.clicked.connect(self.reject)
        header_layout.addWidget(close_btn, 0, Qt.AlignRight)

        main_layout.addWidget(header)

        form_frame = QWidget()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(20, 15, 20, 15)

        form_layout.addWidget(QLabel("Name"))
        self.name_entry = QLineEdit(current_title)
        self.name_entry.setFixedWidth(220)
        form_layout.addWidget(self.name_entry)

        form_layout.addWidget(QLabel("Dimensions"))
        self.dim_combo = QComboBox()
        self.dim_combo.addItems(["CR-50", "ISO ID-1", "Custom"])
        self.dim_combo.setFixedWidth(130)
        self.dim_combo.currentTextChanged.connect(self.on_dimension_change)
        form_layout.addWidget(self.dim_combo)

        form_layout.addWidget(QLabel("Units"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Centimeters", "Millimeters"])
        self.unit_combo.setFixedWidth(130)
        self.unit_combo.currentTextChanged.connect(self.on_unit_change)
        form_layout.addWidget(self.unit_combo)

        form_layout.addWidget(QLabel("Width"))
        w_layout = QHBoxLayout()
        self.width_entry = QLineEdit("8.8900")
        self.width_entry.setFixedWidth(130)
        self.width_unit_lbl = QLabel("centimeters")
        w_layout.addWidget(self.width_entry)
        w_layout.addWidget(self.width_unit_lbl)
        w_layout.addStretch()
        form_layout.addLayout(w_layout)

        form_layout.addWidget(QLabel("Height"))
        h_layout = QHBoxLayout()
        self.height_entry = QLineEdit("4.3815")
        self.height_entry.setFixedWidth(130)
        self.height_unit_lbl = QLabel("centimeters")
        h_layout.addWidget(self.height_entry)
        h_layout.addWidget(self.height_unit_lbl)
        h_layout.addStretch()
        form_layout.addLayout(h_layout)

        self.rewritable_chk = QCheckBox("Rewritable credential  ❓")
        self.print_edge_chk = QCheckBox("Print over the edge  ❓")
        form_layout.addWidget(self.rewritable_chk)
        form_layout.addWidget(self.print_edge_chk)

        form_layout.addWidget(QLabel("Description"))
        self.desc_textbox = QTextEdit()
        self.desc_textbox.setFixedHeight(80)
        form_layout.addWidget(self.desc_textbox)

        main_layout.addWidget(form_frame)

        btn_bar = QFrame()
        btn_bar.setFixedHeight(45)
        btn_bar.setStyleSheet("background-color: #E5E7EB;")
        btn_layout = QHBoxLayout(btn_bar)
        btn_layout.setContentsMargins(15, 0, 15, 0)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedSize(80, 30)
        ok_btn.setStyleSheet("QPushButton { background-color: #3B82F6; color: white; font-weight: bold; border: none; border-radius: 2px; } QPushButton:hover { background-color: #2563EB; }")
        ok_btn.clicked.connect(self.save_and_close)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(80, 30)
        cancel_btn.setStyleSheet("QPushButton { background-color: #D1D5DB; color: #374151; border: none; border-radius: 2px; } QPushButton:hover { background-color: #9CA3AF; }")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        main_layout.addWidget(btn_bar)

    def on_dimension_change(self, choice):
        if choice == "ISO ID-1":
            if self.unit_combo.currentText() == "Centimeters":
                self.width_entry.setText("8.5725")
                self.height_entry.setText("5.3975")
            else:
                self.width_entry.setText("85.60")
                self.height_entry.setText("53.98")
        elif choice == "CR-50":
            if self.unit_combo.currentText() == "Centimeters":
                self.width_entry.setText("8.8900")
                self.height_entry.setText("4.3815")
            else:
                self.width_entry.setText("88.90")
                self.height_entry.setText("43.82")

    def on_unit_change(self, choice):
        unit_text = choice.lower()
        self.width_unit_lbl.setText(unit_text)
        self.height_unit_lbl.setText(unit_text)
        self.on_dimension_change(self.dim_combo.currentText())

    def save_and_close(self):
        new_name = self.name_entry.text().strip()
        if new_name:
            self.on_save(new_name)
        self.accept()


# -------------------------------------------------------------
# Designer Interface (Updated Icons & Toolbar)
# -------------------------------------------------------------
class CredentialDesignerWidget(QWidget):
    def __init__(self, on_close):
        super().__init__()
        self.on_close = on_close
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Ribbon Header
        ribbon = QFrame()
        ribbon.setFixedHeight(70)
        ribbon.setStyleSheet("background-color: #6B21A8;")
        ribbon_layout = QHBoxLayout(ribbon)
        ribbon_layout.setContentsMargins(15, 0, 15, 0)

        self.design_title_lbl = QLabel("Credential Design 1")
        self.design_title_lbl.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        ribbon_layout.addWidget(self.design_title_lbl)

        self.edit_btn = QPushButton()
        self.edit_btn.setFixedSize(60, 60)
        self.edit_btn.setToolTip("Edit Properties")
        
        pix = get_pixmap("icon_edit_on.png", size=(52, 52))
        if pix:
            self.edit_btn.setIcon(QIcon(pix))
            self.edit_btn.setIconSize(QSize(52, 52))
        else:
            self.edit_btn.setText("✏️")

        self.edit_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #7E22CE;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #581C87;
            }
        """)
        self.edit_btn.clicked.connect(self.open_edit_dialog)
        ribbon_layout.addWidget(self.edit_btn)
        ribbon_layout.addStretch()

        main_layout.addWidget(ribbon)

        # Prominent Toolbar Section
        toolbar_frame = QFrame()
        toolbar_frame.setFixedHeight(48)
        toolbar_frame.setStyleSheet("""
            QFrame {
                background-color: #F3F4F6; 
                border-bottom: 1px solid #CBD5E1;
            }
            QPushButton {
                background-color: #FFFFFF; 
                border: 1px solid #CBD5E1; 
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
                color: #1F2937;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
                border-color: #9CA3AF;
            }
            QPushButton:pressed {
                background-color: #CBD5E1;
            }
        """)
        tb_layout = QHBoxLayout(toolbar_frame)
        tb_layout.setContentsMargins(8, 4, 8, 4)
        tb_layout.setSpacing(6)

        tools = [
            ("↶", "Undo"), ("↷", "Redo"), ("📋", "Copy"), ("✂️", "Cut"), ("📑", "Paste"),
            ("|", None),
            ("T⁭", "Text"), ("T", "Static Text"), ("👤", "Photo"), ("🖼️", "Graphic"),
            ("|", None),
            ("║█║", "Bar Code"), ("💳", "Mag Stripe"), ("🎛️", "Chip")
        ]

        for icon, tooltip in tools:
            if icon == "|":
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setStyleSheet("color: #CBD5E1; max-height: 24px;")
                tb_layout.addWidget(line)
            else:
                btn = QPushButton(icon)
                btn.setFixedSize(36, 36)
                if tooltip:
                    btn.setToolTip(tooltip)
                tb_layout.addWidget(btn)

        tb_layout.addStretch()
        main_layout.addWidget(toolbar_frame)

        # Workspace Area
        workspace = QFrame()
        workspace.setStyleSheet("background-color: #D1D5DB;")
        ws_layout = QHBoxLayout(workspace)
        ws_layout.setContentsMargins(10, 10, 10, 10)

        canvas_box = QFrame()
        canvas_box.setStyleSheet("background-color: #E5E7EB; border-radius: 4px;")
        c_layout = QHBoxLayout(canvas_box)

        front_card = QFrame()
        front_card.setFixedSize(300, 180)
        front_card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #374151;")

        back_card = QFrame()
        back_card.setFixedSize(300, 180)
        back_card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #374151;")

        c_layout.addWidget(front_card, 0, Qt.AlignCenter)
        c_layout.addWidget(back_card, 0, Qt.AlignCenter)

        right_panel = QFrame()
        right_panel.setFixedWidth(220)
        right_panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #CBD5E1;")

        ws_layout.addWidget(canvas_box)
        ws_layout.addWidget(right_panel)

        main_layout.addWidget(workspace)

        # Bottom Bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(40)
        bottom_bar.setStyleSheet("background-color: #F3F4F6; border-top: 1px solid #CBD5E1;")
        bb_layout = QHBoxLayout(bottom_bar)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(75, 26)
        close_btn.clicked.connect(self.on_close)
        bb_layout.addWidget(close_btn)
        bb_layout.addStretch()

        main_layout.addWidget(bottom_bar)

    def open_edit_dialog(self):
        dialog = EditPropertiesDialog(self, self.design_title_lbl.text(), self.update_title)
        dialog.exec()

    def update_title(self, new_title):
        self.design_title_lbl.setText(new_title)


# -------------------------------------------------------------
# Main Window Frame
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instant PVC")
        self.resize(1200, 720)

        self.login_widget = LoginWidget(self.show_dashboard)
        self.setCentralWidget(self.login_widget)

    def show_dashboard(self, username):
        self.designer = CredentialDesignerWidget(on_close=self.logout)
        self.setCentralWidget(self.designer)

    def logout(self):
        self.login_widget = LoginWidget(self.show_dashboard)
        self.setCentralWidget(self.login_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
