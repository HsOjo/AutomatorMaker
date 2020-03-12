from PyQt5.QtCore import QLineF
from ojoqt.widget.graphics import Rect

from app.utils import list_math


class ObjectRect(Rect):
    def draw(self):
        super().draw()
        p = self.painter
        s = self.scale
        x, y, w, h = self
        w2, h2 = list_math.divide([w, h], [2, 2])
        l1 = list_math.multiply([x + w2, y, x + w2, y + h], [s, s, s, s])
        l2 = list_math.multiply([x, y + h2, x + w, y + h2], [s, s, s, s])
        l1 = [int(i) for i in l1]
        l2 = [int(i) for i in l2]
        p.drawLines([QLineF(*l1), QLineF(*l2)])
