import sys
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QPen, QPainterPath, QLinearGradient
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QComboBox, QCheckBox,
    QToolButton, QScrollArea, QTabWidget
)

# -------------------------------------------------------------
# Toolbar & Icons Generator
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

    p.end()
    return QIcon(pixmap)


# -------------------------------------------------------------
# ဘေးဘက်သို့ 600px အထိ ပိုမိုကျယ်ပြန့်သွားအောင် ပြင်ဆင်ထားသော Custom Canvas
# -------------------------------------------------------------
class CustomGradientCardArea(QFrame):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Background Canvas Width ကို 600px အထိ ပိုမိုကျယ်ပြန့်အောင် ပြင်ဆင်ထားပါသည်
        self.setFixedSize(600, 540)
        self.is_selected = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 1. Smooth Linear Gradient Background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#A2A2A2"))
        gradient.setColorAt(1.0, QColor("#828282"))

        painter.fillRect(self.rect(), gradient)

        # 2. Card Dimensions (Canvas Width ကျယ်သွားသော်လည်း အလယ်တည့်တည့်၌ အလိုအလျောက် ရောက်ရှိနေပါမည်)
        card_w, card_h = 285, 180
        card_x = (self.width() - card_w) / 2
        card_y = 65

        card_rect = QRectF(card_x, card_y, card_w, card_h)

        # 3. Corner Outlines (Black Background behind inner card)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#000000"))
        painter.drawRect(card_rect)

        # 4. Inner White Card with Rounded Corners
        inner_rect = card_rect.adjusted(2, 2, -2, -2)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawRoundedRect(inner_rect, 14, 14)

        # 5. Active Selection Border
        if self.is_selected:
            pen = QPen(QColor("#0078D7"), 3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        painter.end()


# -------------------------------------------------------------
# Main Application View
# -------------------------------------------------------------
class CredentialDesignEditorView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. TOP HEADER & TABS ---
        top_bar = QFrame()
        top_bar.setFixedHeight(48)
        top_bar.setStyleSheet("background-color: #7B0082; border: none;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(15, 0, 15, 0)
        top_layout.setSpacing(10)

        app_title = QLabel("ENTRUST Adaptive Issuance Instant ID")
        app_title.setFont(QFont("Arial", 11, QFont.Bold))
        app_title.setStyleSheet("color: #FFFFFF;")
        top_layout.addWidget(app_title)

        top_layout.addSpacing(30)

        nav_tabs_layout = QHBoxLayout()
        nav_tabs_layout.setSpacing(2)

        tab_home = QPushButton("Home")
        tab_design = QPushButton("Design")
        tab_queues = QPushButton("Printer Queues")

        active_tab_style = """
            QPushButton {
                background-color: #FFFFFF;
                color: #7B0082;
                font-family: Arial;
                font-size: 9.5pt;
                font-weight: bold;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 16px;
            }
        """
        inactive_tab_style = """
            QPushButton {
                background-color: transparent;
                color: #E2D0E6;
                font-family: Arial;
                font-size: 9.5pt;
                border: none;
                padding: 6px 16px;
            }
            QPushButton:hover {
                color: #FFFFFF;
                background-color: #8C0094;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
        """

        tab_home.setStyleSheet(inactive_tab_style)
        tab_design.setStyleSheet(active_tab_style)
        tab_queues.setStyleSheet(inactive_tab_style)

        nav_tabs_layout.addWidget(tab_home)
        nav_tabs_layout.addWidget(tab_design)
        nav_tabs_layout.addWidget(tab_queues)

        top_layout.addLayout(nav_tabs_layout)
        top_layout.addStretch()

        main_layout.addWidget(top_bar)

        # --- Sub Header Ribbon ---
        sub_header = QFrame()
        sub_header.setFixedHeight(40)
        sub_header.setStyleSheet("background-color: #800080;")
        sub_layout = QHBoxLayout(sub_header)
        sub_layout.setContentsMargins(15, 0, 15, 0)
        
        lbl_sub = QLabel("Credential Design 1")
        lbl_sub.setFont(QFont("Arial", 11, QFont.Bold))
        lbl_sub.setStyleSheet("color: #FFFFFF;")
        
        sub_layout.addWidget(lbl_sub)
        sub_layout.addStretch()
        main_layout.addWidget(sub_header)

        # --- 2. TOOLBAR ---
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
        for ik in ["undo", "redo"]:
            btn = QToolButton()
            btn.setFixedSize(42, 38)
            btn.setIcon(make_toolbar_icon(ik, size=32))
            btn.setIconSize(btn.size())
            btn.setStyleSheet(btn_style)
            grp1.addWidget(btn)

        sep1 = QFrame()
        sep1.setFixedWidth(12)

        grp2 = QHBoxLayout()
        grp2.setSpacing(0)
        for ik in ["copy", "cut", "paste"]:
            btn = QToolButton()
            btn.setFixedSize(42, 38)
            btn.setIcon(make_toolbar_icon(ik, size=32))
            btn.setIconSize(btn.size())
            btn.setStyleSheet(btn_style)
            grp2.addWidget(btn)

        sep2 = QFrame()
        sep2.setFixedWidth(12)

        grp3 = QHBoxLayout()
        grp3.setSpacing(0)
        for ik in ["text", "static_text", "photo", "static_graphic", "variable_graphic", "date", "signature"]:
            btn = QToolButton()
            btn.setFixedSize(42, 38)
            btn.setIcon(make_toolbar_icon(ik, size=32))
            btn.setIconSize(btn.size())
            btn.setStyleSheet(btn_style)
            grp3.addWidget(btn)

        sep3 = QFrame()
        sep3.setFixedWidth(12)

        grp4 = QHBoxLayout()
        grp4.setSpacing(0)
        for ik in ["barcode", "magnetic_stripe", "chip"]:
            btn = QToolButton()
            btn.setFixedSize(42, 38)
            btn.setIcon(make_toolbar_icon(ik, size=32))
            btn.setIconSize(btn.size())
            btn.setStyleSheet(btn_style)
            grp4.addWidget(btn)

        sep4 = QFrame()
        sep4.setFixedWidth(12)

        grp5 = QHBoxLayout()
        grp5.setSpacing(0)
        for ik in ["line", "rectangle", "ellipse", "ruler", "grid_lines", "zoom_out", "zoom_in"]:
            btn = QToolButton()
            btn.setFixedSize(42, 38)
            btn.setIcon(make_toolbar_icon(ik, size=32))
            btn.setIconSize(btn.size())
            btn.setStyleSheet(btn_style)
            grp5.addWidget(btn)

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

        # --- 3. WORKSPACE / CARD AREA ---
        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #FFFFFF; }")

        canvas_container = QWidget()
        canvas_container.setStyleSheet("background-color: #FFFFFF;")
        canvas_layout = QHBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(12, 10, 12, 0)
        canvas_layout.setSpacing(25)
        canvas_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # FRONT SIDE
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

        self.front_card_bg = CustomGradientCardArea()

        front_container.addLayout(front_header_row)
        front_container.addWidget(self.front_card_bg)

        # BACK SIDE
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

        self.back_card_bg = CustomGradientCardArea()

        back_container.addLayout(back_header_row)
        back_container.addWidget(self.back_card_bg)

        canvas_layout.addLayout(front_container)
        canvas_layout.addLayout(back_container)

        scroll_area.setWidget(canvas_container)
        content_layout.addWidget(scroll_area, stretch=1)

        # --- 4. RIGHT SIDEBAR ---
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
        card_frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 1px solid #D0D0D0; border-radius: 4px; }")
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(0, 0, 0, 12)
        card_layout.setSpacing(10)

        header_frame = QFrame()
        header_frame.setStyleSheet("QFrame { background-color: #EAEAEA; border: none; border-bottom: 1px solid #D0D0D0; border-top-left-radius: 4px; border-top-right-radius: 4px; }")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 6, 10, 6)
        header_layout.setSpacing(6)

        minus_lbl = QLabel("-")
        minus_lbl.setFont(QFont("Arial", 11, QFont.Bold))
        minus_lbl.setStyleSheet("color: #333333; border: none; background: transparent;")

        self.prop_title_lbl = QLabel("Front Side Properties")
        self.prop_title_lbl.setFont(QFont("Arial", 9.5, QFont.Bold))
        self.prop_title_lbl.setStyleSheet("color: #222222; border: none; background: transparent;")

        header_layout.addWidget(minus_lbl)
        header_layout.addWidget(self.prop_title_lbl)
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

        cb1 = QCheckBox("Rotate print orientation 180\ndegrees")
        cb1.setStyleSheet(checkbox_style)

        cb2 = QCheckBox("Tactile Impression Module")
        cb2.setStyleSheet(checkbox_style)

        checkbox_layout.addWidget(cb1)
        checkbox_layout.addWidget(cb2)

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

        # --- 5. BOTTOM BUTTON BAR ---
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

        # Signals
        self.front_card_bg.clicked.connect(self.select_front_side)
        self.back_card_bg.clicked.connect(self.select_back_side)

        self.select_front_side()

    def select_front_side(self):
        self.front_card_bg.set_selected(True)
        self.back_card_bg.set_selected(False)
        self.active_layer_lbl.setText("Active Design Layer: Color (Front Side)")
        self.prop_title_lbl.setText("Front Side Properties")

    def select_back_side(self):
        self.front_card_bg.set_selected(False)
        self.back_card_bg.set_selected(True)
        self.active_layer_lbl.setText("Active Design Layer: Color (Back Side)")
        self.prop_title_lbl.setText("Back Side Properties")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance Instant ID")
        self.resize(1500, 820)
        self.setCentralWidget(CredentialDesignEditorView())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
