import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QLinearGradient, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, QMessageBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QToolButton
)

# -------------------------------------------------------------
# 1. Custom Vector Icons for Card Editor
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

        self.setStyleSheet("background-color: #1E2530;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(360, 420)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(12)

        title = QLabel("Instant Card Studio")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #7B2CBF; border: none; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(10)

        user_lbl = QLabel("Username:")
        user_lbl.setStyleSheet("color: #4A5568; font-weight: bold; border: none; background: transparent;")
        card_layout.addWidget(user_lbl)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter username")
        self.user_input.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #8E44AD;
                border-radius: 5px;
                padding: 8px;
                background-color: #FAFAFA;
                color: #1A202C;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #6C5CE7;
                background-color: #FFFFFF;
            }
        """)
        card_layout.addWidget(self.user_input)

        pass_lbl = QLabel("Password:")
        pass_lbl.setStyleSheet("color: #4A5568; font-weight: bold; border: none; background: transparent;")
        card_layout.addWidget(pass_lbl)

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Enter password")
        self.pass_input.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #BDC3C7;
                border-radius: 5px;
                padding: 8px;
                background-color: #FAFAFA;
                color: #1A202C;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #6C5CE7;
                background-color: #FFFFFF;
            }
        """)
        self.pass_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.pass_input)

        card_layout.addSpacing(10)

        login_btn = QPushButton("Sign In")
        login_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B2CBF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #6A00B8;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)

        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #2563EB;
                font-size: 12px;
                font-weight: 600;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #1D4ED8;
            }
        """)
        forgot_btn.clicked.connect(self.handle_forgot_password)
        card_layout.addWidget(forgot_btn, alignment=Qt.AlignCenter)

        layout.addWidget(card)

    def handle_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if username == "admin" and password == "1234":
            self.on_login_success()
        elif username == "" and password == "":
            self.on_login_success()
        else:
            QMessageBox.warning(self, "Login Error", "Invalid Username or Password!")

    def handle_forgot_password(self):
        QMessageBox.information(self, "Reset Password", "Please contact your system administrator to reset your password.")


# -------------------------------------------------------------
# 3. Card Designer Component
# -------------------------------------------------------------

class CardDesignerWidget(QWidget):
    def __init__(self, card_name="Credential Design 1"):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Purple Ribbon Title
        purple_ribbon = QFrame()
        purple_ribbon.setFixedHeight(45)
        purple_ribbon.setStyleSheet("background-color: #830093;")
        
        purple_layout = QHBoxLayout(purple_ribbon)
        purple_layout.setContentsMargins(18, 0, 18, 0)
        purple_layout.setSpacing(12)

        title_lbl = QLabel(card_name)
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Medium))
        title_lbl.setStyleSheet("color: #FFFFFF; background: transparent;")
        purple_layout.addWidget(title_lbl)

        self.pencil_btn = CustomPencilButton()
        purple_layout.addWidget(self.pencil_btn)

        purple_layout.addStretch()
        main_layout.addWidget(purple_ribbon)

        # Toolbar
        toolbar = QFrame()
        toolbar.setFixedHeight(46)
        toolbar.setStyleSheet("background-color: #7F7F7F;")
        
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 6, 12, 6)
        tb_layout.setSpacing(12)

        # Undo/Redo Group
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

        # Copy/Cut/Paste Group
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
# 4. Main Dashboard Widget
# -------------------------------------------------------------

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- White Top Bar with Centered Tabs ---
        top_bar = QFrame()
        top_bar.setFixedHeight(48)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #DCDCDC;")
        
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        # Left Title
        title_lbl = QLabel("Instant Card Studio")
        title_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_lbl.setStyleSheet("color: #444444; border: none;")
        top_layout.addWidget(title_lbl)

        top_layout.addStretch()

        # Tabs on the White Top Bar
        self.nav_tabs = QTabWidget()
        self.nav_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: transparent;
                color: #555555;
                font-weight: 600;
                font-size: 13px;
                padding: 12px 18px;
                border: none;
            }
            QTabBar::tab:selected {
                color: #8E44AD;
                font-weight: bold;
                border-bottom: 3px solid #8E44AD;
            }
            QTabBar::tab:hover {
                color: #8E44AD;
            }
        """)

        top_layout.addWidget(self.nav_tabs)
        top_layout.addStretch()

        layout.addWidget(top_bar)

        # Content Pages
        self.home_page = self.create_home_view()
        self.design_page = CardDesignerWidget("Credential Design 1")
        self.printer_page = self.create_printer_queues_view()

        self.nav_tabs.addTab(self.home_page, "Home")
        self.nav_tabs.addTab(self.design_page, "Design ▾")
        self.nav_tabs.addTab(self.printer_page, "Printer Queues")

        # Open Design tab by default
        self.nav_tabs.setCurrentIndex(1)

        layout.addWidget(self.nav_tabs, stretch=1)

    # ---------------------------------------------------------
    # Helper Views
    # ---------------------------------------------------------

    def create_home_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)

        lbl = QLabel("Home View Content")
        lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        lbl.setStyleSheet("color: #333333;")
        layout.addWidget(lbl)
        layout.addStretch()

        return widget

    def create_printer_queues_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        table = QTableWidget(3, 4)
        table.setHorizontalHeaderLabels(["Job ID", "Card Template", "Status", "Progress"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                gridline-color: #E2E8F0;
                border: 1px solid #CBD5E0;
            }
            QHeaderView::section {
                background-color: #EDF2F7;
                font-weight: bold;
                border: 1px solid #CBD5E0;
                padding: 6px;
            }
        """)

        sample_data = [
            ("JOB-1001", "Credential Design 1", "Printing...", "75%"),
            ("JOB-1002", "Credential Design 1", "Queued", "0%"),
            ("JOB-1003", "Visitor Pass B", "Queued", "0%")
        ]

        for row, data in enumerate(sample_data):
            for col, text in enumerate(data):
                table.setItem(row, col, QTableWidgetItem(text))

        layout.addWidget(table)
        return widget


# -------------------------------------------------------------
# 5. Main Window Container (Login Stack Restored)
# -------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instant Card Studio")
        self.resize(1100, 700)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_page = LoginWidget(on_login_success=self.show_dashboard)
        self.dashboard_page = DashboardWidget()

        self.stacked_widget.addWidget(self.login_page)     # Index 0
        self.stacked_widget.addWidget(self.dashboard_page)  # Index 1

        # Restored Login Screen First
        self.stacked_widget.setCurrentIndex(0)

    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
