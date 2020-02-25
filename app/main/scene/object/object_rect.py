from PyQt5.QtCore import QLineF

from app.base.widget.graphics import Rect
from app.utils import list_math


class ObjectRect(Rect):
    def draw(self):
        super().draw()
        p = self.painter
        x, y, w, h = self
        w2, h2 = list_math.divide([w, h], [2, 2])
        p.drawLines([
            QLineF(x + w2, y, x + w2, y + h),
            QLineF(x, y + h2, x + w, y + h2),
        ])
