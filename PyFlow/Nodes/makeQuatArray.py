from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node
from Qt.QtWidgets import QMenu
from ..Core.Pin import PinWidgetBase


class makeQuatArray(Node):
    def __init__(self, name, graph):
        super(makeQuatArray, self).__init__(name, graph)
        self.out0 = self.addOutputPin('quats', DataTypes.Array)
        self.menu = QMenu()
        self.action = self.menu.addAction('add input')
        self.action.triggered.connect(self.addInPin)

    def addInPin(self):
        p = self.addInputPin(str(len(self.inputs)), DataTypes.Quaternion)
        pinAffects(p, self.out0)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Quaternion], 'outputs': [DataTypes.Array]}

    @staticmethod
    def category():
        return 'GenericTypes'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'array of quaternions'

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)

        # restore dynamically created inputs
        for inp in jsonTemplate['inputs']:
            p = PinWidgetBase.deserialize(self, inp)
            pinAffects(p, self.out0)

    def compute(self):
        self.out0.setData(list([i.getData() for i in self.inputs.values()]))
