# Author: Epihaius
# Date: 2019-09-23
#
# This module contains wrapper classes for the DirectGui widgets.

from panda3d.core import *
from direct.gui.DirectGui import *
from .sizer import Sizer


class Widget:

    def __init__(self, dgui_obj, stretch_dir=""):

        self._type = "widget"
        self.dgui_obj = dgui_obj
        self._stretch_dir = stretch_dir  # "horizontal", "vertical", "both" or ""
        self._sizer = None
        self._sizer_item = None

        l, r, b, t = self._get_bounds(dgui_obj)
        self._bounds = l, r, b, t

        sx, _, sz = dgui_obj.get_scale()
        w = (r - l) * sx
        h = (t - b) * sz
        self._size = self._min_size = (int(w), int(h))

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

    def _get_bounds(self, dgui_obj):

        l1, r1, b1, t1 = dgui_obj.getBounds()
        l2, r2, b2, t2 = dgui_obj.guiItem.getFrame()
        l = min(l1, l2)
        r = max(r1, r2)
        b = min(b1, b2)
        t = max(t1, t2)

        return (l, r, b, t)

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

    def set_min_size(self, size):
        
        self._min_size = w_min, h_min = size
        w, h = self._size
        self._size = (max(w_min, w), max(h_min, h))

        if self._sizer:
            self._sizer.set_min_size_stale()
            self._sizer.update_min_size()
            self._sizer.set_size(self._size)

    def get_size(self):

        return self._sizer.get_size() if self._sizer else self._size

    def set_size(self, size):

        width, height = size
        w_min, h_min = w_new, h_new = self.get_min_size()

        if self._stretch_dir in ("both", "horizontal"):
            w_new = max(w_min, width)

        if self._stretch_dir in ("both", "vertical"):
            h_new = max(h_min, height)

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


class ScrolledListWidget(Widget):

    def __init__(self, dgui_obj, stretch_dir, scrollbtn_proportion, scrollbtn_borders,
                 itemframe_borders, margins):

        Widget.__init__(self, dgui_obj, stretch_dir)

        sizer = Sizer("vertical")
        self.set_sizer(sizer)

        dec_sizer = Sizer("horizontal")
        sizer.add(dec_sizer, expand=True)
        widget = Widget(dgui_obj.decButton, "horizontal")
        dec_sizer.add((0, 0), proportion=.5)
        dec_sizer.add(widget, proportion=scrollbtn_proportion, borders=scrollbtn_borders)
        dec_sizer.add((0, 0), proportion=.5)

        frame_widget = Widget(dgui_obj.itemFrame, stretch_dir)
        sizer.add(frame_widget, expand=True, proportion=1., borders=itemframe_borders)

        inc_sizer = Sizer("horizontal")
        sizer.add(inc_sizer, expand=True)
        widget = Widget(dgui_obj.incButton, "horizontal")
        inc_sizer.add((0, 0), proportion=.5)
        inc_sizer.add(widget, proportion=scrollbtn_proportion, borders=scrollbtn_borders)
        inc_sizer.add((0, 0), proportion=.5)

        self._list_sizer = sizer = Sizer("vertical")
        frame_widget.set_sizer(sizer)
        self._item_root = DirectFrame(parent=dgui_obj.itemFrame)
        self._root_widget = widget = Widget(self._item_root, "horizontal")
        sizer.add((0, dgui_obj["forceHeight"]))
        l, r = margins
        borders = (l, r, 0, 0)
        sizer.add(widget, expand=True, borders=borders)
        sizer.add((0, dgui_obj["forceHeight"]))

        self._stretching_items = []
        self._item_widths = {None: 0}

        # provide camelCase aliases for method names
        self.addItem = self.add_item
        self.removeItem = self.remove_item

    def add_item(self, item, refresh=True, stretch=True):

        self.dgui_obj.addItem(item, refresh)
        item.reparent_to(self._item_root)

        l, r, b, t = self._get_bounds(item)
        w = (r - l) * item.get_scale()[0]
        w_ = int(w * .5)
        max_width = max(self._item_widths.values())
        self._item_widths[item] = w

        if stretch:
            item["frameSize"] = (l, r, b, t)
            self._stretching_items.append(item)

        if w > max_width:
            self._item_root["frameSize"] = (-w_, w_, 0, 0)
            self._root_widget._bounds = (-w_, w_, 0, 0)
            self._root_widget.set_min_size((w, 0))

    def remove_item(self, item, refresh=True):

        w = self._item_widths[item]
        del self._item_widths[item]
        max_width = max(self._item_widths.values())
        w_ = int(max_width * .5)

        if item in self._stretching_items:
            self._stretching_items.remove(item)

        if w > max_width:
            self._item_root["frameSize"] = (-w_, w_, 0, 0)
            self._root_widget._bounds = (-w_, w_, 0, 0)
            self._root_widget.set_min_size((max_width, 0))
            self._list_sizer.set_min_size_stale()

        self.dgui_obj.removeItem(item, refresh)

    def set_size(self, size):

        new_size = Widget.set_size(self, size)

        w, h = self._list_sizer.get_size()
        w = self._item_root.getWidth()
        w_ = w * .5
        self._item_root["frameSize"] = (-w_, w_, 0, 0)
        self._root_widget._bounds = (-w_, w_, 0, 0)

        for item in self._stretching_items:
            l, r, b, t = item["frameSize"]
            sx = item.get_scale()[0]
            w_ = int(w * .5) / sx
            l = -w_
            r = w_
            item["frameSize"] = (l, r, b, t)

        item_height = self.dgui_obj["forceHeight"]
        self.dgui_obj["numItemsVisible"] = int((h - item_height * .5) // item_height)
        self.dgui_obj.refresh()

        return new_size
