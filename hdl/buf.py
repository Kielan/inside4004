from hdl import *


class buf(sensor):
    def __init__(self, i, o, name=""):
        sensor.__init__(self, name, i)
        self._i = i
        self._o = o

    def i(self):
        return self._i

    def o(self):
        return self._o

    def always(self):
        self._o.v(self._i.v())
