import sys
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QPen, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QComboBox, QCheckBox,
    QToolButton, QDialog, QLineEdit, QTextEdit
)

# -------------------------------------------------------------
# Vector Icon Painter Helpers (ဒုတိယပုံအတိုင်း အပြာရောင် Icons များ)
# -------------------------------------------------------------
def make_toolbar_icon(icon_type, color="#002D62", size=24):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, True)
    
    pen = QPen(QColor(color), 2)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)

    if icon_type == "undo":
        path = QPainterPath()
        path.arcMoveTo(4, 4, 16, 16, 45)
        path.arcTo(4, 4, 16, 16, 45, 200)
        p.drawPath(path)
        # Arrowhead
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(4, 7), QPointF(9, 3), QPointF(9, 10)])

    elif icon_type == "redo":
        path = QPainterPath()
        path.arcMoveTo(4, 4, 16, 16, 135)
        path.arcTo(4, 4, 16, 16, 135, -200)
        p.drawPath(path)
        # Arrowhead
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(20, 7), QPointF(15, 3), QPointF(15, 10)])

    elif icon_type == "copy":
        p.setPen(QPen(QColor(color), 1.8))
        # Back Doc
        p.drawRoundedRect(QRectF(5, 4, 10, 12), 1, 1)
        # Front Doc
        p.setBrush(QColor("#F0F4F8"))
        p.drawRoundedRect(QRectF(9, 8, 10, 12), 1, 1)

    elif icon_type == "cut":
        p.setPen(QPen(QColor(color), 1.8))
        # Handles
        p.drawEllipse(4, 15, 5, 5)
        p.drawEllipse(15, 15, 5, 5)
        # Blades
        p.drawLine(6.5, 15.5, 16, 4)
        p.drawLine(17.5, 15.5, 8, 4)

    elif icon_type == "paste":
        p.setPen(QPen(QColor(color), 1.8))
        # Clipboard back
        p.setBrush(QColor(color))
        p.drawRoundedRect(QRectF(6, 4, 12, 16), 1, 1)
        # Paper
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(QRectF(9, 7, 11, 14), 1, 1)
        # Top Clip
        p.drawRect(QRectF(9, 2, 6, 3))

    p.end()
    return QIcon(pixmap)


# -------------------------------------------------------------
# Custom Edit Button (Hover to Expand Text)
# -------------------------------------------------------------
class HoverEditButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("✏", parent)
        self.setFixedHeight(24)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #1E293B;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
                padding: 0 6px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)

    def enterEvent(self, event):
        self.setText("✏ Edit Properties")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setText("✏")
        super().leaveEvent(event)


# -------------------------------------------------------------
# Edit Properties Dialog
# -------------------------------------------------------------
class EditPropertiesDialog(QDialog):
    def __init__(self, current_name="Credential Design 1", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setFixedSize(410, 560)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; border: 1px solid #000000; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(34)
        header.setStyleSheet("background-color: #7B0082;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 0, 8, 0)

        title = QLabel("Edit Properties")
        title.setFont(QFont("Arial", 9.5, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF;")

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("QPushButton { background: #6B0072; color: #FFFFFF; border: none; border-radius: 10px; }")
        close_btn.clicked.connect(self.reject)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        layout.addWidget(header)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(16, 12, 16, 12)
        
        lbl_name = QLabel("Name")
        self.txt_name = QLineEdit(current_name)
        self.txt_name.setFixedSize(230, 26)

        form_layout.addWidget(lbl_name)
        form_layout.addWidget(self.txt_name)
        layout.addWidget(form_widget, stretch=1)

        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(44)
        bottom_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        bb_layout = QHBoxLayout(bottom_bar)
        
        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(72, 28)
        btn_ok.setStyleSheet("background-color: #0284C7; color: #FFFFFF; font-weight: bold;")
        btn_ok.clicked.connect(self.accept)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(72, 28)
        btn_cancel.clicked.connect(self.reject)

        bb_layout.addWidget(btn_ok)
        bb_layout.addWidget(btn_cancel)
        bb_layout.addStretch()
        layout.addWidget(bottom_bar)

    def get_updated_name(self):
        return self.txt_name.text()


# -------------------------------------------------------------
# Credential Design Editor View
# -------------------------------------------------------------
class CredentialDesignEditorView(QWidget):
    def __init__(self, on_close_callback=None):
        super().__init__()
        self.setStyleSheet("background-color: #EFEFEF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Editing Toolbar (ဒုတိယပုံအတိုင်း အတိအကျ Styling)
        editor_toolbar = QFrame()
        editor_toolbar.setFixedHeight(34)
        editor_toolbar.setStyleSheet("background-color: #D6D6D6; border-bottom: 1px solid #B0B0B0;")
        tb_layout = QHBoxLayout(editor_toolbar)
        tb_layout.setContentsMargins(4, 3, 4, 3)
        tb_layout.setSpacing(0)

        btn_style = """
            QToolButton {
                background-color: #F4F4F4;
                border: 1px solid #B0B0B0;
                margin-right: -1px;
            }
            QToolButton:hover {
                background-color: #E0E0E0;
            }
        """

        # Group 1: Undo / Redo
        grp1 = QHBoxLayout()
        grp1.setSpacing(0)
        
        btn_undo = QToolButton()
        btn_undo.setFixedSize(28, 26)
        btn_undo.setIcon(make_toolbar_icon("undo"))
        btn_undo.setToolTip("Undo")
        btn_undo.setStyleSheet(btn_style)

        btn_redo = QToolButton()
        btn_redo.setFixedSize(28, 26)
        btn_redo.setIcon(make_toolbar_icon("redo"))
        btn_redo.setToolTip("Redo")
        btn_redo.setStyleSheet(btn_style)

        grp1.addWidget(btn_undo)
        grp1.addWidget(btn_redo)

        sep1 = QFrame()
        sep1.setFixedWidth(8)

        # Group 2: Copy / Cut / Paste
        grp2 = QHBoxLayout()
        grp2.setSpacing(0)

        btn_copy = QToolButton()
        btn_copy.setFixedSize(28, 26)
        btn_copy.setIcon(make_toolbar_icon("copy"))
        btn_copy.setToolTip("Copy")
        btn_copy.setStyleSheet(btn_style)

        btn_cut = QToolButton()
        btn_cut.setFixedSize(28, 26)
        btn_cut.setIcon(make_toolbar_icon("cut"))
        btn_cut.setToolTip("Cut")
        btn_cut.setStyleSheet(btn_style)

        btn_paste = QToolButton()
        btn_paste.setFixedSize(28, 26)
        btn_paste.setIcon(make_toolbar_icon("paste"))
        btn_paste.setToolTip("Paste")
        btn_paste.setStyleSheet(btn_style)

        grp2.addWidget(btn_copy)
        grp2.addWidget(btn_cut)
        grp2.addWidget(btn_paste)

        tb_layout.addLayout(grp1)
        tb_layout.addWidget(sep1)
        tb_layout.addLayout(grp2)

        sep2 = QFrame()
        sep2.setFixedWidth(8)
        tb_layout.addWidget(sep2)

        other_tools = ["🗑", "T", "👤", "📷", "📊", "▦", "▤", "║", "▭", "╱", "◯"]
        for tool in other_tools:
            btn = QToolButton()
            btn.setText(tool)
            btn.setFixedSize(26, 26)
            btn.setStyleSheet("QToolButton { background-color: #FFFFFF; border: 1px solid #CBD5E1; margin: 1px; } QToolButton:hover { background-color: #E2E8F0; }")
            tb_layout.addWidget(btn)

        tb_layout.addStretch()
        main_layout.addWidget(editor_toolbar)

        # Canvas Area
        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)

        canvas_container = QWidget()
        canvas_container.setStyleSheet("background-color: #B3B3B3;")
        canvas_layout = QHBoxLayout(canvas_container)

        front_box = QVBoxLayout()
        front_title = QLabel("Front Side")
        front_title.setFont(QFont("Arial", 9, QFont.Bold))
        front_box.addWidget(front_title)

        front_card_bg = QFrame()
        front_card_bg.setFixedSize(300, 380)
        front_card_bg.setStyleSheet("background-color: #8C8C8C;")
        front_box.addWidget(front_card_bg)

        canvas_layout.addLayout(front_box)
        canvas_layout.addStretch()

        content_layout.addWidget(canvas_container, stretch=1)
        main_layout.addWidget(content_area, stretch=1)

        # Bottom Action Bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(40)
        bottom_bar.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #CBD5E1;")
        bb_layout = QHBoxLayout(bottom_bar)

        btn_close = QPushButton("Close")
        btn_close.setFixedSize(70, 28)
        if on_close_callback:
            btn_close.clicked.connect(on_close_callback)

        bb_layout.addWidget(btn_close)
        bb_layout.addStretch()
        main_layout.addWidget(bottom_bar)


# -------------------------------------------------------------
# Main Application Dashboard
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.current_title = "Credential Design 1"
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Purple Navigation Bar
        self.purple_bar = QFrame()
        self.purple_bar.setFixedHeight(34)
        self.purple_bar.setStyleSheet("background-color: #7B0082;")
        self.purple_layout = QHBoxLayout(self.purple_bar)
        self.purple_layout.setContentsMargins(10, 0, 20, 0)

        main_layout.addWidget(self.purple_bar)

        # Editor Stack
        self.editor_page = CredentialDesignEditorView()
        main_layout.addWidget(self.editor_page, stretch=1)

        self.update_purple_bar_title()

    def update_purple_bar_title(self):
        while self.purple_layout.count() > 0:
            item = self.purple_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        title_lbl = QLabel(self.current_title)
        title_lbl.setFont(QFont("Arial", 11, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; padding-left: 10px;")

        edit_icon_btn = HoverEditButton(self)
        edit_icon_btn.clicked.connect(self.show_edit_properties_dialog)

        self.purple_layout.addWidget(title_lbl)
        self.purple_layout.addSpacing(6)
        self.purple_layout.addWidget(edit_icon_btn)
        self.purple_layout.addStretch()

    def show_edit_properties_dialog(self):
        dialog = EditPropertiesDialog(current_name=self.current_title, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.current_title = dialog.get_updated_name()
            self.update_purple_bar_title()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Instant ID Design View")
        self.resize(1120, 640)
        self.setCentralWidget(EntrustDashboard())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
