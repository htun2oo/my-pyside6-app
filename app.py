import sys
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor, QPen, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QToolButton, QFrame
)

# -------------------------------------------------------------
# ဒုတိယပုံအတိုင်း Dark Blue Icons များ ဖန်တီးပေးသည့် Helper
# -------------------------------------------------------------
def get_action_icon(action_type, color="#002B66", size=24):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, True)
    
    pen = QPen(QColor(color), 2)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)

    if action_type == "undo":
        path = QPainterPath()
        path.arcMoveTo(4, 5, 16, 16, 40)
        path.arcTo(4, 5, 16, 16, 40, 210)
        p.drawPath(path)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(3, 8), QPointF(9, 3), QPointF(9, 11)])

    elif action_type == "redo":
        path = QPainterPath()
        path.arcMoveTo(4, 5, 16, 16, 140)
        path.arcTo(4, 5, 16, 16, 140, -210)
        p.drawPath(path)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(21, 8), QPointF(15, 3), QPointF(15, 11)])

    elif action_type == "copy":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawRoundedRect(QRectF(5, 4, 10, 12), 1, 1)
        p.setBrush(QColor("#EAEFF5"))
        p.drawRoundedRect(QRectF(9, 8, 10, 12), 1, 1)

    elif action_type == "cut":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawEllipse(4, 15, 5, 5)
        p.drawEllipse(15, 15, 5, 5)
        p.drawLine(6.5, 15.5, 16, 4)
        p.drawLine(17.5, 15.5, 8, 4)

    elif action_type == "paste":
        p.setPen(QPen(QColor(color), 1.8))
        p.setBrush(QColor(color))
        p.drawRoundedRect(QRectF(6, 4, 12, 16), 1, 1)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(QRectF(9, 7, 11, 14), 1, 1)
        p.drawRect(QRectF(9, 2, 6, 3))

    p.end()
    return QIcon(pixmap)


# -------------------------------------------------------------
# ဒုတိယပုံပါ Button Style နှင့် Icon Grouping သီးသန့် Widget
# -------------------------------------------------------------
class ActionToolbarGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ဒုတိယပုံပါ ခလုတ်များ၏ Border, Gap နှင့် Highlight Styling
        btn_style = """
            QToolButton {
                background-color: #F4F4F4;
                border: 1px solid #B0B0B0;
                margin-right: -1px;
            }
            QToolButton:hover {
                background-color: #E2E8F0;
            }
            QToolButton:pressed {
                background-color: #CBD5E1;
            }
        """

        # Group 1: Undo & Redo
        self.btn_undo = QToolButton()
        self.btn_undo.setFixedSize(30, 28)
        self.btn_undo.setIcon(get_action_icon("undo"))
        self.btn_undo.setStyleSheet(btn_style)

        self.btn_redo = QToolButton()
        self.btn_redo.setFixedSize(30, 28)
        self.btn_redo.setIcon(get_action_icon("redo"))
        self.btn_redo.setStyleSheet(btn_style)

        # Spacer (Group နှစ်ခုကြား ခြားရန်)
        sep = QFrame()
        sep.setFixedWidth(8)

        # Group 2: Copy, Cut & Paste
        self.btn_copy = QToolButton()
        self.btn_copy.setFixedSize(30, 28)
        self.btn_copy.setIcon(get_action_icon("copy"))
        self.btn_copy.setStyleSheet(btn_style)

        self.btn_cut = QToolButton()
        self.btn_cut.setFixedSize(30, 28)
        self.btn_cut.setIcon(get_action_icon("cut"))
        self.btn_cut.setStyleSheet(btn_style)

        self.btn_paste = QToolButton()
        self.btn_paste.setFixedSize(30, 28)
        self.btn_paste.setIcon(get_action_icon("paste"))
        self.btn_paste.setStyleSheet(btn_style)

        # Layout ထဲသို့ ထည့်သွင်းခြင်း
        layout.addWidget(self.btn_undo)
        layout.addWidget(self.btn_redo)
        layout.addWidget(sep)
        layout.addWidget(self.btn_copy)
        layout.addWidget(self.btn_cut)
        layout.addWidget(self.btn_paste)


# -------------------------------------------------------------
# စမ်းသပ်ကြည့်ရှုနိုင်သည့် Main Window
# -------------------------------------------------------------
class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toolbar Action Group Test")
        self.setStyleSheet("background-color: #D6D6D6;")

        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Action Toolbar Component ကို ထည့်သွင်းခြင်း
        self.action_group = ActionToolbarGroup()
        main_layout.addWidget(self.action_group)
        main_layout.addStretch()

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.resize(300, 80)
    window.show()
    sys.exit(app.exec())
