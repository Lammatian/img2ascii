from PyQt5.QtWidgets import QWidgetAction

class PushButtonAction(QWidgetAction):
    def __init__(self, icon, text, parent=None):
        super(PushButtonAction, self).__init__(parent)
        self.setIcon(icon)
        self.setObjectName(text)
        self.setCheckable(True)

class BrushButtonAction(PushButtonAction):
    def __init__(self, icon, text, brush_size, parent=None):
        super(BrushButtonAction, self).__init__(icon, text, parent)
        self.brush_size = brush_size