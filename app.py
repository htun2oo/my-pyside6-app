import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
)

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Background Color
        self.setStyleSheet("background-color: #1E2530;")

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Login Card Container
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

        # Title
        title = QLabel("Instant Card Studio")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #7B2CBF; border: none; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(10)

        # Username Input
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

        # Password Input
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

        # Sign In Button
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

        # Forgot Password Button
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

        if (username == "admin" and password == "1234") or (username == "" and password == ""):
            QMessageBox.information(self, "Success", "Login Successful!")
        else:
            QMessageBox.warning(self, "Login Error", "Invalid Username or Password!")

    def handle_forgot_password(self):
        QMessageBox.information(self, "Reset Password", "Please contact your system administrator to reset your password.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instant Card Studio - Login")
        self.resize(1100, 700)

        # Set Login Widget as Central Widget directly
        self.login_widget = LoginWidget()
        self.setCentralWidget(self.login_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
