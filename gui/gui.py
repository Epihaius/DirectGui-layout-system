# Author: Epihaius
# Date: 2019-09-23
#
# This package contains code to create an automatic GUI layout system.

from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from .sizer import Sizer


class GUI:

    def __init__(self, showbase):

        self._showbase = showbase
        listener = DirectObject()
        listener.accept("window-event", self.__handle_window_event)
        self.sizer = Sizer("vertical")

    def layout(self):

        win_props = self._showbase.win.get_properties()
        w = win_props.get_x_size()
        h = win_props.get_y_size()
        self._window_size = (w, h)
        self.sizer.update((w, h))

    def __handle_window_event(self, window):

        win_props = window.get_properties()
        w, h = max(1, win_props.get_x_size()), max(1, win_props.get_y_size())

        if self._window_size != (w, h):

            self._window_size = (w, h)
            win_props = WindowProperties()
            win_props.set_size(w, h)
            window.request_properties(win_props)

            w_min, h_min = self.sizer.update_min_size()

            if w < w_min:
                w = w_min

            if h < h_min:
                h = h_min

            self.sizer.update((w, h))
