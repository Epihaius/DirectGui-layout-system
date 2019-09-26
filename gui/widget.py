# Author: Epihaius
# Date: 2019-09-23
#
# This module contains the Widget wrapper class for all DirectGui widgets.

from panda3d.core import *


class Widget:

    def __init__(self, dgui_obj, stretch_dir=""):

        self._type = "widget"
        self.dgui_obj = dgui_obj
        self._stretch_dir = stretch_dir  # "horizontal", "vertical", "both" or ""
        self._sizer = None
        self._sizer_item = None

        l1, r1, b1, t1 = self.dgui_obj.getBounds()
        l2, r2, b2, t2 = self.dgui_obj.guiItem.getFrame()
        l = min(l1, l2)
        r = max(r1, r2)
        b = min(b1, b2)
        t = max(t1, t2)
        self._bounds = l, r, b, t

        sx, _, sz = self.dgui_obj.get_scale()
        w = (r - l) * sx
        h = (t - b) * sz
        self._size = self._default_size = self._min_size = (int(w), int(h))

    def destroy(self):

        if not self.dgui_obj:
            return

        if self._sizer:
            self._sizer.destroy()
            self._sizer = None

        self._sizer_item = None
        self.dgui_obj.destroy()
        self.dgui_obj = None

    def get_type(self):

        return self._type

    def get_pos(self):

        x, _, z = self.dgui_obj.get_pos()
        y = -z

        return (int(x), int(y))

    def set_pos(self, pos):

        x, z = pos
        sx, _, sz = self.dgui_obj.get_scale()
        l, r, b, t = self._bounds
        self.dgui_obj.set_pos(x - l * sx, 0., -z - t * sz)

    def get_sizer(self):

        return self._sizer

    def set_sizer(self, sizer):

        if sizer:
            sizer.set_owner(self)

        self._sizer = sizer

    def get_sizer_item(self):

        return self._sizer_item

    def set_sizer_item(self, sizer_item):

        self._sizer_item = sizer_item

    def get_stretch_dir(self):

        return self._stretch_dir

    def get_min_size(self):

        return self._sizer.get_min_size() if self._sizer else self._min_size

    def get_default_size(self):

        return self._default_size

    def get_size(self):

        return self._sizer.get_size() if self._sizer else self._size

    def set_size(self, size):

        width, height = size
        w_def, h_def = self._default_size
        width, height = max(w_def, width), max(h_def, height)
        w_min, h_min = self.get_min_size()
        w_new, h_new = max(w_min, width), max(h_min, height)

        new_size = (w_new, h_new)
        sx, _, sz = self.dgui_obj.get_scale()
        l, r, b, t = self._bounds

        if self.dgui_obj.hascomponent("text0"):

            text_node = self.dgui_obj.component("text0")

            if text_node.align == TextNode.A_center:
                l = -w_new / sx * .5
                r = w_new / sx * .5
            elif text_node.align == TextNode.A_right:
                text_np = NodePath(text_node)
                _, p = text_np.get_tight_bounds()
                r = p[0]
                l = r - w_new / sx
            elif text_node.align == TextNode.A_left:
                l = 0.
                r = w_new / sx

        else:

            l = 0.
            r = w_new / sx

        b = t - h_new / sz
        self.dgui_obj["frameSize"] = self._bounds = (l, r, b, t)

        if self.dgui_obj.hascomponent("popupMarker"):
            marker = self.dgui_obj.component("popupMarker")
            sx = marker.get_scale()[0]
            b = self.dgui_obj["popupMarkerBorder"][0]
            z = marker.get_pos()[2]
            marker.set_pos(r - marker.getWidth() * .5 * sx - b, 0, z)

        if self._sizer:
            self._sizer.set_size(new_size)

        self._size = new_size

        return new_size
