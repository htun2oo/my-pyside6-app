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
        self.setStyleSheet("background-color: #1E2530;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Card Container
        card = QFrame()
        card.setFixedSize(360, 380)
        card.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

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
                border: 1.5px solid #BDC3C7;
                border-radius: 5px;
                padding: 8px;
                background-color: #FAFAFA;
                color: #1A202C;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #7B2CBF;
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
                border: 2px solid #7B2CBF;
                background-color: #FFFFFF;
            }
        """)
        self.pass_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.pass_input)

        card_layout.addSpacing(15)

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

        layout.addWidget(card)

    def handle_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if (username == "admin" and password == "1234") or (username == "" and password == ""):
            QMessageBox.information(self, "Success", "Login Successful!")
        else:
            QMessageBox.warning(self, "Login Error", "Invalid Username or Password!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instant Card Studio")
        self.resize(1100, 700)
        self.setCentralWidget(LoginWidget())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
