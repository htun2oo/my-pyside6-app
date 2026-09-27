import sys
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QPen, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QComboBox, QCheckBox,
    QToolButton, QDialog, QLineEdit, QTextEdit, QScrollArea, QTabWidget
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
        path.arcMoveTo(6, 6, 20, 20, 0)
        path.arcTo(6, 6, 20, 20, 0, 200)
        p.drawPath(path)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(4, 18), QPointF(14, 12), QPointF(12, 22)])

    elif icon_type == "redo":
        path = QPainterPath()
        path.arcMoveTo(6, 6, 20, 20, 180)
        path.arcTo(6, 6, 20, 20, 180, -200)
        p.drawPath(path)
        p.setBrush(QColor(color))
        p.drawPolygon([QPointF(28, 18), QPointF(18, 12), QPointF(20, 22)])

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
        """)


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
        close_btn.setStyleSheet("QPushButton { background: #6B0072; color: #FFFFFF; border: none; border-radius: 14px; font-weight: bold; font-size: 12px; } QPushButton:hover { background: #92009C; }")
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
        form_layout.addWidget(lbl_desc)
        form_layout.addWidget(self.txt_desc)

        layout.addWidget(form_widget, stretch=1)

        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(56)
        bottom_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(20, 0, 20, 0)
        bb_layout.setSpacing(14)

        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(90, 36)
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.setStyleSheet("QPushButton { background-color: #0284C7; color: #FFFFFF; font-weight: bold; font-size: 9.5pt; border: none; border-radius: 4px; }")
        btn_ok.clicked.connect(self.accept)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(90, 36)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("QPushButton { background-color: #E2E8F0; color: #1E293B; font-size: 9.5pt; border: 1px solid #CBD5E1; border-radius: 4px; }")
        btn_cancel.clicked.connect(self.reject)

        bb_layout.addWidget(btn_ok)
        bb_layout.addWidget(btn_cancel)
        bb_layout.addStretch()

        layout.addWidget(bottom_bar)

    def get_updated_name(self):
        return self.txt_name.text()


# -------------------------------------------------------------
# Credential Design Editor View (Exact Second Image Match)
# -------------------------------------------------------------
class CredentialDesignEditorView(QWidget):
    def __init__(self, on_close_callback=None):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- TOP TOOLBAR ----------------
        editor_toolbar = QFrame()
        editor_toolbar.setFixedHeight(52)
        editor_toolbar.setStyleSheet("background-color: #D6D6D6; border-bottom: 1px solid #B0B0B0;")
        tb_layout = QHBoxLayout(editor_toolbar)
        tb_layout.setContentsMargins(8, 5, 8, 5)
        tb_layout.setSpacing(0)

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
        """

        grp1 = QHBoxLayout()
        grp1.setSpacing(0)
        btn_undo = QToolButton()
        btn_undo.setFixedSize(42, 38)
        btn_undo.setIcon(make_toolbar_icon("undo", size=32))
        btn_undo.setIconSize(btn_undo.size())
        btn_undo.setStyleSheet(btn_style)

        btn_redo = QToolButton()
        btn_redo.setFixedSize(42, 38)
        btn_redo.setIcon(make_toolbar_icon("redo", size=32))
        btn_redo.setIconSize(btn_redo.size())
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
        btn_copy.setStyleSheet(btn_style)

        btn_cut = QToolButton()
        btn_cut.setFixedSize(42, 38)
        btn_cut.setIcon(make_toolbar_icon("cut", size=32))
        btn_cut.setIconSize(btn_cut.size())
        btn_cut.setStyleSheet(btn_style)

        btn_paste = QToolButton()
        btn_paste.setFixedSize(42, 38)
        btn_paste.setIcon(make_toolbar_icon("paste", size=32))
        btn_paste.setIconSize(btn_paste.size())
        btn_paste.setStyleSheet(btn_style)

        grp2.addWidget(btn_copy)
        grp2.addWidget(btn_cut)
        grp2.addWidget(btn_paste)

        sep2 = QFrame()
        sep2.setFixedWidth(12)

        grp3 = QHBoxLayout()
        grp3.setSpacing(0)
        tools_config = ["text", "static_text", "photo", "static_graphic", "variable_graphic", "date", "signature"]
        for icon_key in tools_config:
            btn_tool = QToolButton()
            btn_tool.setFixedSize(42, 38)
            btn_tool.setIcon(make_toolbar_icon(icon_key, size=32))
            btn_tool.setIconSize(btn_tool.size())
            btn_tool.setStyleSheet(btn_style)
            grp3.addWidget(btn_tool)

        sep3 = QFrame()
        sep3.setFixedWidth(12)

        grp4 = QHBoxLayout()
        grp4.setSpacing(0)
        new_tools_config = ["barcode", "magnetic_stripe", "chip"]
        for icon_key in new_tools_config:
            btn_tool = QToolButton()
            btn_tool.setFixedSize(42, 38)
            btn_tool.setIcon(make_toolbar_icon(icon_key, size=32))
            btn_tool.setIconSize(btn_tool.size())
            btn_tool.setStyleSheet(btn_style)
            grp4.addWidget(btn_tool)

        sep4 = QFrame()
        sep4.setFixedWidth(12)

        grp5 = QHBoxLayout()
        grp5.setSpacing(0)
        drawing_tools = ["line", "rectangle", "ellipse", "ruler", "grid_lines", "zoom_out", "zoom_in"]
        for icon_key in drawing_tools:
            btn_tool = QToolButton()
            btn_tool.setFixedSize(42, 38)
            btn_tool.setIcon(make_toolbar_icon(icon_key, size=32))
            btn_tool.setIconSize(btn_tool.size())
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
        zoom_combo.addItems(["100%", "150%", "75%", "50%"])
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
        """)
        tb_layout.addWidget(zoom_combo)

        tb_layout.addSpacing(8)

        btn_orientation = QToolButton()
        btn_orientation.setFixedSize(42, 38)
        btn_orientation.setIcon(make_toolbar_icon("orientation", size=32))
        btn_orientation.setIconSize(btn_orientation.size())
        btn_orientation.setStyleSheet(btn_style)
        tb_layout.addWidget(btn_orientation)

        tb_layout.addStretch()
        main_layout.addWidget(editor_toolbar)

        # ---------------- CONTENT AREA ----------------
        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Main Scroll Workspace
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #FFFFFF; }")

        canvas_container = QWidget()
        canvas_container.setStyleSheet("background-color: #FFFFFF;")
        canvas_layout = QHBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(15, 12, 15, 0)
        canvas_layout.setSpacing(30)
        canvas_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # --- FRONT SIDE CARD AREA ---
        front_container = QVBoxLayout()
        front_container.setSpacing(6)
        front_container.setContentsMargins(0, 0, 0, 0)

        front_header_row = QHBoxLayout()
        front_header_row.setContentsMargins(0, 0, 0, 0)

        front_title = QLabel("Front Side")
        front_title.setFont(QFont("Arial", 10, QFont.Bold))
        front_title.setStyleSheet("color: #000000;")

        self.active_layer_lbl = QLabel("Active Design Layer: Color")
        self.active_layer_lbl.setFont(QFont("Arial", 10, QFont.Bold))
        self.active_layer_lbl.setStyleSheet("color: #000000;")

        front_header_row.addWidget(front_title)
        front_header_row.addStretch()
        front_header_row.addWidget(self.active_layer_lbl)

        # ဒုတိယပုံအတိုင်း အောက်ခြေအထိ ထိကပ်သော မီးခိုးရောင် Canvas (Screenshot 2026-09-27 104356.png)
        front_card_bg = QFrame()
        front_card_bg.setFixedSize(360, 520)
        front_card_bg.setStyleSheet("background-color: #8C8C8C; border: none;")
        
        fc_layout = QVBoxLayout(front_card_bg)
        fc_layout.setContentsMargins(0, 70, 0, 0)
        fc_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        front_card = QFrame()
        front_card.setFixedSize(305, 195)
        front_card.setStyleSheet("background-color: #FFFFFF; border: 3.5px solid #000000; border-radius: 18px;")
        fc_layout.addWidget(front_card)

        front_container.addLayout(front_header_row)
        front_container.addWidget(front_card_bg)

        # --- BACK SIDE CARD AREA ---
        back_container = QVBoxLayout()
        back_container.setSpacing(6)
        back_container.setContentsMargins(0, 0, 0, 0)

        back_header_row = QHBoxLayout()
        back_header_row.setContentsMargins(0, 0, 0, 0)

        back_title = QLabel("Back Side")
        back_title.setFont(QFont("Arial", 10, QFont.Bold))
        back_title.setStyleSheet("color: #000000;")

        back_header_row.addWidget(back_title)
        back_header_row.addStretch()

        # ဒုတိယပုံအတိုင်း အောက်ခြေအထိ ထိကပ်သော မီးခိုးရောင် Canvas (Screenshot 2026-09-27 104356.png)
        back_card_bg = QFrame()
        back_card_bg.setFixedSize(360, 520)
        back_card_bg.setStyleSheet("background-color: #8C8C8C; border: none;")

        bc_layout = QVBoxLayout(back_card_bg)
        bc_layout.setContentsMargins(0, 70, 0, 0)
        bc_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        back_card = QFrame()
        back_card.setFixedSize(305, 195)
        back_card.setStyleSheet("background-color: #FFFFFF; border: 3.5px solid #000000; border-radius: 18px;")
        bc_layout.addWidget(back_card)

        back_container.addLayout(back_header_row)
        back_container.addWidget(back_card_bg)

        canvas_layout.addLayout(front_container)
        canvas_layout.addLayout(back_container)

        scroll_area.setWidget(canvas_container)
        content_layout.addWidget(scroll_area, stretch=1)

        # ---------------- RIGHT SIDEBAR PANEL ----------------
        sidebar = QFrame()
        sidebar.setFixedWidth(270)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #CCCCCC;")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)

        right_tabs = QTabWidget()
        
        properties_tab = QWidget()
        properties_tab.setStyleSheet("background-color: #FFFFFF;")
        prop_tab_layout = QVBoxLayout(properties_tab)
        prop_tab_layout.setContentsMargins(12, 12, 12, 12)
        prop_tab_layout.setAlignment(Qt.AlignTop)

        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                border-radius: 4px;
            }
        """)
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(0, 0, 0, 12)
        card_layout.setSpacing(10)

        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #EAEAEA;
                border: none;
                border-bottom: 1px solid #D0D0D0;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 6, 10, 6)
        header_layout.setSpacing(6)

        minus_lbl = QLabel("-")
        minus_lbl.setFont(QFont("Arial", 11, QFont.Bold))
        minus_lbl.setStyleSheet("color: #333333; border: none; background: transparent;")

        title_lbl = QLabel("Front Side Properties")
        title_lbl.setFont(QFont("Arial", 9.5, QFont.Bold))
        title_lbl.setStyleSheet("color: #222222; border: none; background: transparent;")

        header_layout.addWidget(minus_lbl)
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        card_layout.addWidget(header_frame)

        checkbox_container = QWidget()
        checkbox_container.setStyleSheet("border: none;")
        checkbox_layout = QVBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(12, 4, 12, 0)
        checkbox_layout.setSpacing(10)

        checkbox_style = """
            QCheckBox {
                font-size: 9.5pt;
                font-family: Arial;
                color: #334455;
                spacing: 8px;
                border: none;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #777777;
                border-radius: 2px;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #334455;
            }
        """

        self.cb1 = QCheckBox("Rotate print orientation 180\ndegrees")
        self.cb1.setStyleSheet(checkbox_style)

        self.cb2 = QCheckBox("Tactile Impression Module")
        self.cb2.setStyleSheet(checkbox_style)

        checkbox_layout.addWidget(self.cb1)
        checkbox_layout.addWidget(self.cb2)

        card_layout.addWidget(checkbox_container)
        prop_tab_layout.addWidget(card_frame)

        layers_tab = QWidget()
        layers_tab.setStyleSheet("background-color: #FFFFFF;")

        right_tabs.addTab(properties_tab, "Properties")
        right_tabs.addTab(layers_tab, "Layers")

        right_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background: #EAEAEA;
                color: #333333;
                font-size: 9.5pt;
                font-weight: bold;
                font-family: Arial;
                padding: 8px 24px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                color: #000000;
            }
        """)

        sb_layout.addWidget(right_tabs)
        content_layout.addWidget(sidebar)

        main_layout.addWidget(content_area, stretch=1)

        # ---------------- BOTTOM BUTTON BAR ----------------
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(54)
        bottom_bar.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #CBD5E1;")
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(16, 6, 16, 6)
        bb_layout.setSpacing(10)

        btn_save = QPushButton("Save")
        btn_save.setFixedSize(85, 36)
        btn_save.setFont(QFont("Arial", 9.5, QFont.Bold))
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet("QPushButton { background-color: #0078D7; color: #FFFFFF; border: none; border-radius: 2px; }")

        btn_save_as = QPushButton("Save As...")
        btn_save_as.setFixedSize(90, 36)
        btn_save_as.setFont(QFont("Arial", 9.5))
        btn_save_as.setCursor(Qt.PointingHandCursor)
        btn_save_as.setStyleSheet("QPushButton { background-color: #E1E1E1; color: #000000; border: none; border-radius: 2px; }")

        btn_close = QPushButton("Close")
        btn_close.setFixedSize(80, 36)
        btn_close.setFont(QFont("Arial", 9.5))
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setStyleSheet("QPushButton { background-color: #E1E1E1; color: #000000; border: none; border-radius: 2px; }")
        if on_close_callback:
            btn_close.clicked.connect(on_close_callback)

        btn_print_sample = QPushButton("Print Sample")
        btn_print_sample.setFixedSize(100, 36)
        btn_print_sample.setFont(QFont("Arial", 9.5))
        btn_print_sample.setCursor(Qt.PointingHandCursor)
        btn_print_sample.setStyleSheet("QPushButton { background-color: #E1E1E1; color: #000000; border: none; border-radius: 2px; }")

        btn_quick_start = QPushButton("Quick Start")
        btn_quick_start.setFixedSize(95, 36)
        btn_quick_start.setFont(QFont("Arial", 9.5))
        btn_quick_start.setEnabled(False)
        btn_quick_start.setStyleSheet("QPushButton { background-color: #F2F2F2; color: #A6A6A6; border: 1px solid #E1E1E1; border-radius: 2px; }")

        bb_layout.addWidget(btn_save)
        bb_layout.addWidget(btn_save_as)
        bb_layout.addWidget(btn_close)
        bb_layout.addWidget(btn_print_sample)
        bb_layout.addWidget(btn_quick_start)
        bb_layout.addStretch()

        main_layout.addWidget(bottom_bar)


# -------------------------------------------------------------
# Main Application Window
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1350, 780)
        self.setCentralWidget(CredentialDesignEditorView())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
