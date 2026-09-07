import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QLinearGradient, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, QMessageBox
)

# -------------------------------------------------------------
# 1. Custom Vector Icons
# -------------------------------------------------------------

class CustomPencilButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(32, 32)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        rect = QRectF(0, 0, self.width(), self.height())
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor("#FFFFFF"))
        grad.setColorAt(0.5, QColor("#E3EEFF"))
        grad.setColorAt(1.0, QColor("#CBE0FC"))

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor("#B0C8E8"), 1))
        painter.drawRoundedRect(rect, 6, 6)

        painter.save()
        painter.translate(16, 16)
        painter.rotate(-45)

        dark_blue = QColor("#1C3B6F")
        light_blue = QColor("#6DA5E3")

        painter.setBrush(QBrush(dark_blue))
        painter.setPen(Qt.NoPen)
        painter.drawRect(-3, -7, 6, 11)

        painter.setBrush(QBrush(light_blue))
        painter.drawRect(-1, -7, 2, 11)

        path = QPainterPath()
        path.moveTo(-3, 4)
        path.lineTo(3, 4)
        path.lineTo(0, 9)
        path.closeSubpath()
        painter.setBrush(QBrush(dark_blue))
        painter.drawPath(path)

        painter.setBrush(QBrush(QColor("#1C3B6F")))
        painter.drawRoundedRect(-3, -10, 6, 3, 1, 1)

        painter.restore()


class CustomUndoButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(38, 34)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        painter.save()
        painter.setPen(QPen(QColor("#082046"), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        path = QPainterPath()
        path.moveTo(27, 24)
        path.cubicTo(27, 12, 12, 12, 12, 19)
        painter.drawPath(path)

        head = QPainterPath()
        head.moveTo(17, 14)
        head.lineTo(10, 19)
        head.lineTo(16, 25)
        painter.setBrush(QBrush(QColor("#082046")))
        painter.setPen(Qt.NoPen)
        painter.drawPath(head)

        painter.restore()


class CustomRedoButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(38, 34)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        painter.save()
        painter.setPen(QPen(QColor("#082046"), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        path = QPainterPath()
        path.moveTo(11, 24)
        path.cubicTo(11, 12, 26, 12, 26, 19)
        painter.drawPath(path)

        head = QPainterPath()
        head.moveTo(21, 14)
        head.lineTo(28, 19)
        head.lineTo(22, 25)
        painter.setBrush(QBrush(QColor("#082046")))
        painter.setPen(Qt.NoPen)
        painter.drawPath(head)

        painter.restore()


class CustomCopyButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(38, 34)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        pen = QPen(QColor("#082046"), 2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("#FFFFFF")))

        painter.drawRoundedRect(11, 9, 13, 15, 1, 1)
        painter.drawRoundedRect(15, 13, 13, 15, 1, 1)


class CustomCutButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(38, 34)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        painter.setPen(QPen(QColor("#082046"), 2))
        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(10, 20, 7, 7)
        painter.drawEllipse(10, 8, 7, 7)

        painter.drawLine(16, 22, 27, 10)
        painter.drawLine(16, 12, 27, 24)


class CustomPasteButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(38, 34)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        pen = QPen(QColor("#082046"), 2)
        painter.setPen(pen)

        painter.setBrush(QBrush(QColor("#082046")))
        painter.drawRoundedRect(10, 9, 15, 18, 2, 2)

        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawRoundedRect(14, 12, 14, 17, 1, 1)


# -------------------------------------------------------------
# 2. Login Screen Widget
# -------------------------------------------------------------

class LoginWidget(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success

        self.setStyleSheet("background-color: #2D3748;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(320, 360)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 8px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        title = QLabel("ENTRUST Login")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #830093; border: none;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(10)

        # Username Input
        user_lbl = QLabel("Username:")
        user_lbl.setStyleSheet("color: #4A5568; font-weight: bold; border: none;")
        card_layout.addWidget(user_lbl)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter username")
        self.user_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CBD5E0;
                border-radius: 4px;
                padding: 6px;
                background-color: #F7FAFC;
            }
            QLineEdit:focus {
                border: 1px solid #830093;
            }
        """)
        card_layout.addWidget(self.user_input)

        # Password Input
        pass_lbl = QLabel("Password:")
        pass_lbl.setStyleSheet("color: #4A5568; font-weight: bold; border: none;")
        card_layout.addWidget(pass_lbl)

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Enter password")
        self.pass_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CBD5E0;
                border-radius: 4px;
                padding: 6px;
                background-color: #F7FAFC;
            }
            QLineEdit:focus {
                border: 1px solid #830093;
            }
        """)
        self.pass_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.pass_input)

        card_layout.addSpacing(10)

        # Login Button
        login_btn = QPushButton("Sign In")
        login_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #830093;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #6B007B;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)

        layout.addWidget(card)

    def handle_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        # Simple verification check
        if username == "admin" and password == "1234":
            self.on_login_success()
        elif username == "" and password == "":
            self.on_login_success()  # Allow empty login for quick test
        else:
            QMessageBox.warning(self, "Login Error", "Invalid Username or Password!")


# -------------------------------------------------------------
# 3. Card Designer Screen Widget
# -------------------------------------------------------------

class CardDesignerWidget(QWidget):
    def __init__(self, card_name="Credential Design 1"):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Purple Ribbon
        purple_ribbon = QFrame()
        purple_ribbon.setFixedHeight(54)
        purple_ribbon.setStyleSheet("background-color: #830093;")
        
        purple_layout = QHBoxLayout(purple_ribbon)
        purple_layout.setContentsMargins(18, 0, 18, 0)
        purple_layout.setSpacing(12)

        title_lbl = QLabel(card_name)
        title_lbl.setFont(QFont("Segoe UI", 18, QFont.Medium))
        title_lbl.setStyleSheet("color: #FFFFFF; background: transparent;")
        purple_layout.addWidget(title_lbl)

        self.pencil_btn = CustomPencilButton()
        purple_layout.addWidget(self.pencil_btn)

        purple_layout.addStretch()
        main_layout.addWidget(purple_ribbon)

        # Toolbar Section
        toolbar = QFrame()
        toolbar.setFixedHeight(48)
        toolbar.setStyleSheet("background-color: #7F7F7F;")
        
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 6, 12, 6)
        tb_layout.setSpacing(12)

        # Undo/Redo Frame
        ur_frame = QFrame()
        ur_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #EAEAEA, stop:1 #D3D3D3);
                border: 1px solid #A0A0A0;
                border-radius: 1px;
            }
        """)
        ur_layout = QHBoxLayout(ur_frame)
        ur_layout.setContentsMargins(0, 0, 0, 0)
        ur_layout.setSpacing(0)

        self.undo_btn = CustomUndoButton()
        self.redo_btn = CustomRedoButton()

        self.undo_btn.setStyleSheet("border-right: 1px solid #C0C0C0;")
        self.redo_btn.setStyleSheet("border: none;")

        ur_layout.addWidget(self.undo_btn)
        ur_layout.addWidget(self.redo_btn)
        tb_layout.addWidget(ur_frame)

        # Copy/Cut/Paste Frame
        clip_frame = QFrame()
        clip_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #EAEAEA);
                border: 1px solid #A0A0A0;
                border-radius: 1px;
            }
        """)
        clip_layout = QHBoxLayout(clip_frame)
        clip_layout.setContentsMargins(0, 0, 0, 0)
        clip_layout.setSpacing(0)

        self.copy_btn = CustomCopyButton()
        self.cut_btn = CustomCutButton()
        self.paste_btn = CustomPasteButton()

        self.copy_btn.setStyleSheet("border-right: 1px solid #D0D0D0;")
        self.cut_btn.setStyleSheet("border-right: 1px solid #D0D0D0;")
        self.paste_btn.setStyleSheet("border: none;")

        clip_layout.addWidget(self.copy_btn)
        clip_layout.addWidget(self.cut_btn)
        clip_layout.addWidget(self.paste_btn)
        tb_layout.addWidget(clip_frame)

        tb_layout.addStretch()
        main_layout.addWidget(toolbar)

        canvas_bg = QFrame()
        canvas_bg.setStyleSheet("background-color: #E2E8F0;")
        main_layout.addWidget(canvas_bg, stretch=1)


# -------------------------------------------------------------
# 4. Main Window with Page Switching (Stacked Widget)
# -------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Credential Design Editor")
        self.resize(1000, 600)

        # Stacked Widget for Page Management
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create Pages
        self.login_page = LoginWidget(on_login_success=self.show_designer)
        self.designer_page = CardDesignerWidget("Credential Design 1")

        # Add Pages to Stack
        self.stacked_widget.addWidget(self.login_page)     # Index 0
        self.stacked_widget.addWidget(self.designer_page)  # Index 1

        # Show Login Page First
        self.stacked_widget.setCurrentIndex(0)

    def show_designer(self):
        self.stacked_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
