import sys
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QPen, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QComboBox, QCheckBox,
    QToolButton, QDialog, QLineEdit, QTextEdit
)

# -------------------------------------------------------------
# Toolbar & Custom Vector Icon Painter
# -------------------------------------------------------------
def make_toolbar_icon(icon_type, color="#002D62", size=32):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, True)
    
    pen = QPen(QColor(color), 2.2)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)

    if icon_type == "undo":
        path = QPainterPath()
        path.arcMoveTo(4, 6, 24, 24, 45)
        path.arcTo(4, 6, 24, 24, 45, 200)
        p.drawPath(path)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(4, 10), QPointF(12, 4), QPointF(12, 14)])

    elif icon_type == "redo":
        path = QPainterPath()
        path.arcMoveTo(4, 6, 24, 24, 135)
        path.arcTo(4, 6, 24, 24, 135, -200)
        p.drawPath(path)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(28, 10), QPointF(20, 4), QPointF(20, 14)])

    elif icon_type == "copy":
        p.drawRoundedRect(QRectF(5, 4, 14, 16), 2, 2)
        p.setBrush(QColor("#F0F4F8"))
        p.drawRoundedRect(QRectF(11, 10, 14, 16), 2, 2)

    elif icon_type == "cut":
        p.drawEllipse(4, 20, 7, 7)
        p.drawEllipse(21, 20, 7, 7)
        p.drawLine(8.5, 20.5, 22, 5)
        p.drawLine(23.5, 20.5, 10, 5)

    elif icon_type == "paste":
        p.setBrush(QColor(color))
        p.drawRoundedRect(QRectF(7, 6, 18, 22), 2, 2)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(QRectF(11, 10, 15, 18), 2, 2)
        p.drawRect(QRectF(11, 3, 10, 5))

    elif icon_type == "text":
        p.setFont(QFont("Times New Roman", 18, QFont.Bold))
        p.setPen(QPen(QColor(color)))
        p.drawText(QRectF(2, 2, 18, 20), Qt.AlignLeft | Qt.AlignTop, "T")
        p.setPen(QPen(QColor(color), 2.0))
        p.drawRect(QRectF(15, 15, 14, 14))
        p.drawLine(22, 17, 22, 26)
        p.drawLine(19, 17, 25, 17)

    elif icon_type == "static_text":
        p.setFont(QFont("Times New Roman", 20, QFont.Bold))
        p.setPen(QPen(QColor(color)))
        p.drawText(QRectF(0, 0, 32, 32), Qt.AlignCenter, "T")

    elif icon_type == "photo":
        p.drawRect(QRectF(3, 5, 26, 22))
        p.setBrush(QColor(color))
        p.drawEllipse(13, 8, 6, 6)
        path = QPainterPath()
        path.moveTo(9, 24)
        path.arcTo(9, 15, 14, 12, 0, 180)
        p.drawPath(path)

    elif icon_type == "static_graphic":
        p.drawRect(QRectF(3, 5, 26, 22))
        p.setBrush(QColor(color))
        poly = [QPointF(5, 24), QPointF(12, 15), QPointF(18, 21), QPointF(22, 15), QPointF(27, 24)]
        p.drawPolygon(poly)

    elif icon_type == "variable_graphic":
        p.setPen(QPen(QColor(color), 2.0))
        p.drawRect(QRectF(2, 2, 18, 17))
        p.drawRect(QRectF(7, 7, 18, 17))
        p.setPen(QPen(QColor(color), 2.2))
        p.drawArc(19, 19, 10, 10, 0, 270 * 16)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(26, 18), QPointF(30, 23), QPointF(21, 23)])

    elif icon_type == "date":
        p.drawRect(QRectF(4, 4, 24, 24))
        p.setBrush(QColor(color))
        for r in range(3):
            for c in range(3):
                p.drawRect(QRectF(9 + c*6, 9 + r*6, 3, 3))

    elif icon_type == "signature":
        p.drawRect(QRectF(4, 6, 24, 20))
        p.setPen(QPen(QColor(color), 2.4))
        p.drawLine(3, 24, 8, 5)
        path = QPainterPath()
        path.moveTo(8, 18)
        path.cubicTo(14, 10, 16, 22, 22, 14)
        path.cubicTo(24, 12, 26, 18, 28, 18)
        p.drawPath(path)

    elif icon_type == "barcode":
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(color))
        bars = [(3, 2), (7, 2), (11, 4), (17, 2), (21, 3), (26, 2)]
        for x, w in bars:
            p.drawRect(QRectF(x, 5, w, 22))

    elif icon_type == "magnetic_stripe":
        p.drawRoundedRect(QRectF(3, 5, 26, 22), 2.5, 2.5)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(color))
        p.drawRect(QRectF(3, 10, 26, 6))

    elif icon_type == "chip":
        p.setPen(QPen(QColor(color), 2.2))
        p.drawRoundedRect(QRectF(3, 3, 26, 26), 4, 4)
        p.drawLine(3, 16, 10, 16)
        p.drawLine(22, 16, 29, 16)
        p.drawLine(16, 3, 16, 10)
        p.drawLine(16, 22, 16, 29)
        p.drawEllipse(QRectF(10, 10, 12, 12))

    elif icon_type == "line":
        p.drawLine(4, 28, 28, 4)

    elif icon_type == "rectangle":
        p.drawRect(QRectF(4, 4, 24, 24))

    elif icon_type == "ellipse":
        p.drawEllipse(QRectF(3, 3, 26, 26))

    elif icon_type == "ruler":
        p.drawRoundedRect(QRectF(3, 8, 26, 16), 2, 2)
        p.drawLine(8, 17, 8, 24)
        p.drawLine(13, 19, 13, 24)
        p.drawLine(18, 17, 18, 24)
        p.drawLine(23, 19, 23, 24)

    elif icon_type == "grid_lines":
        p.drawRect(QRectF(3, 3, 26, 26))
        p.drawLine(11, 3, 11, 29)
        p.drawLine(19, 3, 19, 29)
        p.drawLine(3, 11, 29, 11)
        p.drawLine(3, 19, 29, 19)

    elif icon_type == "zoom_out":
        p.drawEllipse(QRectF(3, 3, 18, 18))
        p.drawLine(17, 17, 28, 28)
        p.drawLine(7, 12, 17, 12)

    elif icon_type == "zoom_in":
        p.drawEllipse(QRectF(3, 3, 18, 18))
        p.drawLine(17, 17, 28, 28)
        p.drawLine(7, 12, 17, 12)
        p.drawLine(12, 7, 12, 17)

    elif icon_type == "orientation":
        pen_card = QPen(QColor(color), 2.2)
        pen_card.setCapStyle(Qt.RoundCap)
        pen_card.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen_card)

        p.drawRoundedRect(QRectF(9, 14, 8, 14), 1.5, 1.5)
        p.drawRoundedRect(QRectF(16, 6, 12, 22), 1.5, 1.5)

        p.setPen(QPen(QColor(color), 2.0, Qt.SolidLine, Qt.RoundCap))
        arrow_path = QPainterPath()
        arrow_path.moveTo(7, 12)
        arrow_path.quadTo(7, 6, 14, 6)
        p.drawPath(arrow_path)

        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(14, 3), QPointF(18, 6), QPointF(14, 9)])

    elif icon_type == "pencil_45":
        p.save()
        p.translate(size / 2, size / 2)
        p.rotate(45)
        
        pen_body = QPen(QColor(color), 2.0)
        pen_body.setCapStyle(Qt.SquareCap)
        pen_body.setJoinStyle(Qt.MiterJoin)
        p.setPen(pen_body)
        
        p.drawRoundedRect(QRectF(-6, -13, 12, 6), 1, 1)
        p.drawRect(QRectF(-6, -7, 12, 14))
        
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(-6, 7), QPointF(6, 7), QPointF(0, 14)])
        p.restore()

    p.end()
    return QIcon(pixmap)


# -------------------------------------------------------------
# Hover Edit Button Class
# -------------------------------------------------------------
class HoverEditButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(34, 34)
        self.setCursor(Qt.PointingHandCursor)
        self.setIcon(make_toolbar_icon("pencil_45", color="#002D62", size=26))
        self.setIconSize(self.icon().actualSize(self.size()))
        self.setToolTip("Edit Properties")
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
            QToolTip {
                background-color: #1E293B;
                color: #FFFFFF;
                border: none;
                padding: 6px 10px;
                font-size: 9.5pt;
                font-family: Arial;
                border-radius: 4px;
            }
        """)


# -------------------------------------------------------------
# Grid & List Icons Helpers
# -------------------------------------------------------------
def draw_grid_icon(size=20, color="#003366"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, False)
    p.setBrush(QBrush(QColor(color)))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 0, 9, 9)
    p.drawRect(11, 0, 9, 9)
    p.drawRect(0, 11, 9, 9)
    p.drawRect(11, 11, 9, 9)
    p.end()
    return QIcon(pixmap)

def draw_list_icon(size=20, color="#003366"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, False)
    p.setBrush(QBrush(QColor(color)))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 1, 20, 4)
    p.drawRect(0, 8, 20, 4)
    p.drawRect(0, 15, 20, 4)
    p.end()
    return QIcon(pixmap)


# -------------------------------------------------------------
# Edit Properties Dialog Popup Window
# -------------------------------------------------------------
class EditPropertiesDialog(QDialog):
    def __init__(self, current_name="Credential Design 1", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setFixedSize(450, 600)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; border: 1px solid #000000; }")

        self.dim_data = {
            "ISO ID-1": {"Centimeters": (8.5725, 5.3975), "Millimeters": (85.725, 53.975)},
            "CR-50": {"Centimeters": (8.8900, 4.4450), "Millimeters": (88.900, 44.450)},
            "Custom": {"Centimeters": (8.5725, 5.3975), "Millimeters": (85.725, 53.975)}
        }

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(45)
        header.setStyleSheet("background-color: #7B0082;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 12, 0)

        title = QLabel("Edit Properties")
        title.setFont(QFont("Arial", 11, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF;")

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background: #6B0072; color: #FFFFFF; border: none; border-radius: 14px; font-weight: bold; font-size: 12px; }
            QPushButton:hover { background: #92009C; }
        """)
        close_btn.clicked.connect(self.reject)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        layout.addWidget(header)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(20, 16, 20, 16)
        form_layout.setSpacing(10)

        label_style = "color: #334155; font-size: 9.5pt; font-family: Arial; font-weight: bold;"
        
        input_style = """
            QLineEdit, QComboBox {
                border: 1px solid #94A3B8;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 9.5pt;
                font-family: Arial;
                background-color: #FFFFFF;
                color: #0F172A;
            }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #0284C7; }
            QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 24px; border-left: 1px solid #94A3B8; }
            QComboBox QAbstractItemView { border: 1px solid #94A3B8; background-color: #FFFFFF; color: #0F172A; selection-background-color: #0284C7; selection-color: #FFFFFF; padding: 4px; }
        """

        lbl_name = QLabel("Name")
        lbl_name.setStyleSheet(label_style)
        self.txt_name = QLineEdit(current_name)
        self.txt_name.setFixedSize(270, 34)
        self.txt_name.setStyleSheet(input_style)

        lbl_dim = QLabel("Dimensions")
        lbl_dim.setStyleSheet(label_style)
        self.cbo_dim = QComboBox()
        self.cbo_dim.addItems(["ISO ID-1", "CR-50", "Custom"])
        self.cbo_dim.setFixedSize(160, 34)
        self.cbo_dim.setStyleSheet(input_style)

        lbl_units = QLabel("Units")
        lbl_units.setStyleSheet(label_style)
        self.cbo_units = QComboBox()
        self.cbo_units.addItems(["Centimeters", "Millimeters"])
        self.cbo_units.setFixedSize(160, 34)
        self.cbo_units.setStyleSheet(input_style)

        lbl_width = QLabel("Width")
        lbl_width.setStyleSheet(label_style)
        width_box = QHBoxLayout()
        width_box.setSpacing(8)
        self.txt_width = QLineEdit("8.5725")
        self.txt_width.setFixedSize(140, 34)
        self.txt_width.setStyleSheet(input_style)
        self.unit_w_lbl = QLabel("centimeters")
        self.unit_w_lbl.setStyleSheet("color: #0F172A; font-size: 9.5pt; font-family: Arial;")
        width_box.addWidget(self.txt_width)
        width_box.addWidget(self.unit_w_lbl)
        width_box.addStretch()

        lbl_height = QLabel("Height")
        lbl_height.setStyleSheet(label_style)
        height_box = QHBoxLayout()
        height_box.setSpacing(8)
        self.txt_height = QLineEdit("5.3975")
        self.txt_height.setFixedSize(140, 34)
        self.txt_height.setStyleSheet(input_style)
        self.unit_h_lbl = QLabel("centimeters")
        self.unit_h_lbl.setStyleSheet("color: #0F172A; font-size: 9.5pt; font-family: Arial;")
        height_box.addWidget(self.txt_height)
        height_box.addWidget(self.unit_h_lbl)
        height_box.addStretch()

        self.cbo_dim.currentIndexChanged.connect(self.update_dimensions_and_units)
        self.cbo_units.currentIndexChanged.connect(self.update_dimensions_and_units)

        def make_checkbox_row(text):
            row = QHBoxLayout()
            row.setSpacing(6)
            chk = QCheckBox(text)
            chk.setStyleSheet("""
                QCheckBox { font-size: 9.5pt; font-family: Arial; color: #334155; }
                QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #0284C7; border-radius: 3px; background-color: #FFFFFF; }
                QCheckBox::indicator:checked { background-color: #0284C7; }
            """)
            help_btn = QLabel("?")
            help_btn.setFixedSize(20, 20)
            help_btn.setAlignment(Qt.AlignCenter)
            help_btn.setStyleSheet("background-color: #38BDF8; color: #FFFFFF; font-weight: bold; font-size: 9pt; border-radius: 10px;")
            row.addWidget(chk)
            row.addWidget(help_btn)
            row.addStretch()
            return row

        row_rewritable = make_checkbox_row("Rewritable credential")
        row_print_edge = make_checkbox_row("Print over the edge")

        lbl_desc = QLabel("Description")
        lbl_desc.setStyleSheet(label_style)
        self.txt_desc = QTextEdit()
        self.txt_desc.setFixedHeight(85)
        self.txt_desc.setStyleSheet("QTextEdit { border: 1px solid #94A3B8; border-radius: 4px; background-color: #FFFFFF; }")

        form_layout.addWidget(lbl_name)
        form_layout.addWidget(self.txt_name)
        form_layout.addWidget(lbl_dim)
        form_layout.addWidget(self.cbo_dim)
        form_layout.addWidget(lbl_units)
        form_layout.addWidget(self.cbo_units)
        form_layout.addWidget(lbl_width)
        form_layout.addLayout(width_box)
        form_layout.addWidget(lbl_height)
        form_layout.addLayout(height_box)
        form_layout.addLayout(row_rewritable)
        form_layout.addLayout(row_print_edge)
        form_layout.addWidget(lbl_desc)
        form_layout.addWidget(self.txt_desc)

        layout.addWidget(form_widget, stretch=1)

        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(56)
        bottom_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(20, 0, 20, 0)
        bb_layout.setSpacing(14)

        # Larger OK / Cancel Dialog Buttons
        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(90, 36)
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.setStyleSheet("QPushButton { background-color: #0284C7; color: #FFFFFF; font-weight: bold; font-size: 9.5pt; border: none; border-radius: 4px; } QPushButton:hover { background-color: #0369A1; }")
        btn_ok.clicked.connect(self.accept)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(90, 36)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("QPushButton { background-color: #E2E8F0; color: #1E293B; font-size: 9.5pt; border: 1px solid #CBD5E1; border-radius: 4px; } QPushButton:hover { background-color: #CBD5E1; }")
        btn_cancel.clicked.connect(self.reject)

        bb_layout.addWidget(btn_ok)
        bb_layout.addWidget(btn_cancel)
        bb_layout.addStretch()

        layout.addWidget(bottom_bar)

    def update_dimensions_and_units(self):
        selected_dim = self.cbo_dim.currentText()
        selected_unit = self.cbo_units.currentText()

        self.unit_w_lbl.setText(selected_unit.lower())
        self.unit_h_lbl.setText(selected_unit.lower())

        if selected_dim in self.dim_data and selected_unit in self.dim_data[selected_dim]:
            w_val, h_val = self.dim_data[selected_dim][selected_unit]
            self.txt_width.setText(str(w_val))
            self.txt_height.setText(str(h_val))

            if selected_dim == "Custom":
                self.txt_width.setReadOnly(False)
                self.txt_height.setReadOnly(False)
            else:
                self.txt_width.setReadOnly(True)
                self.txt_height.setReadOnly(True)

    def get_updated_name(self):
        return self.txt_name.text()


# -------------------------------------------------------------
# Toolbar View Toggle Widget
# -------------------------------------------------------------
class ViewToggleToolbar(QFrame):
    def __init__(self, on_grid_click=None, on_list_click=None, is_grid_active=True, show_create_btn=False, on_create_click=None):
        super().__init__()
        self.setFixedHeight(48)
        self.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB; }")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(0)
        layout.addStretch()

        self.grid_btn = QPushButton()
        self.grid_btn.setFixedSize(44, 34)
        self.grid_btn.setCursor(Qt.PointingHandCursor)

        self.list_btn = QPushButton()
        self.list_btn.setFixedSize(44, 34)
        self.list_btn.setCursor(Qt.PointingHandCursor)

        self.grid_btn.setIcon(draw_grid_icon(20, "#003366"))
        self.list_btn.setIcon(draw_list_icon(20, "#003366"))

        self.set_active_state(is_grid_active)

        if on_grid_click:
            self.grid_btn.clicked.connect(on_grid_click)
        if on_list_click:
            self.list_btn.clicked.connect(on_list_click)

        layout.addWidget(self.grid_btn)
        layout.addWidget(self.list_btn)

        if show_create_btn:
            layout.addSpacing(10)
            self.create_btn = QPushButton("+ Create")
            self.create_btn.setFixedHeight(34)
            self.create_btn.setFont(QFont("Arial", 9.5, QFont.Bold))
            self.create_btn.setCursor(Qt.PointingHandCursor)
            self.create_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; color: #1F2937; border: 1px solid #9CA3AF; border-radius: 4px; padding: 0 16px; } QPushButton:hover { background-color: #D1D5DB; }")
            if on_create_click:
                self.create_btn.clicked.connect(on_create_click)
            layout.addWidget(self.create_btn)

    def set_active_state(self, is_grid_active):
        if is_grid_active:
            self.grid_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #AFAFAF, stop:1 #C4C4C4); border: 1px solid #888888; border-top-left-radius: 4px; border-bottom-left-radius: 4px; }")
            self.list_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F0F0F0, stop:1 #D9D9D9); border: 1px solid #B0B0B0; border-left: none; border-top-right-radius: 4px; border-bottom-right-radius: 4px; } QPushButton:hover { background: #E0E0E0; }")
        else:
            self.grid_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F0F0F0, stop:1 #D9D9D9); border: 1px solid #B0B0B0; border-top-left-radius: 4px; border-bottom-left-radius: 4px; } QPushButton:hover { background: #E0E0E0; }")
            self.list_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #AFAFAF, stop:1 #C4C4C4); border: 1px solid #888888; border-left: none; border-top-right-radius: 4px; border-bottom-right-radius: 4px; }")


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

        # Height increased to 52px for bigger buttons
        editor_toolbar = QFrame()
        editor_toolbar.setFixedHeight(52)
        editor_toolbar.setStyleSheet("background-color: #D6D6D6; border-bottom: 1px solid #B0B0B0;")
        tb_layout = QHBoxLayout(editor_toolbar)
        tb_layout.setContentsMargins(8, 5, 8, 5)
        tb_layout.setSpacing(0)

        # Significantly enlarged button style (42x38 px)
        btn_style = """
            QToolButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #E0E0E0);
                border: 1px solid #B0B0B0;
                margin-right: -1px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F0F0F0, stop:1 #D0D0D0);
            }
            QToolTip {
                background-color: #1E293B;
                color: #FFFFFF;
                border: none;
                padding: 6px 10px;
                font-size: 9.5pt;
                font-family: Arial;
                border-radius: 4px;
            }
        """

        grp1 = QHBoxLayout()
        grp1.setSpacing(0)
        btn_undo = QToolButton()
        btn_undo.setFixedSize(42, 38)
        btn_undo.setIcon(make_toolbar_icon("undo", size=32))
        btn_undo.setIconSize(btn_undo.size())
        btn_undo.setToolTip("Undo")
        btn_undo.setStyleSheet(btn_style)

        btn_redo = QToolButton()
        btn_redo.setFixedSize(42, 38)
        btn_redo.setIcon(make_toolbar_icon("redo", size=32))
        btn_redo.setIconSize(btn_redo.size())
        btn_redo.setToolTip("Redo")
        btn_redo.setStyleSheet(btn_style)

        grp1.addWidget(btn_undo)
        grp1.addWidget(btn_redo)

        sep1 = QFrame()
        sep1.setFixedWidth(12)

        grp2 = QHBoxLayout()
        grp2.setSpacing(0)
        btn_copy = QToolButton()
        btn_copy.setFixedSize(42, 38)
        btn_copy.setIcon(make_toolbar_icon("copy", size=32))
        btn_copy.setIconSize(btn_copy.size())
        btn_copy.setToolTip("Copy")
        btn_copy.setStyleSheet(btn_style)

        btn_cut = QToolButton()
        btn_cut.setFixedSize(42, 38)
        btn_cut.setIcon(make_toolbar_icon("cut", size=32))
        btn_cut.setIconSize(btn_cut.size())
        btn_cut.setToolTip("Cut")
        btn_cut.setStyleSheet(btn_style)

        btn_paste = QToolButton()
        btn_paste.setFixedSize(42, 38)
        btn_paste.setIcon(make_toolbar_icon("paste", size=32))
        btn_paste.setIconSize(btn_paste.size())
        btn_paste.setToolTip("Paste")
        btn_paste.setStyleSheet(btn_style)

        grp2.addWidget(btn_copy)
        grp2.addWidget(btn_cut)
        grp2.addWidget(btn_paste)

        sep2 = QFrame()
        sep2.setFixedWidth(12)

        grp3 = QHBoxLayout()
        grp3.setSpacing(0)
        tools_config = [
            ("text", "Text"),
            ("static_text", "Static Text"),
            ("photo", "Photo"),
            ("static_graphic", "Static Graphic"),
            ("variable_graphic", "Variable Graphic"),
            ("date", "Date"),
            ("signature", "Signature")
        ]

        for icon_key, tooltip_name in tools_config:
            btn_tool = QToolButton()
            btn_tool.setFixedSize(42, 38)
            btn_tool.setIcon(make_toolbar_icon(icon_key, size=32))
            btn_tool.setIconSize(btn_tool.size())
            btn_tool.setToolTip(tooltip_name)
            btn_tool.setStyleSheet(btn_style)
            grp3.addWidget(btn_tool)

        sep3 = QFrame()
        sep3.setFixedWidth(12)

        grp4 = QHBoxLayout()
        grp4.setSpacing(0)
        new_tools_config = [
            ("barcode", "Barcode"),
            ("magnetic_stripe", "Magnetic Stripe"),
            ("chip", "Chip")  
        ]

        for icon_key, tooltip_name in new_tools_config:
            btn_tool = QToolButton()
            btn_tool.setFixedSize(42, 38)
            btn_tool.setIcon(make_toolbar_icon(icon_key, size=32))
            btn_tool.setIconSize(btn_tool.size())
            btn_tool.setToolTip(tooltip_name)
            btn_tool.setStyleSheet(btn_style)
            grp4.addWidget(btn_tool)

        sep4 = QFrame()
        sep4.setFixedWidth(12)

        grp5 = QHBoxLayout()
        grp5.setSpacing(0)
        drawing_tools = [
            ("line", "Line"),
            ("rectangle", "Rectangle"),
            ("ellipse", "Ellipse"),
            ("ruler", "Ruler"),
            ("grid_lines", "Grid Lines"),
            ("zoom_out", "Zoom Out"),
            ("zoom_in", "Zoom In")
        ]

        for icon_key, tooltip_name in drawing_tools:
            btn_tool = QToolButton()
            btn_tool.setFixedSize(42, 38)
            btn_tool.setIcon(make_toolbar_icon(icon_key, size=32))
            btn_tool.setIconSize(btn_tool.size())
            btn_tool.setToolTip(tooltip_name)
            btn_tool.setStyleSheet(btn_style)
            grp5.addWidget(btn_tool)

        tb_layout.addLayout(grp1)
        tb_layout.addWidget(sep1)
        tb_layout.addLayout(grp2)
        tb_layout.addWidget(sep2)
        tb_layout.addLayout(grp3)
        tb_layout.addWidget(sep3)
        tb_layout.addLayout(grp4)
        tb_layout.addWidget(sep4)
        tb_layout.addLayout(grp5)

        lbl_zoom = QLabel("Zoom ")
        lbl_zoom.setFont(QFont("Arial", 9.5))
        lbl_zoom.setStyleSheet("color: #333333; margin-left: 10px;")
        tb_layout.addWidget(lbl_zoom)

        zoom_combo = QComboBox()
        zoom_combo.addItems(["150%", "100%", "75%", "50%"])
        zoom_combo.setFixedSize(85, 38)
        zoom_combo.setStyleSheet("""
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #E0E0E0);
                border: 1px solid #B0B0B0;
                border-radius: 3px;
                padding-left: 8px;
                font-size: 9.5pt;
                font-family: Arial;
                color: #000000;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: none;
            }
        """)
        tb_layout.addWidget(zoom_combo)

        tb_layout.addSpacing(8)

        # Larger Orientation Button
        btn_orientation = QToolButton()
        btn_orientation.setFixedSize(42, 38)
        btn_orientation.setIcon(make_toolbar_icon("orientation", size=32))
        btn_orientation.setIconSize(btn_orientation.size())
        btn_orientation.setToolTip("Orientation")
        btn_orientation.setStyleSheet(btn_style)
        tb_layout.addWidget(btn_orientation)

        tb_layout.addStretch()
        main_layout.addWidget(editor_toolbar)

        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        canvas_container = QWidget()
        canvas_container.setStyleSheet("background-color: #B3B3B3;")
        canvas_layout = QHBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(30, 15, 30, 15)
        canvas_layout.setSpacing(30)

        front_box = QVBoxLayout()
        front_title = QLabel("Front Side                                Active Design Layer: Color")
        front_title.setFont(QFont("Arial", 9.5, QFont.Bold))
        front_title.setStyleSheet("color: #0F172A;")
        front_box.addWidget(front_title)

        front_card_bg = QFrame()
        front_card_bg.setFixedSize(300, 380)
        front_card_bg.setStyleSheet("background-color: #8C8C8C; border-radius: 2px;")
        fc_layout = QVBoxLayout(front_card_bg)
        fc_layout.setContentsMargins(20, 50, 20, 50)

        front_card = QFrame()
        front_card.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 12px;")
        fc_layout.addWidget(front_card)
        front_box.addWidget(front_card_bg)

        back_box = QVBoxLayout()
        back_title = QLabel("Back Side")
        back_title.setFont(QFont("Arial", 9.5, QFont.Bold))
        back_title.setStyleSheet("color: #0F172A;")
        back_box.addWidget(back_title)

        back_card_bg = QFrame()
        back_card_bg.setFixedSize(300, 380)
        back_card_bg.setStyleSheet("background-color: #8C8C8C; border-radius: 2px;")
        bc_layout = QVBoxLayout(back_card_bg)
        bc_layout.setContentsMargins(20, 50, 20, 50)

        back_card = QFrame()
        back_card.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 12px;")
        bc_layout.addWidget(back_card)
        back_box.addWidget(back_card_bg)

        canvas_layout.addLayout(front_box)
        canvas_layout.addLayout(back_box)
        canvas_layout.addStretch()

        content_layout.addWidget(canvas_container, stretch=1)

        sidebar = QFrame()
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet("background-color: #F8FAFC; border-left: 1px solid #CBD5E1;")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)

        sb_tabs = QFrame()
        sb_tabs.setFixedHeight(36)
        sb_tabs.setStyleSheet("background-color: #E2E8F0; border-bottom: 1px solid #CBD5E1;")
        sb_tabs_layout = QHBoxLayout(sb_tabs)
        sb_tabs_layout.setContentsMargins(0, 0, 0, 0)

        prop_tab = QPushButton("Properties")
        prop_tab.setFont(QFont("Arial", 9, QFont.Bold))
        prop_tab.setStyleSheet("background-color: #FFFFFF; border: none; border-top: 2px solid #7B0082;")
        layer_tab = QPushButton("Layers")
        layer_tab.setFont(QFont("Arial", 9))
        layer_tab.setStyleSheet("background-color: transparent; border: none; color: #475569;")

        sb_tabs_layout.addWidget(prop_tab)
        sb_tabs_layout.addWidget(layer_tab)
        sb_layout.addWidget(sb_tabs)

        sb_content = QWidget()
        sb_content_layout = QVBoxLayout(sb_content)
        sb_content_layout.setContentsMargins(12, 12, 12, 12)

        prop_header = QLabel("- Front Side Properties")
        prop_header.setFont(QFont("Arial", 9, QFont.Bold))
        prop_header.setStyleSheet("color: #1E293B; background-color: #E2E8F0; padding: 6px;")
        sb_content_layout.addWidget(prop_header)

        chk_rotate = QCheckBox("Rotate print orientation 180\ndegrees")
        chk_rotate.setFont(QFont("Arial", 8.5))
        chk_rotate.setStyleSheet("color: #475569; margin-top: 8px;")

        chk_tactile = QCheckBox("Tactile Impression Module")
        chk_tactile.setFont(QFont("Arial", 8.5))
        chk_tactile.setStyleSheet("color: #475569; margin-top: 8px;")

        sb_content_layout.addWidget(chk_rotate)
        sb_content_layout.addWidget(chk_tactile)
        sb_content_layout.addStretch()

        sb_layout.addWidget(sb_content)
        content_layout.addWidget(sidebar)

        main_layout.addWidget(content_area, stretch=1)

        # Bottom Bar Buttons enlarged to height 36px
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(54)
        bottom_bar.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #CBD5E1;")
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(16, 6, 16, 6)
        bb_layout.setSpacing(12)

        btn_save = QPushButton("Save")
        btn_save.setFixedSize(90, 36)
        btn_save.setFont(QFont("Arial", 9.5, QFont.Bold))
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet("QPushButton { background-color: #0284C7; color: #FFFFFF; border: none; border-radius: 4px; } QPushButton:hover { background-color: #0369A1; }")

        btn_save_as = QPushButton("Save As...")
        btn_save_as.setFixedSize(100, 36)
        btn_save_as.setFont(QFont("Arial", 9.5))
        btn_save_as.setCursor(Qt.PointingHandCursor)
        btn_save_as.setStyleSheet("QPushButton { background-color: #E2E8F0; color: #1E293B; border: 1px solid #CBD5E1; border-radius: 4px; } QPushButton:hover { background-color: #CBD5E1; }")

        btn_close = QPushButton("Close")
        btn_close.setFixedSize(90, 36)
        btn_close.setFont(QFont("Arial", 9.5))
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setStyleSheet("QPushButton { background-color: #E2E8F0; color: #1E293B; border: 1px solid #CBD5E1; border-radius: 4px; } QPushButton:hover { background-color: #CBD5E1; }")
        if on_close_callback:
            btn_close.clicked.connect(on_close_callback)

        bb_layout.addWidget(btn_save)
        bb_layout.addWidget(btn_save_as)
        bb_layout.addWidget(btn_close)
        bb_layout.addStretch()

        main_layout.addWidget(bottom_bar)


# -------------------------------------------------------------
# Generic Workspace Wrapper
# -------------------------------------------------------------
class GenericWorkspace(QWidget):
    def __init__(self, title_text="Workspace", show_create=False, default_grid_active=True, on_create_click=None):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = ViewToggleToolbar(
            on_grid_click=self.show_grid_view,
            on_list_click=self.show_list_view,
            is_grid_active=default_grid_active,
            show_create_btn=show_create,
            on_create_click=on_create_click
        )
        layout.addWidget(self.toolbar)

        self.view_stack = QStackedWidget()

        grid_widget = QWidget()
        grid_layout = QVBoxLayout(grid_widget)
        grid_label = QLabel(f"⬚ {title_text} - Grid View Content")
        grid_label.setFont(QFont("Arial", 11, QFont.Bold))
        grid_label.setStyleSheet("color: #4B5563; padding: 20px;")
        grid_layout.addWidget(grid_label)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_label = QLabel(f"☰ {title_text} - List View Content")
        list_label.setFont(QFont("Arial", 11, QFont.Bold))
        list_label.setStyleSheet("color: #1F2937; padding: 20px;")
        list_layout.addWidget(list_label)

        self.view_stack.addWidget(grid_widget)
        self.view_stack.addWidget(list_widget)

        self.view_stack.setCurrentIndex(0 if default_grid_active else 1)
        layout.addWidget(self.view_stack, stretch=1)

    def show_grid_view(self):
        self.view_stack.setCurrentIndex(0)
        self.toolbar.set_active_state(is_grid_active=True)

    def show_list_view(self):
        self.view_stack.setCurrentIndex(1)
        self.toolbar.set_active_state(is_grid_active=False)


# -------------------------------------------------------------
# Main Dashboard Class
# -------------------------------------------------------------
class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.current_title = "Credential Design 1"
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = QFrame()
        top_bar.setFixedHeight(56)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(14, 0, 18, 0)

        logo_hex = QLabel("⬡")
        logo_hex.setStyleSheet("color: #7B0082; font-size: 24px; font-weight: bold;")
        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Arial", 13, QFont.Bold))
        logo_text.setStyleSheet("color: #2D3748; padding-right: 12px; border-right: 1px solid #D1D5DB;")

        sub_text = QLabel("Adaptive Issuance™\nInstant ID")
        sub_text.setFont(QFont("Arial", 8, QFont.Bold))

        top_layout.addWidget(logo_hex)
        top_layout.addWidget(logo_text)
        top_layout.addWidget(sub_text)
        top_layout.addStretch()

        self.home_nav_btn = QPushButton("Home")
        self.design_nav_btn = QPushButton("Design")
        self.queue_nav_btn = QPushButton("Printer Queues")

        for btn in [self.home_nav_btn, self.design_nav_btn, self.queue_nav_btn]:
            btn.setFont(QFont("Arial", 9.5, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("QPushButton { border: none; color: #1A202C; background: transparent; padding: 6px 16px; }")

        self.home_nav_btn.clicked.connect(self.switch_to_home_section)
        self.design_nav_btn.clicked.connect(lambda: self.switch_to_design_section(0))

        top_layout.addWidget(self.home_nav_btn)
        top_layout.addWidget(self.design_nav_btn)
        top_layout.addWidget(self.queue_nav_btn)

        main_layout.addWidget(top_bar)

        self.purple_bar = QFrame()
        self.purple_bar.setFixedHeight(42)
        self.purple_bar.setStyleSheet("background-color: #7B0082;")
        self.purple_layout = QHBoxLayout(self.purple_bar)
        self.purple_layout.setContentsMargins(14, 0, 20, 0)
        self.purple_layout.setSpacing(0)

        main_layout.addWidget(self.purple_bar)

        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)

        self.section_stack = QStackedWidget()

        self.home_stack = QStackedWidget()
        self.home_credentials_page = GenericWorkspace("Home -> Credentials")
        self.home_reports_page = GenericWorkspace("Home -> Reports")
        self.home_stack.addWidget(self.home_credentials_page)
        self.home_stack.addWidget(self.home_reports_page)

        self.design_stack = QStackedWidget()
        self.design_cred_page = GenericWorkspace("Design -> Credential Designs", show_create=True, on_create_click=self.open_editor_view)
        self.design_workflow_page = GenericWorkspace("Design -> Workflows", show_create=True)
        self.design_reports_page = GenericWorkspace("Design -> Reports", show_create=True)
        self.design_fields_page = GenericWorkspace("Design -> Field Connections", show_create=True)
        
        self.editor_page = CredentialDesignEditorView(on_close_callback=self.close_editor_view)

        self.design_stack.addWidget(self.design_cred_page)
        self.design_stack.addWidget(self.design_workflow_page)
        self.design_stack.addWidget(self.design_reports_page)
        self.design_stack.addWidget(self.design_fields_page)
        self.design_stack.addWidget(self.editor_page)

        self.section_stack.addWidget(self.home_stack)
        self.section_stack.addWidget(self.design_stack)

        body_layout.addWidget(self.section_stack, stretch=1)
        main_layout.addWidget(body_container, stretch=1)

        self.switch_to_design_section(0)
        self.open_editor_view()

    def clear_purple_bar(self):
        while self.purple_layout.count() > 0:
            item = self.purple_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def open_editor_view(self):
        self.design_stack.setCurrentIndex(4)
        self.update_purple_bar_title()

    def update_purple_bar_title(self):
        self.clear_purple_bar()

        title_lbl = QLabel(self.current_title)
        title_lbl.setFont(QFont("Arial", 12, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; padding-left: 10px;")

        edit_icon_btn = HoverEditButton(self)
        edit_icon_btn.clicked.connect(self.show_edit_properties_dialog)

        self.purple_layout.addWidget(title_lbl)
        self.purple_layout.addSpacing(10)
        self.purple_layout.addWidget(edit_icon_btn)
        self.purple_layout.addStretch()

    def show_edit_properties_dialog(self):
        dialog = EditPropertiesDialog(current_name=self.current_title, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.current_title = dialog.get_updated_name()
            self.update_purple_bar_title()

    def close_editor_view(self):
        self.switch_to_design_section(0)

    def switch_to_home_section(self):
        self.section_stack.setCurrentIndex(0)
        self.clear_purple_bar()

        btn_credentials = QPushButton("Credentials")
        btn_reports = QPushButton("Reports")

        for btn in [btn_credentials, btn_reports]:
            btn.setFont(QFont("Arial", 9.5, QFont.Bold))
            btn.setFixedHeight(42)
            btn.setCursor(Qt.PointingHandCursor)

        btn_credentials.clicked.connect(lambda: self.set_sub_tab(self.home_stack, 0, [btn_credentials, btn_reports]))
        btn_reports.clicked.connect(lambda: self.set_sub_tab(self.home_stack, 1, [btn_credentials, btn_reports]))

        self.purple_layout.addStretch()
        self.purple_layout.addWidget(btn_credentials)
        self.purple_layout.addWidget(btn_reports)

        self.set_sub_tab(self.home_stack, 0, [btn_credentials, btn_reports])

    def switch_to_design_section(self, target_tab_index=0):
        self.section_stack.setCurrentIndex(1)
        self.clear_purple_bar()

        btn_cred_designs = QPushButton("Credential Designs")
        btn_workflows = QPushButton("Workflows")
        btn_reports = QPushButton("Reports")
        btn_fields = QPushButton("Field Connections")

        tab_buttons = [btn_cred_designs, btn_workflows, btn_reports, btn_fields]

        self.purple_layout.addStretch()

        for idx, btn in enumerate(tab_buttons):
            btn.setFont(QFont("Arial", 9.5, QFont.Bold))
            btn.setFixedHeight(42)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self.set_sub_tab(self.design_stack, i, tab_buttons))
            self.purple_layout.addWidget(btn)

        self.set_sub_tab(self.design_stack, target_tab_index, tab_buttons)

    def set_sub_tab(self, stack_widget, index, button_list):
        stack_widget.setCurrentIndex(index)
        for i, btn in enumerate(button_list):
            if i == index:
                btn.setStyleSheet("background-color: #FFFFFF; color: #7B0082; border: none; padding: 0 20px; border-top-left-radius: 4px; border-top-right-radius: 4px;")
            else:
                btn.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0 20px;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1280, 750)
        self.setCentralWidget(EntrustDashboard())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
