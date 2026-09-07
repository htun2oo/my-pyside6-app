import sys
import math
from PySide6.QtCore import Qt, QPointF, Signal, QPoint
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QPolygonF, QCursor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QStackedWidget,
    QTabWidget, QCheckBox, QScrollArea, QComboBox, QGridLayout
)

# -------------------------------------------------------------
# Horizontal Ruler Widget (Photoshop Drag-to-Create Guide)
# -------------------------------------------------------------
class HorizontalRulerWidget(QWidget):
    start_h_guide = Signal(int)

    def __init__(self, height=26, offset=25):
        super().__init__()
        self.setFixedHeight(height)
        self.offset = offset
        self.setCursor(Qt.SizeVerCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#E5E7EB"))
        painter.setPen(QPen(QColor("#9CA3AF"), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        line_pen = QPen(QColor("#000000"), 1)
        font = QFont("Arial", 8, QFont.Bold)
        painter.setFont(font)

        step = 8
        major_step = 40
        
        for x in range(self.offset, -1, -step):
            rel_x = x - self.offset
            if rel_x % major_step == 0:
                painter.setPen(line_pen)
                painter.drawLine(x, self.height() - 14, x, self.height())
            elif rel_x % (step * 2) == 0:
                painter.setPen(line_pen)
                painter.drawLine(x, self.height() - 9, x, self.height())
            else:
                painter.setPen(line_pen)
                painter.drawLine(x, self.height() - 5, x, self.height())

        val = 0
        for x in range(self.offset, self.width(), step):
            rel_x = x - self.offset
            if rel_x % major_step == 0:
                painter.setPen(line_pen)
                painter.drawLine(x, self.height() - 14, x, self.height())
                painter.setPen(QPen(QColor("#000000")))
                painter.drawText(x + 2, 1, 24, 14, Qt.AlignLeft | Qt.AlignTop, str(val))
                val += 2
            elif rel_x % (step * 2) == 0:
                painter.setPen(line_pen)
                painter.drawLine(x, self.height() - 9, x, self.height())
            else:
                painter.setPen(line_pen)
                painter.drawLine(x, self.height() - 5, x, self.height())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Trigger new guideline creation
            global_y = event.globalPosition().toPoint().y()
            self.start_h_guide.emit(global_y)


# -------------------------------------------------------------
# Vertical Ruler Widget (Photoshop Drag-to-Create Guide)
# -------------------------------------------------------------
class VerticalRulerWidget(QWidget):
    start_v_guide = Signal(int)

    def __init__(self, width=26, offset=30):
        super().__init__()
        self.setFixedWidth(width)
        self.offset = offset
        self.setCursor(Qt.SizeHorCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#E5E7EB"))
        painter.setPen(QPen(QColor("#9CA3AF"), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        line_pen = QPen(QColor("#000000"), 1)
        font = QFont("Arial", 8, QFont.Bold)
        painter.setFont(font)

        step = 8
        major_step = 40

        for y in range(self.offset, -1, -step):
            rel_y = y - self.offset
            if rel_y % major_step == 0:
                painter.setPen(line_pen)
                painter.drawLine(self.width() - 14, y, self.width(), y)
            elif rel_y % (step * 2) == 0:
                painter.setPen(line_pen)
                painter.drawLine(self.width() - 9, y, self.width(), y)
            else:
                painter.setPen(line_pen)
                painter.drawLine(self.width() - 5, y, self.width(), y)

        val = 0
        for y in range(self.offset, self.height(), step):
            rel_y = y - self.offset
            if rel_y % major_step == 0:
                painter.setPen(line_pen)
                painter.drawLine(self.width() - 14, y, self.width(), y)
                painter.setPen(QPen(QColor("#000000")))
                painter.drawText(2, y + 2, 20, 12, Qt.AlignLeft | Qt.AlignTop, str(val))
                val += 2
            elif rel_y % (step * 2) == 0:
                painter.setPen(line_pen)
                painter.drawLine(self.width() - 9, y, self.width(), y)
            else:
                painter.setPen(line_pen)
                painter.drawLine(self.width() - 5, y, self.width(), y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Trigger new guideline creation
            global_x = event.globalPosition().toPoint().x()
            self.start_v_guide.emit(global_x)


# -------------------------------------------------------------
# Canvas Overlay Frame (Full Drag, Move & Delete System)
# -------------------------------------------------------------
class CanvasOverlayFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #6B7280; border: none;")
        self.h_guides = []  # Y coordinates
        self.v_guides = []  # X coordinates
        self.active_drag = None
        self.drag_type = None  # 'H' or 'V'
        self.setMouseTracking(True)

    def start_new_h_guide(self, global_y):
        local_y = self.mapFromGlobal(QPoint(0, global_y)).y()
        self.h_guides.append(local_y)
        self.active_drag = len(self.h_guides) - 1
        self.drag_type = 'H'
        self.grabMouse()  # Capture mouse events immediately
        self.update()

    def start_new_v_guide(self, global_x):
        local_x = self.mapFromGlobal(QPoint(global_x, 0)).x()
        self.v_guides.append(local_x)
        self.active_drag = len(self.v_guides) - 1
        self.drag_type = 'V'
        self.grabMouse()  # Capture mouse events immediately
        self.update()

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        # Check if clicking existing horizontal guide
        for idx, y in enumerate(self.h_guides):
            if abs(pos.y() - y) <= 5:
                self.active_drag = idx
                self.drag_type = 'H'
                self.grabMouse()
                return
        # Check if clicking existing vertical guide
        for idx, x in enumerate(self.v_guides):
            if abs(pos.x() - x) <= 5:
                self.active_drag = idx
                self.drag_type = 'V'
                self.grabMouse()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        if self.active_drag is not None:
            if self.drag_type == 'H':
                self.h_guides[self.active_drag] = pos.y()
            elif self.drag_type == 'V':
                self.v_guides[self.active_drag] = pos.x()
            self.update()
        else:
            # Hover detection cursor change
            over_h = any(abs(pos.y() - y) <= 5 for y in self.h_guides)
            over_v = any(abs(pos.x() - x) <= 5 for x in self.v_guides)
            if over_h:
                self.setCursor(Qt.SizeVerCursor)
            elif over_v:
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.active_drag is not None:
            pos = event.position().toPoint()
            # Delete line if dragged out of canvas bounds (Photoshop behaviour)
            if self.drag_type == 'H':
                if pos.y() < 0 or pos.y() > self.height():
                    self.h_guides.pop(self.active_drag)
            elif self.drag_type == 'V':
                if pos.x() < 0 or pos.x() > self.width():
                    self.v_guides.pop(self.active_drag)

            self.active_drag = None
            self.drag_type = None
            self.releaseMouse()
            self.setCursor(Qt.ArrowCursor)
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        
        # Photoshop Cyan Guideline Color (#00FFFF)
        photoshop_cyan = QPen(QColor("#00FFFF"), 1, Qt.SolidLine)
        painter.setPen(photoshop_cyan)

        # Draw Horizontal Guides
        for y in self.h_guides:
            if 0 <= y <= self.height():
                painter.drawLine(0, y, self.width(), y)

        # Draw Vertical Guides
        for x in self.v_guides:
            if 0 <= x <= self.width():
                painter.drawLine(x, 0, x, self.height())


# -------------------------------------------------------------
# Layer Item Widget
# -------------------------------------------------------------
class LayerItemWidget(QFrame):
    item_selected = Signal(str)
    visibility_toggled = Signal(str, bool)
    check_toggled = Signal(str, bool)

    def __init__(self, layer_name, is_selected=False, is_checked=False, is_visible=True):
        super().__init__()
        self.layer_name = layer_name
        self.is_selected = is_selected
        self.is_visible = is_visible

        self.setFixedHeight(28)
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(8)

        self.eye_btn = QPushButton("👁" if is_visible else "❌")
        self.eye_btn.setFixedSize(20, 20)
        self.eye_btn.setFont(QFont("Segoe UI", 8))
        self.eye_btn.setCursor(Qt.PointingHandCursor)
        self.eye_btn.setStyleSheet("QPushButton { background: transparent; border: none; color: #4B5563; } QPushButton:hover { color: #2563EB; }")
        self.eye_btn.clicked.connect(self.toggle_eye)
        layout.addWidget(self.eye_btn)

        self.name_lbl = QLabel(layer_name)
        self.name_lbl.setFont(QFont("Segoe UI", 9))
        self.name_lbl.setStyleSheet("background: transparent;")
        layout.addWidget(self.name_lbl, stretch=1)

        self.chk = QCheckBox()
        self.chk.setChecked(is_checked)
        self.chk.setCursor(Qt.PointingHandCursor)
        self.chk.setStyleSheet("QCheckBox::indicator { width: 13px; height: 13px; border: 1px solid #9CA3AF; background-color: #FFFFFF; } QCheckBox::indicator:checked { background-color: #2563EB; border-color: #2563EB; }")
        self.chk.toggled.connect(self.on_checkbox_toggled)
        layout.addWidget(self.chk)

        self.update_style()

    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("QFrame { background-color: #B2C8E6; border-radius: 2px; }")
            self.name_lbl.setStyleSheet("color: #1E3A8A; font-weight: bold; background: transparent;")
        else:
            self.setStyleSheet("QFrame { background-color: transparent; } QFrame:hover { background-color: #D1D5DB; }")
            self.name_lbl.setStyleSheet("color: #374151; background: transparent;")

    def set_selected(self, selected):
        self.is_selected = selected
        self.update_style()

    def toggle_eye(self):
        self.is_visible = not self.is_visible
        self.eye_btn.setText("👁" if self.is_visible else "❌")
        self.visibility_toggled.emit(self.layer_name, self.is_visible)

    def set_visible_state(self, visible):
        self.is_visible = visible
        self.eye_btn.setText("👁" if self.is_visible else "❌")

    def on_checkbox_toggled(self, checked):
        self.check_toggled.emit(self.layer_name, checked)

    def set_checked_state(self, checked):
        self.chk.blockSignals(True)
        self.chk.setChecked(checked)
        self.chk.blockSignals(False)

    def mousePressEvent(self, event):
        self.item_selected.emit(self.layer_name)
        super().mousePressEvent(event)


# -------------------------------------------------------------
# Instant PVC Logo Widget
# -------------------------------------------------------------
class InstantPVCLogo(QWidget):
    def __init__(self, size=40, is_white=True):
        super().__init__()
        self.setFixedSize(size, size)
        self.size_val = size
        self.is_white = is_white

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        center = self.size_val / 2
        radius = center - 3
        points = [
            QPointF(center + radius * math.cos(math.radians(60 * i - 30)),
                    center + radius * math.sin(math.radians(60 * i - 30)))
            for i in range(6)
        ]

        color = QColor("#FFFFFF") if self.is_white else QColor("#6B21A8")
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(QPolygonF(points))

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        s = self.size_val / 70
        painter.drawRoundedRect(22 * s, 22 * s, 26 * s, 18 * s, 2, 2)


# -------------------------------------------------------------
# Card Canvas Box Container
# -------------------------------------------------------------
class SelectableCardWidget(QWidget):
    clicked = Signal()

    def __init__(self, side_text):
        super().__init__()
        self.setFixedWidth(380)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        header_layout = QHBoxLayout()
        self.side_lbl = QLabel(side_text)
        self.side_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.side_lbl.setStyleSheet("color: #374151; background: transparent;")

        self.layer_lbl = QLabel("")
        self.layer_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.layer_lbl.setStyleSheet("color: #374151; background: transparent;")

        header_layout.addWidget(self.side_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.layer_lbl)

        layout.addLayout(header_layout)

        self.canvas_frame = QFrame()
        self.canvas_frame.setFixedHeight(310)
        self.canvas_frame.setStyleSheet("background-color: #E5E7EB; border: 1px solid #9CA3AF;")

        grid_layout = QGridLayout(self.canvas_frame)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(0)

        # Top-Left Corner Box
        corner_box = QWidget()
        corner_box.setFixedSize(26, 26)
        corner_box.setStyleSheet("background-color: #E5E7EB; border-right: 1px solid #9CA3AF; border-bottom: 1px solid #9CA3AF;")
        grid_layout.addWidget(corner_box, 0, 0)

        # Rulers Alignment (Left Offset 25, Top Offset 30)
        self.h_ruler = HorizontalRulerWidget(height=26, offset=25)
        self.v_ruler = VerticalRulerWidget(width=26, offset=30)

        grid_layout.addWidget(self.h_ruler, 0, 1)
        grid_layout.addWidget(self.v_ruler, 1, 0)

        # Interactive Overlay Frame
        self.gray_box = CanvasOverlayFrame()
        
        gray_layout = QVBoxLayout(self.gray_box)
        gray_layout.setContentsMargins(25, 30, 25, 30)

        self.white_card = QFrame()
        self.white_card.setFixedHeight(210)
        self.white_card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #1F2937; border-radius: 12px;")

        gray_layout.addWidget(self.white_card)
        grid_layout.addWidget(self.gray_box, 1, 1)

        # Connect Drag-Create signals
        self.h_ruler.start_h_guide.connect(self.gray_box.start_new_h_guide)
        self.v_ruler.start_v_guide.connect(self.gray_box.start_new_v_guide)

        layout.addWidget(self.canvas_frame)

    def set_layer_text(self, text):
        self.layer_lbl.setText(text)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


# -------------------------------------------------------------
# Card Designer Main View
# -------------------------------------------------------------
class CardDesignerWidget(QWidget):
    def __init__(self, card_name="Credential Design 1", on_close_callback=None):
        super().__init__()
        self.on_close_callback = on_close_callback
        self.layer_widgets = {}

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        purple_ribbon = QFrame()
        purple_ribbon.setFixedHeight(36)
        purple_ribbon.setStyleSheet("background-color: #5B21B6;")
        purple_layout = QHBoxLayout(purple_ribbon)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        title_lbl = QLabel(f"{card_name} ✏")
        title_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF;")
        purple_layout.addWidget(title_lbl)
        purple_layout.addStretch()

        main_layout.addWidget(purple_ribbon)

        toolbar = QFrame()
        toolbar.setFixedHeight(40)
        toolbar.setStyleSheet("background-color: #E5E7EB; border-bottom: 1px solid #D1D5DB;")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(10, 2, 10, 2)
        tb_layout.setSpacing(3)

        tools = ["↩", "↪", "📄+", "✂", "📋", "T", "T_i", "👤", "🖼", "📊", "〰", "||||", "💳", "💻", "╱", "⬜", "⭕", "📱", "▦", "🔍+", "🔍-"]
        for tool in tools:
            btn = QPushButton(tool)
            btn.setFixedSize(26, 26)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("QPushButton { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 2px; font-size: 11px; font-weight: bold; color: #374151; } QPushButton:hover { background-color: #F3F4F6; border-color: #6B21A8; }")
            tb_layout.addWidget(btn)

        tb_layout.addSpacing(8)
        zoom_combo = QComboBox()
        zoom_combo.addItems(["100%", "75%", "50%", "150%"])
        zoom_combo.setFixedWidth(65)
        zoom_combo.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; font-size: 11px;")
        tb_layout.addWidget(zoom_combo)

        tb_layout.addStretch()
        main_layout.addWidget(toolbar)

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setStyleSheet("background-color: #EFEFEF; border: none;")

        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(20, 20, 20, 20)

        cards_outer_layout = QHBoxLayout()
        cards_outer_layout.setSpacing(30)

        self.front_card = SelectableCardWidget("Front Side")
        self.back_card = SelectableCardWidget("Back Side")

        cards_outer_layout.addStretch()
        cards_outer_layout.addWidget(self.front_card)
        cards_outer_layout.addWidget(self.back_card)
        cards_outer_layout.addStretch()

        canvas_layout.addLayout(cards_outer_layout)
        canvas_layout.addStretch()

        canvas_scroll.setWidget(canvas_container)
        body_layout.addWidget(canvas_scroll, stretch=1)

        right_panel = QFrame()
        right_panel.setFixedWidth(270)
        right_panel.setStyleSheet("background-color: #E5E7EB; border-left: 1px solid #C0C0C0;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(6, 6, 6, 6)

        self.prop_tabs = QTabWidget()
        self.prop_tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #C0C0C0; background-color: #E5E7EB; top: -1px; } QTabBar::tab { background: #D1D5DB; color: #374151; padding: 6px 20px; font-size: 11px; font-weight: bold; border: 1px solid #C0C0C0; margin-right: 2px; } QTabBar::tab:selected { background: #FFFFFF; border-bottom: 1px solid #FFFFFF; color: #111827; }")

        properties_page = QWidget()
        properties_page.setStyleSheet("background-color: #E5E7EB;")
        prop_page_layout = QVBoxLayout(properties_page)
        prop_page_layout.setContentsMargins(8, 12, 8, 12)

        prop_box = QFrame()
        prop_box.setStyleSheet("background-color: #DCDCDC; border: 1px solid #C0C0C0;")
        box_layout = QVBoxLayout(prop_box)
        box_layout.setContentsMargins(10, 10, 10, 10)
        box_layout.setSpacing(10)

        self.prop_title = QLabel("- Front Side Properties")
        self.prop_title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.prop_title.setStyleSheet("color: #1F2937; border: none; background: transparent;")
        box_layout.addWidget(self.prop_title)

        box_layout.addWidget(QCheckBox("Rotate print orientation 180 degrees"))
        box_layout.addWidget(QCheckBox("Tactile Impression Module"))

        prop_page_layout.addWidget(prop_box)
        prop_page_layout.addStretch()

        layers_page = QWidget()
        layers_page.setStyleSheet("background-color: #E5E7EB;")
        layers_page_layout = QVBoxLayout(layers_page)
        layers_page_layout.setContentsMargins(8, 12, 8, 12)

        layer_container = QFrame()
        layer_container.setStyleSheet("background-color: #E5E7EB; border: 1px solid #C0C0C0;")
        layer_box_layout = QVBoxLayout(layer_container)
        layer_box_layout.setContentsMargins(6, 8, 6, 8)
        layer_box_layout.setSpacing(2)

        self.layer_header_lbl = QLabel("Front Side")
        self.layer_header_lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.layer_header_lbl.setStyleSheet("color: #1F2937; border: none; background: transparent;")
        layer_box_layout.addWidget(self.layer_header_lbl)

        layer_data = [
            ("All layers", False, False), ("Background", False, False), ("Color", True, True),
            ("Black", False, False), ("Topcoat", False, True), ("Retransfer Material", False, False),
            ("Luster/Fluorescent", False, False), ("Non-printable area", False, False),
            ("Lamination", False, False), ("Emboss or indent", False, False), ("Magnetic stripe", False, False)
        ]

        for name, is_sel, is_chk in layer_data:
            item_w = LayerItemWidget(name, is_selected=is_sel, is_checked=is_chk)
            item_w.item_selected.connect(self.on_layer_selected)
            item_w.visibility_toggled.connect(self.on_layer_visibility_toggled)
            item_w.check_toggled.connect(self.on_layer_check_toggled)
            self.layer_widgets[name] = item_w
            layer_box_layout.addWidget(item_w)

        layer_box_layout.addStretch()
        layers_page_layout.addWidget(layer_container)

        self.prop_tabs.addTab(properties_page, "Properties")
        self.prop_tabs.addTab(layers_page, "Layers")

        right_layout.addWidget(self.prop_tabs)
        body_layout.addWidget(right_panel)

        main_layout.addLayout(body_layout, stretch=1)

        footer = QFrame()
        footer.setFixedHeight(36)
        footer.setStyleSheet("background-color: #E5E7EB; border-top: 1px solid #D1D5DB;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 0, 15, 0)
        footer_layout.setSpacing(6)

        btn_style = "QPushButton { background-color: #2563EB; color: white; font-weight: bold; font-size: 11px; border: none; border-radius: 3px; padding: 4px 12px; } QPushButton:hover { background-color: #1D4ED8; }"
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(btn_style)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(btn_style)
        if self.on_close_callback:
            close_btn.clicked.connect(self.on_close_callback)

        footer_layout.addWidget(save_btn)
        footer_layout.addWidget(close_btn)
        footer_layout.addStretch()

        main_layout.addWidget(footer)

        self.front_card.clicked.connect(self.select_front_side)
        self.back_card.clicked.connect(self.select_back_side)
        self.select_front_side()

    def on_layer_selected(self, selected_layer_name):
        for name, widget in self.layer_widgets.items():
            widget.set_selected(name == selected_layer_name)

        if self.front_card.layer_lbl.text() != "":
            self.front_card.set_layer_text(f"Active Design Layer: {selected_layer_name}")
        elif self.back_card.layer_lbl.text() != "":
            self.back_card.set_layer_text(f"Active Design Layer: {selected_layer_name}")

    def on_layer_visibility_toggled(self, layer_name, visible):
        if layer_name == "All layers":
            for name, widget in self.layer_widgets.items():
                if name != "All layers":
                    widget.set_visible_state(visible)

    def on_layer_check_toggled(self, layer_name, checked):
        if layer_name == "All layers":
            for name, widget in self.layer_widgets.items():
                if name != "All layers":
                    widget.set_checked_state(checked)

    def select_front_side(self):
        self.front_card.set_layer_text("Active Design Layer: Color")
        self.back_card.set_layer_text("")
        self.prop_title.setText("- Front Side Properties")
        self.layer_header_lbl.setText("Front Side")

    def select_back_side(self):
        self.front_card.set_layer_text("")
        self.back_card.set_layer_text("Active Design Layer: Black")
        self.prop_title.setText("- Back Side Properties")
        self.layer_header_lbl.setText("Back Side")


# -------------------------------------------------------------
# Main Dashboard Panel
# -------------------------------------------------------------
class MainDashboardWidget(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        nav_bar = QFrame()
        nav_bar.setFixedHeight(45)
        nav_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(15, 0, 15, 0)

        brand_box = QHBoxLayout()
        brand_box.setSpacing(8)
        brand_box.addWidget(InstantPVCLogo(size=28, is_white=False))
        
        brand_title = QLabel("ENTRUST")
        brand_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        brand_title.setStyleSheet("color: #4C1D95;")
        brand_box.addWidget(brand_title)

        sub_brand = QLabel("Adaptive Issuance Instant ID")
        sub_brand.setFont(QFont("Segoe UI", 9))
        sub_brand.setStyleSheet("color: #6B21A8; padding-left: 5px; border-left: 1px solid #D1D5DB;")
        brand_box.addWidget(sub_brand)

        nav_layout.addLayout(brand_box)
        nav_layout.addSpacing(20)

        self.home_btn = QPushButton("Home")
        self.design_btn = QPushButton("Design")
        self.printer_btn = QPushButton("Printer Queues")

        for btn in [self.home_btn, self.design_btn, self.printer_btn]:
            btn.setCursor(Qt.PointingHandCursor)

        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.design_btn)
        nav_layout.addWidget(self.printer_btn)
        nav_layout.addStretch()

        user_lbl = QLabel(f"{self.username} ▾  ⚙  🔔  ❓  ℹ")
        user_lbl.setStyleSheet("color: #374151; font-weight: 600;")
        nav_layout.addWidget(user_lbl)

        main_layout.addWidget(nav_bar)

        purple_bar = QFrame()
        purple_bar.setFixedHeight(38)
        purple_bar.setStyleSheet("background-color: #6B21A8;")
        purple_layout = QHBoxLayout(purple_bar)
        purple_layout.setContentsMargins(15, 0, 15, 0)

        self.purple_tab_stack = QStackedWidget()

        home_tabs_bar = QFrame()
        home_tabs_layout = QHBoxLayout(home_tabs_bar)
        home_tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.cred_tab_btn = QPushButton("Credentials")
        self.logs_tab_btn = QPushButton("System Logs")
        home_tabs_layout.addWidget(self.cred_tab_btn)
        home_tabs_layout.addWidget(self.logs_tab_btn)
        home_tabs_layout.addStretch()

        design_tabs_bar = QFrame()
        design_tabs_layout = QHBoxLayout(design_tabs_bar)
        design_tabs_layout.setContentsMargins(0, 0, 0, 0)
        design_tabs_layout.setSpacing(4)
        
        self.cards_tab_btn = QPushButton("Cards")
        self.workflows_tab_btn = QPushButton("Workflows")
        self.reports_tab_btn = QPushButton("Reports")
        self.field_conn_tab_btn = QPushButton("Field Connections")

        self.design_tab_buttons = [self.cards_tab_btn, self.workflows_tab_btn, self.reports_tab_btn, self.field_conn_tab_btn]
        purple_tab_style = "QPushButton { background-color: #7C3AED; color: #EDE9FE; border: none; border-top-left-radius: 4px; border-top-right-radius: 4px; padding: 5px 14px; font-weight: bold; font-size: 11px; } QPushButton:hover { background-color: #8B5CF6; color: #FFFFFF; }"

        for btn in [self.cred_tab_btn, self.logs_tab_btn] + self.design_tab_buttons:
            btn.setStyleSheet(purple_tab_style)
            btn.setCursor(Qt.PointingHandCursor)

        design_tabs_layout.addWidget(self.cards_tab_btn)
        design_tabs_layout.addWidget(self.workflows_tab_btn)
        design_tabs_layout.addWidget(self.reports_tab_btn)
        design_tabs_layout.addWidget(self.field_conn_tab_btn)
        design_tabs_layout.addStretch()

        self.purple_tab_stack.addWidget(home_tabs_bar)
        self.purple_tab_stack.addWidget(design_tabs_bar)

        purple_layout.addWidget(self.purple_tab_stack)
        main_layout.addWidget(purple_bar)

        self.content_stack = QStackedWidget()

        cred_page = QWidget()
        cred_layout = QVBoxLayout(cred_page)
        cred_layout.setContentsMargins(20, 20, 20, 20)
        cred_layout.addWidget(QLabel("No credentials available.", alignment=Qt.AlignCenter))

        logs_page = QWidget()
        logs_layout = QVBoxLayout(logs_page)
        logs_layout.addWidget(QLabel("System Logs Information", alignment=Qt.AlignCenter))

        cards_page = QWidget()
        cards_layout = QVBoxLayout(cards_page)
        cards_layout.setContentsMargins(20, 20, 20, 20)

        cards_top_action_bar = QHBoxLayout()
        cards_top_action_bar.addStretch()

        create_card_btn = QPushButton("+ Create Card Design")
        create_card_btn.setFixedSize(160, 36)
        create_card_btn.setCursor(Qt.PointingHandCursor)
        create_card_btn.setStyleSheet("QPushButton { background-color: #2563EB; color: #FFFFFF; font-size: 12px; font-weight: bold; border: none; border-radius: 4px; } QPushButton:hover { background-color: #1D4ED8; }")
        create_card_btn.clicked.connect(self.open_designer_view)

        cards_top_action_bar.addWidget(create_card_btn)
        cards_layout.addLayout(cards_top_action_bar)
        cards_layout.addStretch()

        workflows_page = QWidget()
        reports_page = QWidget()
        field_conn_page = QWidget()

        self.designer_view = CardDesignerWidget(card_name="Credential Design 1", on_close_callback=self.close_designer_view)

        self.content_stack.addWidget(cred_page)
        self.content_stack.addWidget(logs_page)
        self.content_stack.addWidget(cards_page)
        self.content_stack.addWidget(workflows_page)
        self.content_stack.addWidget(reports_page)
        self.content_stack.addWidget(field_conn_page)
        self.content_stack.addWidget(self.designer_view)

        main_layout.addWidget(self.content_stack)

        self.home_btn.clicked.connect(self.show_home_view)
        self.design_btn.clicked.connect(self.show_design_view)

        self.cred_tab_btn.clicked.connect(lambda: self.switch_home_tab(0, self.cred_tab_btn))
        self.logs_tab_btn.clicked.connect(lambda: self.switch_home_tab(1, self.logs_tab_btn))

        self.cards_tab_btn.clicked.connect(lambda: self.switch_design_tab(2, self.cards_tab_btn))
        self.workflows_tab_btn.clicked.connect(lambda: self.switch_design_tab(3, self.workflows_tab_btn))
        self.reports_tab_btn.clicked.connect(lambda: self.switch_design_tab(4, self.reports_tab_btn))
        self.field_conn_tab_btn.clicked.connect(lambda: self.switch_design_tab(5, self.field_conn_tab_btn))

        self.show_home_view()

    def update_purple_tab_active(self, active_btn, btn_group):
        active_style = "QPushButton { background-color: #FFFFFF; color: #6B21A8; border: none; border-top-left-radius: 4px; border-top-right-radius: 4px; padding: 5px 14px; font-weight: bold; font-size: 11px; }"
        normal_style = "QPushButton { background-color: #7C3AED; color: #EDE9FE; border: none; border-top-left-radius: 4px; border-top-right-radius: 4px; padding: 5px 14px; font-weight: bold; font-size: 11px; } QPushButton:hover { background-color: #8B5CF6; color: #FFFFFF; }"
        for btn in btn_group:
            btn.setStyleSheet(active_style if btn == active_btn else normal_style)

    def switch_home_tab(self, index, btn):
        self.content_stack.setCurrentIndex(index)
        self.update_purple_tab_active(btn, [self.cred_tab_btn, self.logs_tab_btn])

    def switch_design_tab(self, index, btn):
        self.content_stack.setCurrentIndex(index)
        self.update_purple_tab_active(btn, self.design_tab_buttons)

    def set_nav_active(self, active_btn):
        active_style = "QPushButton { color: #6B21A8; border-bottom: 2px solid #6B21A8; font-weight: bold; padding: 10px 14px; background: transparent; }"
        normal_style = "QPushButton { color: #374151; border-bottom: 2px solid transparent; font-weight: 600; padding: 10px 14px; background: transparent; } QPushButton:hover { color: #6B21A8; }"

        self.home_btn.setStyleSheet(active_style if active_btn == "home" else normal_style)
        self.design_btn.setStyleSheet(active_style if active_btn == "design" else normal_style)
        self.printer_btn.setStyleSheet(normal_style)

    def show_home_view(self):
        self.set_nav_active("home")
        self.purple_tab_stack.setCurrentIndex(0)
        self.switch_home_tab(0, self.cred_tab_btn)

    def show_design_view(self):
        self.set_nav_active("design")
        self.purple_tab_stack.setCurrentIndex(1)
        self.switch_design_tab(2, self.cards_tab_btn)

    def open_designer_view(self):
        self.content_stack.setCurrentIndex(6)

    def close_designer_view(self):
        self.show_design_view()


# -------------------------------------------------------------
# Login Window
# -------------------------------------------------------------
class LoginWidget(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4C1D95, stop:1 #2E1065);")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        center_box = QWidget()
        center_box.setFixedWidth(420)
        box_layout = QVBoxLayout(center_box)
        box_layout.setSpacing(15)

        box_layout.addWidget(InstantPVCLogo(size=70, is_white=True), 0, Qt.AlignCenter)

        title_lbl = QLabel("INSTANT PVC")
        title_lbl.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; letter-spacing: 2px;")
        title_lbl.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(title_lbl)

        form_card = QFrame()
        form_card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 8px; } QLabel { color: #4B5563; font-size: 13px; font-weight: 600; } QLineEdit { background-color: #F9FAFB; border: 1px solid #D1D5DB; border-radius: 6px; padding: 8px 10px; font-size: 13px; color: #111827; }")
        
        card_layout = QVBoxLayout(form_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(10)

        card_layout.addWidget(QLabel("User ID"))
        self.user_entry = QLineEdit("admin")
        self.user_entry.setFixedHeight(38)
        card_layout.addWidget(self.user_entry)

        card_layout.addWidget(QLabel("Password"))
        self.pass_entry = QLineEdit("admin123")
        self.pass_entry.setEchoMode(QLineEdit.Password)
        self.pass_entry.setFixedHeight(38)
        card_layout.addWidget(self.pass_entry)

        box_layout.addWidget(form_card)

        login_btn = QPushButton("Sign In")
        login_btn.setFixedSize(120, 38)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("QPushButton { background-color: #2563EB; color: white; font-weight: bold; font-size: 14px; border: none; border-radius: 4px; }")
        login_btn.clicked.connect(self.check_login)
        box_layout.addWidget(login_btn, 0, Qt.AlignCenter)

        main_layout.addWidget(center_box)

    def check_login(self):
        if self.user_entry.text().strip() == "admin" and self.pass_entry.text().strip() == "admin123":
            self.on_login_success("admin")
        else:
            QMessageBox.critical(self, "Login Failed", "User ID သို့မဟုတ် Password မှားယွင်းနေပါသည်။")


# -------------------------------------------------------------
# Main Application Window
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENTRUST Adaptive Issuance - Instant PVC")
        self.resize(1150, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_widget = LoginWidget(self.show_dashboard)
        self.stack.addWidget(self.login_widget)

    def show_dashboard(self, username):
        self.dashboard_widget = MainDashboardWidget(username)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.setCurrentWidget(self.dashboard_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
