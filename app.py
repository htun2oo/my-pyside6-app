import sys
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QPen, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QComboBox, QCheckBox,
    QToolButton, QDialog, QLineEdit, QTextEdit
)

# -------------------------------------------------------------
# Toolbar Vector Icon Painter (All Custom Tool Icons)
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
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(4, 7), QPointF(9, 3), QPointF(9, 10)])

    elif icon_type == "redo":
        path = QPainterPath()
        path.arcMoveTo(4, 4, 16, 16, 135)
        path.arcTo(4, 4, 16, 16, 135, -200)
        p.drawPath(path)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(20, 7), QPointF(15, 3), QPointF(15, 10)])

    elif icon_type == "copy":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawRoundedRect(QRectF(5, 4, 10, 12), 1, 1)
        p.setBrush(QColor("#F0F4F8"))
        p.drawRoundedRect(QRectF(9, 8, 10, 12), 1, 1)

    elif icon_type == "cut":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawEllipse(4, 15, 5, 5)
        p.drawEllipse(15, 15, 5, 5)
        p.drawLine(6.5, 15.5, 16, 4)
        p.drawLine(17.5, 15.5, 8, 4)

    elif icon_type == "paste":
        p.setPen(QPen(QColor(color), 1.8))
        p.setBrush(QColor(color))
        p.drawRoundedRect(QRectF(6, 4, 12, 16), 1, 1)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(QRectF(9, 7, 11, 14), 1, 1)
        p.drawRect(QRectF(9, 2, 6, 3))

    elif icon_type == "text":
        p.setFont(QFont("Times New Roman", 13, QFont.Bold))
        p.setPen(QPen(QColor(color)))
        p.drawText(QRectF(1, 1, 14, 16), Qt.AlignLeft | Qt.AlignTop, "T")
        p.setPen(QPen(QColor(color), 1.5))
        p.drawRect(QRectF(11, 11, 11, 11))
        p.drawLine(16, 13, 16, 20)
        p.drawLine(14, 13, 18, 13)

    elif icon_type == "static_text":
        p.setFont(QFont("Times New Roman", 16, QFont.Bold))
        p.setPen(QPen(QColor(color)))
        p.drawText(QRectF(0, 0, 24, 24), Qt.AlignCenter, "T")

    elif icon_type == "photo":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawRect(QRectF(3, 4, 18, 16))
        p.setBrush(QColor(color))
        p.drawEllipse(10, 7, 4, 4)
        path = QPainterPath()
        path.moveTo(7, 18)
        path.arcTo(7, 12, 10, 8, 0, 180)
        p.drawPath(path)

    elif icon_type == "static_graphic":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawRect(QRectF(3, 4, 18, 16))
        p.setBrush(QColor(color))
        poly = [QPointF(5, 18), QPointF(10, 11), QPointF(14, 15), QPointF(17, 11), QPointF(21, 18)]
        p.drawPolygon(poly)

    elif icon_type == "variable_graphic":
        p.setPen(QPen(QColor(color), 1.6))
        p.drawRect(QRectF(2, 2, 14, 13))
        p.drawRect(QRectF(5, 5, 14, 13))
        p.setPen(QPen(QColor(color), 1.8))
        p.drawArc(15, 15, 8, 8, 0, 270 * 16)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(20, 14), QPointF(23, 17), QPointF(17, 17)])

    elif icon_type == "date":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawRect(QRectF(4, 4, 16, 16))
        p.setBrush(QColor(color))
        for r in range(3):
            for c in range(3):
                p.drawRect(QRectF(7 + c*4, 7 + r*4, 2, 2))

    elif icon_type == "signature":
        p.setPen(QPen(QColor(color), 1.8))
        p.drawRect(QRectF(4, 5, 17, 15))
        p.setPen(QPen(QColor(color), 2))
        p.drawLine(3, 20, 6, 4)
        path = QPainterPath()
        path.moveTo(6, 14)
        path.cubicTo(10, 8, 12, 18, 16, 12)
        path.cubicTo(18, 10, 19, 14, 21, 14)
        p.drawPath(path)

    # ------------------ New Icons ------------------
    elif icon_type == "barcode":
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(color))
        # Draw barcode vertical bars with varying thicknesses
        bars = [(3, 2), (6, 1), (8, 2), (11, 3), (15, 1), (17, 2), (20, 1)]
        for x, w in bars:
            p.drawRect(QRectF(x, 4, w, 16))

    elif icon_type == "magnetic_stripe":
        p.setPen(QPen(QColor(color), 1.8))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(3, 4, 18, 16), 2, 2)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(color))
        p.drawRect(QRectF(3, 7, 18, 4))  # Black mag-stripe band

    elif icon_type == "chip":
        p.setPen(QPen(QColor(color), 1.8))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(4, 4, 16, 16), 3, 3)
        # Inner chip pattern lines
        p.drawLine(4, 9, 8, 9)
        p.drawLine(4, 15, 8, 15)
        p.drawLine(16, 9, 20, 9)
        p.drawLine(16, 15, 20, 15)
        p.drawLine(9, 4, 9, 8)
        p.drawLine(15, 4, 15, 8)
        p.drawLine(9, 16, 9, 20)
        p.drawLine(15, 16, 15, 20)
        p.drawRect(QRectF(9, 9, 6, 6))

    p.end()
    return QIcon(pixmap)


# -------------------------------------------------------------
# Hover Edit Button Class
# -------------------------------------------------------------
class HoverEditButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("✏", parent)
        self.setFixedSize(24, 24)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Edit Properties")
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #1E293B;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
            QToolTip {
                background-color: #1E293B;
                color: #FFFFFF;
                border: none;
                padding: 4px 8px;
                font-size: 8pt;
                font-family: Arial;
                border-radius: 3px;
            }
        """)


# -------------------------------------------------------------
# Grid & List Icons Helpers
# -------------------------------------------------------------
def draw_grid_icon(size=14, color="#003366"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, False)
    p.setBrush(QBrush(QColor(color)))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 0, 6, 6)
    p.drawRect(8, 0, 6, 6)
    p.drawRect(0, 8, 6, 6)
    p.drawRect(8, 8, 6, 6)
    p.end()
    return QIcon(pixmap)

def draw_list_icon(size=14, color="#003366"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing, False)
    p.setBrush(QBrush(QColor(color)))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 1, 14, 3)
    p.drawRect(0, 6, 14, 3)
    p.drawRect(0, 11, 14, 3)
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
        self.setFixedSize(410, 560)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; border: 1px solid #000000; }")

        self.dim_data = {
            "ISO ID-1": {"Centimeters": (8.5725, 5.3975), "Millimeters": (85.725, 53.975)},
            "CR-50": {"Centimeters": (8.8900, 4.4450), "Millimeters": (88.900, 44.450)},
            "Custom": {"Centimeters": (8.5725, 5.3975), "Millimeters": (85.725, 53.975)}
        }

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header Bar
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
        close_btn.setStyleSheet("""
            QPushButton { background: #6B0072; color: #FFFFFF; border: none; border-radius: 10px; font-weight: bold; font-size: 10px; }
            QPushButton:hover { background: #92009C; }
        """)
        close_btn.clicked.connect(self.reject)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        layout.addWidget(header)

        # Form Content Area
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(16, 12, 16, 12)
        form_layout.setSpacing(6)

        label_style = "color: #334155; font-size: 8.5pt; font-family: Arial; font-weight: bold;"
        
        input_style = """
            QLineEdit, QComboBox {
                border: 1px solid #94A3B8;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 8.5pt;
                font-family: Arial;
                background-color: #FFFFFF;
                color: #0F172A;
            }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #0284C7; }
            QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 20px; border-left: 1px solid #94A3B8; }
            QComboBox QAbstractItemView { border: 1px solid #94A3B8; background-color: #FFFFFF; color: #0F172A; selection-background-color: #0284C7; selection-color: #FFFFFF; padding: 4px; }
        """

        lbl_name = QLabel("Name")
        lbl_name.setStyleSheet(label_style)
        self.txt_name = QLineEdit(current_name)
        self.txt_name.setFixedSize(230, 26)
        self.txt_name.setStyleSheet(input_style)

        lbl_dim = QLabel("Dimensions")
        lbl_dim.setStyleSheet(label_style)
        self.cbo_dim = QComboBox()
        self.cbo_dim.addItems(["ISO ID-1", "CR-50", "Custom"])
        self.cbo_dim.setFixedSize(140, 26)
        self.cbo_dim.setStyleSheet(input_style)

        lbl_units = QLabel("Units")
        lbl_units.setStyleSheet(label_style)
        self.cbo_units = QComboBox()
        self.cbo_units.addItems(["Centimeters", "Millimeters"])
        self.cbo_units.setFixedSize(140, 26)
        self.cbo_units.setStyleSheet(input_style)

        lbl_width = QLabel("Width")
        lbl_width.setStyleSheet(label_style)
        width_box = QHBoxLayout()
        width_box.setSpacing(8)
        self.txt_width = QLineEdit("8.5725")
        self.txt_width.setFixedSize(110, 26)
        self.txt_width.setStyleSheet(input_style)
        self.unit_w_lbl = QLabel("centimeters")
        self.unit_w_lbl.setStyleSheet("color: #0F172A; font-size: 8.5pt; font-family: Arial;")
        width_box.addWidget(self.txt_width)
        width_box.addWidget(self.unit_w_lbl)
        width_box.addStretch()

        lbl_height = QLabel("Height")
        lbl_height.setStyleSheet(label_style)
        height_box = QHBoxLayout()
        height_box.setSpacing(8)
        self.txt_height = QLineEdit("5.3975")
        self.txt_height.setFixedSize(110, 26)
        self.txt_height.setStyleSheet(input_style)
        self.unit_h_lbl = QLabel("centimeters")
        self.unit_h_lbl.setStyleSheet("color: #0F172A; font-size: 8.5pt; font-family: Arial;")
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
                QCheckBox { font-size: 8.5pt; font-family: Arial; color: #334155; }
                QCheckBox::indicator { width: 12px; height: 12px; border: 1px solid #0284C7; border-radius: 2px; background-color: #FFFFFF; }
                QCheckBox::indicator:checked { background-color: #0284C7; }
            """)
            help_btn = QLabel("?")
            help_btn.setFixedSize(16, 16)
            help_btn.setAlignment(Qt.AlignCenter)
            help_btn.setStyleSheet("background-color: #38BDF8; color: #FFFFFF; font-weight: bold; font-size: 8pt; border-radius: 8px;")
            row.addWidget(chk)
            row.addWidget(help_btn)
            row.addStretch()
            return row

        row_rewritable = make_checkbox_row("Rewritable credential")
        row_print_edge = make_checkbox_row("Print over the edge")

        lbl_desc = QLabel("Description")
        lbl_desc.setStyleSheet(label_style)
        self.txt_desc = QTextEdit()
        self.txt_desc.setFixedHeight(80)
        self.txt_desc.setStyleSheet("QTextEdit { border: 1px solid #94A3B8; border-radius: 3px; background-color: #FFFFFF; }")

        form_layout.addWidget(lbl_name)
        form_layout.addWidget(self.txt_name)
        form_layout.addSpacing(2)
        form_layout.addWidget(lbl_dim)
        form_layout.addWidget(self.cbo_dim)
        form_layout.addSpacing(2)
        form_layout.addWidget(lbl_units)
        form_layout.addWidget(self.cbo_units)
        form_layout.addSpacing(2)
        form_layout.addWidget(lbl_width)
        form_layout.addLayout(width_box)
        form_layout.addSpacing(2)
        form_layout.addWidget(lbl_height)
        form_layout.addLayout(height_box)
        form_layout.addSpacing(4)
        form_layout.addLayout(row_rewritable)
        form_layout.addLayout(row_print_edge)
        form_layout.addSpacing(4)
        form_layout.addWidget(lbl_desc)
        form_layout.addWidget(self.txt_desc)

        layout.addWidget(form_widget, stretch=1)

        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(44)
        bottom_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(16, 0, 16, 0)
        bb_layout.setSpacing(10)

        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(72, 28)
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.setStyleSheet("QPushButton { background-color: #0284C7; color: #FFFFFF; font-weight: bold; border: none; border-radius: 3px; } QPushButton:hover { background-color: #0369A1; }")
        btn_ok.clicked.connect(self.accept)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(72, 28)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("QPushButton { background-color: #E2E8F0; color: #1E293B; border: 1px solid #CBD5E1; border-radius: 3px; } QPushButton:hover { background-color: #CBD5E1; }")
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
        self.setFixedHeight(34)
        self.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB; }")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(0)
        layout.addStretch()

        self.grid_btn = QPushButton()
        self.grid_btn.setFixedSize(32, 26)
        self.grid_btn.setCursor(Qt.PointingHandCursor)

        self.list_btn = QPushButton()
        self.list_btn.setFixedSize(32, 26)
        self.list_btn.setCursor(Qt.PointingHandCursor)

        self.grid_btn.setIcon(draw_grid_icon(14, "#003366"))
        self.list_btn.setIcon(draw_list_icon(14, "#003366"))

        self.set_active_state(is_grid_active)

        if on_grid_click:
            self.grid_btn.clicked.connect(on_grid_click)
        if on_list_click:
            self.list_btn.clicked.connect(on_list_click)

        layout.addWidget(self.grid_btn)
        layout.addWidget(self.list_btn)

        if show_create_btn:
            layout.addSpacing(6)
            self.create_btn = QPushButton("+ Create")
            self.create_btn.setFixedHeight(26)
            self.create_btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            self.create_btn.setCursor(Qt.PointingHandCursor)
            self.create_btn.setStyleSheet("QPushButton { background-color: #E5E7EB; color: #1F2937; border: 1px solid #9CA3AF; border-radius: 3px; padding: 0 8px; } QPushButton:hover { background-color: #D1D5DB; }")
            if on_create_click:
                self.create_btn.clicked.connect(on_create_click)
            layout.addWidget(self.create_btn)

    def set_active_state(self, is_grid_active):
        if is_grid_active:
            self.grid_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #AFAFAF, stop:1 #C4C4C4); border: 1px solid #888888; border-top-left-radius: 4px; border-bottom-left-radius: 4px; }")
            self.list_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F0F0F0, stop:1 #D9D9D9); border: 1px solid #B0B0B0; border-left: none; border-top-right-radius: 6px; border-bottom-right-radius: 6px; } QPushButton:hover { background: #E0E0E0; }")
        else:
            self.grid_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F0F0F0, stop:1 #D9D9D9); border: 1px solid #B0B0B0; border-top-left-radius: 4px; border-bottom-left-radius: 4px; } QPushButton:hover { background: #E0E0E0; }")
            self.list_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #AFAFAF, stop:1 #C4C4C4); border: 1px solid #888888; border-left: none; border-top-right-radius: 6px; border-bottom-right-radius: 6px; }")


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

        # Top Editing Toolbar
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
            QToolTip {
                background-color: #1E293B;
                color: #FFFFFF;
                border: none;
                padding: 4px 8px;
                font-size: 8pt;
                font-family: Arial;
                border-radius: 3px;
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

        sep2 = QFrame()
        sep2.setFixedWidth(8)

        # Group 3: Text, Static Text, Photo, Static Graphic, Variable Graphic, Date, Signature
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
            btn_tool.setFixedSize(28, 26)
            btn_tool.setIcon(make_toolbar_icon(icon_key))
            btn_tool.setToolTip(tooltip_name)
            btn_tool.setStyleSheet(btn_style)
            grp3.addWidget(btn_tool)

        sep3 = QFrame()
        sep3.setFixedWidth(8)

        # Group 4: Barcode, Magnetic Stripe, Smart Card Chip (Newly Added Group)
        grp4 = QHBoxLayout()
        grp4.setSpacing(0)

        new_tools_config = [
            ("barcode", "Barcode"),
            ("magnetic_stripe", "Magnetic Stripe"),
            ("chip", "Smart Card Chip")
        ]

        for icon_key, tooltip_name in new_tools_config:
            btn_tool = QToolButton()
            btn_tool.setFixedSize(28, 26)
            btn_tool.setIcon(make_toolbar_icon(icon_key))
            btn_tool.setToolTip(tooltip_name)
            btn_tool.setStyleSheet(btn_style)
            grp4.addWidget(btn_tool)

        tb_layout.addLayout(grp1)
        tb_layout.addWidget(sep1)
        tb_layout.addLayout(grp2)
        tb_layout.addWidget(sep2)
        tb_layout.addLayout(grp3)
        tb_layout.addWidget(sep3)
        tb_layout.addLayout(grp4)

        sep4 = QFrame()
        sep4.setFixedWidth(8)
        tb_layout.addWidget(sep4)

        other_tools = ["🗑", "▦", "▤", "║", "▭", "╱", "◯"]
        for tool in other_tools:
            btn = QToolButton()
            btn.setText(tool)
            btn.setFixedSize(26, 26)
            btn.setStyleSheet("QToolButton { background-color: #FFFFFF; border: 1px solid #CBD5E1; margin: 1px; } QToolButton:hover { background-color: #E2E8F0; }")
            tb_layout.addWidget(btn)

        zoom_combo = QComboBox()
        zoom_combo.addItems(["100%", "75%", "50%", "150%"])
        zoom_combo.setFixedSize(70, 26)
        zoom_combo.setStyleSheet("background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 3px;")
        tb_layout.addWidget(zoom_combo)

        tb_layout.addStretch()
        main_layout.addWidget(editor_toolbar)

        # Canvas Area
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
        front_title.setFont(QFont("Arial", 9, QFont.Bold))
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
        back_title.setFont(QFont("Arial", 9, QFont.Bold))
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

        # Right Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #F8FAFC; border-left: 1px solid #CBD5E1;")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)

        sb_tabs = QFrame()
        sb_tabs.setFixedHeight(30)
        sb_tabs.setStyleSheet("background-color: #E2E8F0; border-bottom: 1px solid #CBD5E1;")
        sb_tabs_layout = QHBoxLayout(sb_tabs)
        sb_tabs_layout.setContentsMargins(0, 0, 0, 0)

        prop_tab = QPushButton("Properties")
        prop_tab.setFont(QFont("Arial", 8, QFont.Bold))
        prop_tab.setStyleSheet("background-color: #FFFFFF; border: none; border-top: 2px solid #7B0082;")
        layer_tab = QPushButton("Layers")
        layer_tab.setFont(QFont("Arial", 8))
        layer_tab.setStyleSheet("background-color: transparent; border: none; color: #475569;")

        sb_tabs_layout.addWidget(prop_tab)
        sb_tabs_layout.addWidget(layer_tab)
        sb_layout.addWidget(sb_tabs)

        sb_content = QWidget()
        sb_content_layout = QVBoxLayout(sb_content)
        sb_content_layout.setContentsMargins(10, 10, 10, 10)

        prop_header = QLabel("- Front Side Properties")
        prop_header.setFont(QFont("Arial", 8.5, QFont.Bold))
        prop_header.setStyleSheet("color: #1E293B; background-color: #E2E8F0; padding: 4px;")
        sb_content_layout.addWidget(prop_header)

        chk_rotate = QCheckBox("Rotate print orientation 180\ndegrees")
        chk_rotate.setFont(QFont("Arial", 8))
        chk_rotate.setStyleSheet("color: #475569; margin-top: 6px;")

        chk_tactile = QCheckBox("Tactile Impression Module")
        chk_tactile.setFont(QFont("Arial", 8))
        chk_tactile.setStyleSheet("color: #475569; margin-top: 6px;")

        sb_content_layout.addWidget(chk_rotate)
        sb_content_layout.addWidget(chk_tactile)
        sb_content_layout.addStretch()

        sb_layout.addWidget(sb_content)
        content_layout.addWidget(sidebar)

        main_layout.addWidget(content_area, stretch=1)

        # Bottom Action Bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(40)
        bottom_bar.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #CBD5E1;")
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(10, 5, 10, 5)
        bb_layout.setSpacing(8)

        btn_save = QPushButton("Save")
        btn_save.setFixedSize(70, 28)
        btn_save.setStyleSheet("background-color: #0284C7; color: #FFFFFF; font-weight: bold; border: none; border-radius: 3px;")

        btn_save_as = QPushButton("Save As...")
        btn_save_as.setFixedSize(80, 28)
        btn_save_as.setStyleSheet("background-color: #E2E8F0; color: #1E293B; border: 1px solid #CBD5E1; border-radius: 3px;")

        btn_close = QPushButton("Close")
        btn_close.setFixedSize(70, 28)
        btn_close.setStyleSheet("background-color: #E2E8F0; color: #1E293B; border: 1px solid #CBD5E1; border-radius: 3px;")
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

        # 1. Top Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(48)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #D1D5DB;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 15, 0)

        logo_hex = QLabel("⬡")
        logo_hex.setStyleSheet("color: #7B0082; font-size: 19px; font-weight: bold;")
        logo_text = QLabel("ENTRUST")
        logo_text.setFont(QFont("Arial", 11, QFont.Bold))
        logo_text.setStyleSheet("color: #2D3748; padding-right: 8px; border-right: 1px solid #D1D5DB;")

        sub_text = QLabel("Adaptive Issuance™\nInstant ID")
        sub_text.setFont(QFont("Arial", 7, QFont.Bold))

        top_layout.addWidget(logo_hex)
        top_layout.addWidget(logo_text)
        top_layout.addWidget(sub_text)
        top_layout.addStretch()

        self.home_nav_btn = QPushButton("Home")
        self.design_nav_btn = QPushButton("Design")
        self.queue_nav_btn = QPushButton("Printer Queues")

        for btn in [self.home_nav_btn, self.design_nav_btn, self.queue_nav_btn]:
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("QPushButton { border: none; color: #1A202C; background: transparent; padding: 2px 12px; }")

        self.home_nav_btn.clicked.connect(self.switch_to_home_section)
        self.design_nav_btn.clicked.connect(lambda: self.switch_to_design_section(0))

        top_layout.addWidget(self.home_nav_btn)
        top_layout.addWidget(self.design_nav_btn)
        top_layout.addWidget(self.queue_nav_btn)

        main_layout.addWidget(top_bar)

        # 2. Purple Secondary Navigation Bar
        self.purple_bar = QFrame()
        self.purple_bar.setFixedHeight(34)
        self.purple_bar.setStyleSheet("background-color: #7B0082;")
        self.purple_layout = QHBoxLayout(self.purple_bar)
        self.purple_layout.setContentsMargins(10, 0, 20, 0)
        self.purple_layout.setSpacing(0)

        main_layout.addWidget(self.purple_bar)

        # 3. Middle Body Content
        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)

        self.section_stack = QStackedWidget()

        # Home Stack
        self.home_stack = QStackedWidget()
        self.home_credentials_page = GenericWorkspace("Home -> Credentials")
        self.home_reports_page = GenericWorkspace("Home -> Reports")
        self.home_stack.addWidget(self.home_credentials_page)
        self.home_stack.addWidget(self.home_reports_page)

        # Design Stack
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

    def close_editor_view(self):
        self.switch_to_design_section(0)

    def switch_to_home_section(self):
        self.section_stack.setCurrentIndex(0)
        self.clear_purple_bar()

        btn_credentials = QPushButton("Credentials")
        btn_reports = QPushButton("Reports")

        for btn in [btn_credentials, btn_reports]:
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setFixedHeight(34)
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
            btn.setFont(QFont("Arial", 8.5, QFont.Bold))
            btn.setFixedHeight(34)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self.set_sub_tab(self.design_stack, i, tab_buttons))
            self.purple_layout.addWidget(btn)

        self.set_sub_tab(self.design_stack, target_tab_index, tab_buttons)

    def set_sub_tab(self, stack_widget, index, button_list):
        stack_widget.setCurrentIndex(index)
        for i, btn in enumerate(button_list):
            if i == index:
                btn.setStyleSheet("background-color: #FFFFFF; color: #7B0082; border: none; padding: 0 16px; border-top-left-radius: 4px; border-top-right-radius: 4px;")
            else:
                btn.setStyleSheet("background-color: transparent; color: #FFFFFF; border: none; padding: 0 16px;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1120, 640)
        self.setCentralWidget(EntrustDashboard())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
