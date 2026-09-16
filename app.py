import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QComboBox, QCheckBox,
    QToolButton, QDialog, QLineEdit, QTextEdit
)

# -------------------------------------------------------------
# Icons Helpers
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
# Edit Properties Dialog Popup Window (Fixed Dropdown & Default Sizes)
# -------------------------------------------------------------
class EditPropertiesDialog(QDialog):
    def __init__(self, current_name="Credential Design 1", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setFixedSize(410, 560)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; border: 1px solid #000000; }")

        # Preset Dimension Values
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
            QPushButton {
                background: #6B0072; color: #FFFFFF; border: none; border-radius: 10px; font-weight: bold; font-size: 10px;
            }
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
        
        # Fixed Dropdown Stylesheet - Dropdown List Text များကို ရှင်းလင်းစွာ မြင်ရစေရန် ပြင်ဆင်ထားသည်
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
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0284C7;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #94A3B8;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #94A3B8;
                background-color: #FFFFFF;
                color: #0F172A;
                selection-background-color: #0284C7;
                selection-color: #FFFFFF;
                padding: 4px;
            }
        """

        # Name Field
        lbl_name = QLabel("Name")
        lbl_name.setStyleSheet(label_style)
        self.txt_name = QLineEdit(current_name)
        self.txt_name.setReadOnly(False)
        self.txt_name.setFixedSize(230, 26)
        self.txt_name.setStyleSheet(input_style)

        # Dimensions Dropdown
        lbl_dim = QLabel("Dimensions")
        lbl_dim.setStyleSheet(label_style)
        self.cbo_dim = QComboBox()
        self.cbo_dim.addItems(["ISO ID-1", "CR-50", "Custom"])
        self.cbo_dim.setFixedSize(140, 26)
        self.cbo_dim.setStyleSheet(input_style)

        # Units Dropdown
        lbl_units = QLabel("Units")
        lbl_units.setStyleSheet(label_style)
        self.cbo_units = QComboBox()
        self.cbo_units.addItems(["Centimeters", "Millimeters"])
        self.cbo_units.setFixedSize(140, 26)
        self.cbo_units.setStyleSheet(input_style)

        # Width Input (Default Card Size Width = 8.5725)
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

        # Height Input (Default Card Size Height = 5.3975)
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

        # Connect Signals for Live Updates
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

        # Description
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

        # Bottom Buttons
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(44)
        bottom_bar.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(16, 0, 16, 0)
        bb_layout.setSpacing(10)

        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(72, 28)
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.setStyleSheet("""
            QPushButton { background-color: #0284C7; color: #FFFFFF; font-weight: bold; border: none; border-radius: 3px; }
            QPushButton:hover { background-color: #0369A1; }
        """)
        btn_ok.clicked.connect(self.accept)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(72, 28)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton { background-color: #E2E8F0; color: #1E293B; border: 1px solid #CBD5E1; border-radius: 3px; }
            QPushButton:hover { background-color: #CBD5E1; }
        """)
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
# Toolbar Widget
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
            self.create_btn.setStyleSheet("""
                QPushButton { background-color: #E5E7EB; color: #1F2937; border: 1px solid #9CA3AF; border-radius: 3px; padding: 0 8px; }
                QPushButton:hover { background-color: #D1D5DB; }
            """)
            if on_create_click:
                self.create_btn.clicked.connect(on_create_click)
            layout.addWidget(self.create_btn)

    def set_active_state(self, is_grid_active):
        if is_grid_active:
            self.grid_btn.setStyleSheet("QPushButton { background: #C4C4C4; border: 1px solid #888888; border-top-left-radius: 4px; border-bottom-left-radius: 4px; }")
            self.list_btn.setStyleSheet("QPushButton { background: #F0F0F0; border: 1px solid #B0B0B0; border-left: none; border-top-right-radius: 6px; border-bottom-right-radius: 6px; }")
        else:
            self.grid_btn.setStyleSheet("QPushButton { background: #F0F0F0; border: 1px solid #B0B0B0; border-top-left-radius: 4px; border-bottom-left-radius: 4px; }")
            self.list_btn.setStyleSheet("QPushButton { background: #C4C4C4; border: 1px solid #888888; border-left: none; border-top-right-radius: 6px; border-bottom-right-radius: 6px; }")


# -------------------------------------------------------------
# Views & Main Application Container
# -------------------------------------------------------------
class CredentialDesignEditorView(QWidget):
    def __init__(self, on_close_callback=None):
        super().__init__()
        self.setStyleSheet("background-color: #EFEFEF;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar & Content
        editor_toolbar = QFrame()
        editor_toolbar.setFixedHeight(38)
        editor_toolbar.setStyleSheet("background-color: #E2E8F0; border-bottom: 1px solid #CBD5E1;")
        tb_layout = QHBoxLayout(editor_toolbar)
        tb_layout.setContentsMargins(8, 2, 8, 2)
        
        tools = ["↩", "↪", "|", "📋", "✂", "🗑", "|", "T", "T", "👤", "📷"]
        for tool in tools:
            if tool == "|":
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                tb_layout.addWidget(line)
            else:
                btn = QToolButton()
                btn.setText(tool)
                btn.setFixedSize(26, 26)
                tb_layout.addWidget(btn)

        tb_layout.addStretch()
        main_layout.addWidget(editor_toolbar)

        # Card Canvas Area
        canvas_container = QWidget()
        canvas_container.setStyleSheet("background-color: #B3B3B3;")
        canvas_layout = QHBoxLayout(canvas_container)
        
        front_card_bg = QFrame()
        front_card_bg.setFixedSize(300, 380)
        front_card_bg.setStyleSheet("background-color: #FFFFFF; border-radius: 8px;")
        canvas_layout.addWidget(front_card_bg)
        
        main_layout.addWidget(canvas_container, stretch=1)

        # Bottom Bar
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


class GenericWorkspace(QWidget):
    def __init__(self, title_text="Workspace", show_create=False, default_grid_active=True, on_create_click=None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.toolbar = ViewToggleToolbar(
            on_grid_click=lambda: self.view_stack.setCurrentIndex(0),
            on_list_click=lambda: self.view_stack.setCurrentIndex(1),
            is_grid_active=default_grid_active,
            show_create_btn=show_create,
            on_create_click=on_create_click
        )
        layout.addWidget(self.toolbar)

        self.view_stack = QStackedWidget()
        lbl1 = QLabel(f"⬚ {title_text} - Grid")
        lbl2 = QLabel(f"☰ {title_text} - List")
        self.view_stack.addWidget(lbl1)
        self.view_stack.addWidget(lbl2)
        layout.addWidget(self.view_stack, stretch=1)


class EntrustDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.current_title = "Credential Design 1"
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top Navigation
        top_bar = QFrame()
        top_bar.setFixedHeight(48)
        top_layout = QHBoxLayout(top_bar)
        top_layout.addWidget(QLabel("<b>ENTRUST Adaptive Issuance™</b>"))
        top_layout.addStretch()

        btn_design = QPushButton("Design")
        btn_design.clicked.connect(self.open_editor_view)
        top_layout.addWidget(btn_design)
        main_layout.addWidget(top_bar)

        # Purple Bar
        self.purple_bar = QFrame()
        self.purple_bar.setFixedHeight(34)
        self.purple_bar.setStyleSheet("background-color: #7B0082;")
        self.purple_layout = QHBoxLayout(self.purple_bar)
        main_layout.addWidget(self.purple_bar)

        # Content Views
        self.design_stack = QStackedWidget()
        self.editor_page = CredentialDesignEditorView(on_close_callback=self.close_editor_view)
        self.design_stack.addWidget(self.editor_page)
        main_layout.addWidget(self.design_stack, stretch=1)

        self.update_purple_bar_title()

    def update_purple_bar_title(self):
        while self.purple_layout.count() > 0:
            item = self.purple_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.title_lbl = QLabel(self.current_title)
        self.title_lbl.setFont(QFont("Arial", 11, QFont.Bold))
        self.title_lbl.setStyleSheet("color: #FFFFFF; padding-left: 10px;")

        edit_icon_btn = QPushButton("✏ Edit Properties")
        edit_icon_btn.setFixedHeight(24)
        edit_icon_btn.setCursor(Qt.PointingHandCursor)
        edit_icon_btn.setStyleSheet("background-color: #E2E8F0; color: #1E293B; border-radius: 3px; font-weight: bold;")
        edit_icon_btn.clicked.connect(self.show_edit_properties_dialog)

        self.purple_layout.addWidget(self.title_lbl)
        self.purple_layout.addSpacing(10)
        self.purple_layout.addWidget(edit_icon_btn)
        self.purple_layout.addStretch()

    def show_edit_properties_dialog(self):
        dialog = EditPropertiesDialog(current_name=self.current_title, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.current_title = dialog.get_updated_name()
            self.update_purple_bar_title()

    def open_editor_view(self):
        self.design_stack.setCurrentIndex(0)

    def close_editor_view(self):
        pass


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
