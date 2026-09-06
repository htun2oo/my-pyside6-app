import sys
import os
from PIL import Image
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit,
    QDialog, QFrame, QMessageBox
)

# -------------------------------------------------------------
# Icon Helper Function
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

        # Header Frame
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

        # Form Layout
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

        # Bottom Buttons
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
# Login Window
# -------------------------------------------------------------
class LoginWidget(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setStyleSheet("background-color: #5D2E8C;")

        layout = QVBoxLayout(self)
        
        card = QFrame()
        card.setFixedSize(420, 480)
        card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 15px; }")
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("ENTRUST")
        title.setFont(QFont("Arial Black", 22))
        title.setStyleSheet("color: #2B2B2B;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Adaptive Issuance™\nInstant ID")
        subtitle.setFont(QFont("Arial", 12, QFont.Bold))
        subtitle.setStyleSheet("color: #4A4A4A;")
        subtitle.setAlignment(Qt.AlignCenter)

        notice_box = QTextEdit()
        notice_box.setReadOnly(True)
        notice_box.setFixedHeight(65)
        notice_box.setText("An evaluation license is in effect, which provides the features of Instant ID Professional edition. The license expires on October 5, 2026.")
        notice_box.setStyleSheet("background-color: #F1C40F; color: #5B4500; font-size: 11px; border-radius: 5px; border: none;")

        self.user_entry = QLineEdit()
        self.user_entry.setPlaceholderText("User ID")
        self.user_entry.setFixedHeight(35)
        self.user_entry.setStyleSheet("border: 1px solid #CBD5E1; border-radius: 5px; padding: 5px;")

        self.pass_entry = QLineEdit()
        self.pass_entry.setPlaceholderText("Password")
        self.pass_entry.setEchoMode(QLineEdit.Password)
        self.pass_entry.setFixedHeight(35)
        self.pass_entry.setStyleSheet("border: 1px solid #CBD5E1; border-radius: 5px; padding: 5px;")

        login_btn = QPushButton("Log In")
        login_btn.setFixedHeight(35)
        login_btn.setStyleSheet("QPushButton { background-color: #5D2E8C; color: white; font-weight: bold; border-radius: 5px; } QPushButton:hover { background-color: #4A2370; }")
        login_btn.clicked.connect(self.check_login)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(notice_box)
        card_layout.addWidget(QLabel("User ID"))
        card_layout.addWidget(self.user_entry)
        card_layout.addWidget(QLabel("Password"))
        card_layout.addWidget(self.pass_entry)
        card_layout.addWidget(login_btn)

        layout.addWidget(card, 0, Qt.AlignCenter)

    def check_login(self):
        if self.user_entry.text().strip() == "admin" and self.pass_entry.text().strip() == "admin123":
            self.on_login_success("admin")
        else:
            QMessageBox.critical(self, "Login Failed", "User ID သို့မဟုတ် Password မှားယွင်းနေပါသည်။\n(Default: admin / admin123)")


# -------------------------------------------------------------
# Designer Interface
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

        # Edit Title Pencil Button
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

        # Toolbar Frame
        toolbar_frame = QFrame()
        toolbar_frame.setFixedHeight(40)
        toolbar_frame.setStyleSheet("background-color: #F3F4F6; border-bottom: 1px solid #CBD5E1;")
        tb_layout = QHBoxLayout(toolbar_frame)
        tb_layout.setContentsMargins(5, 0, 5, 0)

        tools = [
            ("↶", "Undo"), ("↷", "Redo"), ("📄", "Copy"), ("✂️", "Cut"), ("📋", "Paste"),
            ("|", None),
            ("T⁭", "Text"), ("T", "Static Text"), ("👤", "Photo"), ("🖼️", "Graphic"),
            ("|", None),
            ("||||", "Bar Code"), ("💳", "Mag Stripe"), ("🎛️", "Chip")
        ]

        for icon, tooltip in tools:
            if icon == "|":
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setStyleSheet("color: #CBD5E1;")
                tb_layout.addWidget(line)
            else:
                btn = QPushButton(icon)
                btn.setFixedSize(28, 26)
                btn.setStyleSheet("QPushButton { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 3px; } QPushButton:hover { background-color: #E2E8F0; }")
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
# Main Application Window
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrust Adaptive Issuance - Instant ID")
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
