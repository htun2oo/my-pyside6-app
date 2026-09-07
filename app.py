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
        self.grabMouse()
        self.update()

    def start_new_v_guide(self, global_x):
        local_x = self.mapFromGlobal(QPoint(global_x, 0)).x()
        self.v_guides.append(local_x)
        self.active_drag = len(self.v_guides) - 1
        self.drag_type = 'V'
        self.grabMouse()
        self.update()

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        for idx, y in enumerate(self.h_guides):
            if abs(pos.y() - y) <= 5:
                self.active_drag = idx
                self.drag_type = 'H'
                self.grabMouse()
                return
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

    # -------------------------------------------------------------
    # Card အဖြူရောင်ပေါ်တွင် Line များ ပေါ်လာစေရန် ပြင်ဆင်ထားသော PaintEvent
    # -------------------------------------------------------------
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiased)

        # 1. Active ဖြစ်နေသော Guideline (Photoshop Cyan Color: #00FFFF)
        photoshop_cyan = QPen(QColor("#00FFFF"), 1.5, Qt.SolidLine)
        painter.setPen(photoshop_cyan)

        # Card အပေါ်တွင် အပေါ်ဆုံးမှ ထပ်ဆွဲပေးခြင်း (Draw Guidelines on top of everything)
        for y in self.h_guides:
            if 0 <= y <= self.height():
                painter.drawLine(0, y, self.width(), y)

        for x in self.v_guides:
            if 0 <= x <= self.width():
                painter.drawLine(x, 0, x, self.height())
