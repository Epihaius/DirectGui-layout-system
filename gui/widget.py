# Author: Epihaius
# Date: 2019-09-23
# Last revision: 2020-10-08
#
# This module contains wrapper classes for the DirectGui widgets.

from panda3d.core import *
from direct.gui.DirectGui import *
from .sizer import Sizer
from math import ceil


class Widget:

    _count = 0

    def __init__(self, dgui_obj):

        self._type = "widget"
        self.dgui_obj = dgui_obj
        self._sizer = None
        # the SizerCell this widget is inside of
        self.sizer_cell = None

        l, r, b, t = self._bounds = self._get_bounds(dgui_obj)

        sx, _, sz = dgui_obj.get_scale()
        w = int((r - l) * sx)
        h = int((t - b) * sz)
        self._size = self._min_size = (w, h)

        self.guiId = "widget_{}".format(Widget._count)
        Widget._count += 1

        # provide camelCase aliases for DirectGui-like method names
        self.resetFrameSize = self.reset_frame_size

    def destroy(self):

        if not self.dgui_obj:
            return

        if self._sizer:
            self._sizer.destroy()
            self._sizer = None

        self.sizer_cell = None
        self.dgui_obj.destroy()
        self.dgui_obj = None

    def __getitem__(key):

        if key == "guiId":
            return self.guiId

    def __setitem__(self, key, value):

        if key == "guiId":
            self.guiId = value

    @property
    def type(self):

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

    @property
    def sizer(self):

        return self._sizer

    @sizer.setter
    def sizer(self, sizer):

        if sizer:
            sizer.owner = self

        self._sizer = sizer

    @property
    def min_size(self):

        return self._sizer.min_size if self._sizer else self._min_size

    @min_size.setter
    def min_size(self, size):

        self._min_size = w_min, h_min = size
        w, h = self._size
        self._size = (max(w_min, w), max(h_min, h))

        if self._sizer:
            self._sizer.set_min_size_stale()
        elif self.sizer_cell:
            self.sizer_cell.sizer.set_min_size_stale()

    def get_size(self):

        return self._sizer.get_size() if self._sizer else self._size

    def set_size(self, size):

        width, height = size
        w_min, h_min = self.min_size
        w_new = max(w_min, width)
        h_new = max(h_min, height)
        new_size = (w_new, h_new)
        sx, _, sz = self.dgui_obj.get_scale()
        l, r, b, t = self._bounds

        if self.dgui_obj["relief"] not in (None, DGG.FLAT):
            border_w, border_h = self.dgui_obj["borderWidth"]
        else:
            border_w = border_h = 0

        if self.dgui_obj.hascomponent("text0"):

            text_node = self.dgui_obj.component("text0")
            l_offset = r_offset = 0

            if self.dgui_obj.hascomponent("indicator"):

                l_b, r_b, b_b, t_b = self.dgui_obj.indicator.guiItem.getFrame()
                offset = r_b - l_b

                if self.dgui_obj["boxPlacement"] == "left":
                    l_offset = offset
                else:
                    r_offset = offset

            if text_node.align == TextNode.A_center:
                l = (-w_new / sx - l_offset + r_offset) * .5
                r = (w_new / sx - l_offset + r_offset) * .5
            elif text_node.align == TextNode.A_right:
                text_np = NodePath(text_node)
                _, p = text_np.get_tight_bounds()
                r = p[0] + border_w + r_offset
                l = r - w_new / sx
            elif text_node.align == TextNode.A_left:
                l = -border_w - l_offset
                r = l + w_new / sx

        else:

            l = 0.
            r = w_new / sx

        b = t - h_new / sz

        self._bounds = (l, r, b, t)

        if self.dgui_obj.hascomponent("indicator"):
            l += border_w
            r -= border_w
            b += border_h
            t -= border_h

        self.dgui_obj["frameSize"] = (l, r, b, t)

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

    def reset_frame_size(self):

        self.dgui_obj["frameSize"] = None
        self.dgui_obj.resetFrameSize()
        l, r, b, t = self._bounds = self._get_bounds(self.dgui_obj)
        sx, _, sz = self.dgui_obj.get_scale()
        w = int((r - l) * sx)
        h = int((t - b) * sz)
        self.min_size = (w, h)


class ScrolledListWidget(Widget):

    def __init__(self, dgui_obj, scrollbtn_proportion, scrollbtn_borders,
                 itemframe_borders, margins):

        Widget.__init__(self, dgui_obj)

        sizer = Sizer("vertical")
        self.sizer = sizer

        dec_sizer = Sizer("horizontal")
        sizer.add(dec_sizer)
        widget = Widget(dgui_obj.decButton)
        dec_sizer.add((0, 0), proportions=(.5, 0.))
        dec_sizer.add(widget, (scrollbtn_proportion, 0.), borders=scrollbtn_borders)
        dec_sizer.add((0, 0), proportions=(.5, 0.))

        frame_widget = Widget(dgui_obj.itemFrame)
        sizer.add(frame_widget, proportions=(1., 1.), borders=itemframe_borders)

        inc_sizer = Sizer("horizontal")
        sizer.add(inc_sizer)
        widget = Widget(dgui_obj.incButton)
        inc_sizer.add((0, 0), proportions=(.5, 0.))
        inc_sizer.add(widget, (scrollbtn_proportion, 0.), borders=scrollbtn_borders)
        inc_sizer.add((0, 0), proportions=(.5, 0.))

        self._list_sizer = sizer = Sizer("vertical")
        frame_widget.sizer = sizer
        self._item_root = DirectFrame(parent=dgui_obj.itemFrame)
        self._root_widget = widget = Widget(self._item_root)
        sizer.add((0, dgui_obj["forceHeight"]))
        l, r = margins
        borders = (l, r, 0, 0)
        sizer.add(widget, proportions=(1., 0.), borders=borders)
        sizer.add((0, dgui_obj["forceHeight"]))

        self._widgets = {}
        self._item_sizer = Sizer("vertical")
        self._item_sizer.set_column_proportion(0, 1.)

        # provide camelCase aliases for DirectGui-like method names
        self.addItem = self.add_item
        self.removeItem = self.remove_item

    def add_item(self, item, refresh=False, expand=True):

        w_min, h_min = self._item_sizer.min_size
        self.dgui_obj.addItem(item, refresh)
        item_parent = self._item_root.attach_new_node("item_parent")
        item.reparent_to(item_parent)
        widget = Widget(item)
        self._widgets[item] = widget
        alignments = ("expand" if expand else "min", "min")
        self._item_sizer.add(widget, alignments=alignments, index=0)
        max_width, _ = size = self._item_sizer.update_min_size()
        self._item_sizer.update(size)
        w, h = widget.get_size()
        w_ = int(w * .5)
        l, r, b, t = item["frameSize"]
        item["frameSize"] = (-w_, w_, b, t)

        if max_width > w_min:
            self._item_root["frameSize"] = (-w_, w_, 0, 0)
            self._root_widget._bounds = (-w_, w_, 0, 0)
            self._root_widget.min_size = (w, 0)

    def remove_item(self, item, refresh=False):

        item.get_parent().detach_node()
        w_min, h_min = self._item_sizer.min_size
        widget = self._widgets[item]
        sizer_cell = widget.sizer_cell
        widget.sizer_cell = None
        del self._widgets[item]
        self._item_sizer.remove_cell(sizer_cell)
        max_width, _ = size = self._item_sizer.update_min_size()
        self._item_sizer.update(size)

        if w_min > max_width:
            w_ = int(max_width * .5)
            self._item_root["frameSize"] = (-w_, w_, 0, 0)
            self._root_widget._bounds = (-w_, w_, 0, 0)
            self._root_widget.min_size = (max_width, 0)
            self._list_sizer.set_min_size_stale()

        self.dgui_obj.removeItem(item, refresh)

    def set_size(self, size):

        new_size = Widget.set_size(self, size)

        w, h = self._list_sizer.get_size()
        w = self._item_root.getWidth()
        w_ = w * .5
        self._item_root["frameSize"] = (-w_, w_, 0, 0)
        self._root_widget._bounds = (-w_, w_, 0, 0)
        self._item_sizer.set_size((w, 0))

        for item in self._widgets:
            l, r, b, t = item["frameSize"]
            sx, _, sz = item.get_scale()
            w_ = int((r - l) * .5) / sx
            item.get_parent().set_x(-w_ - l)

        item_height = self.dgui_obj["forceHeight"]
        self.dgui_obj["numItemsVisible"] = int((h - item_height * .5) // item_height)
        self.dgui_obj.refresh()

        return new_size


class ScrolledFrameWidget(Widget):

    def __init__(self, dgui_obj, scroll_dir=""):

        Widget.__init__(self, dgui_obj)

        self.scroll_dir = scroll_dir
        self.canvas_sizer = Sizer("vertical")

    @property
    def min_size(self):

        w, h = self._min_size
        bar_width = self.dgui_obj["scrollBarWidth"]
        w_min = w if self.scroll_dir in ("", "horizontal") else w + bar_width
        h_min = h if self.scroll_dir in ("", "vertical") else h + bar_width
        self.canvas_sizer.default_size = (0, 0)
        w, h = self.canvas_sizer.update_min_size()
        w += 0 if self.scroll_dir in ("", "horizontal") else bar_width
        h += 0 if self.scroll_dir in ("", "vertical") else bar_width

        if self.scroll_dir in ("", "vertical"):
            w_min = max(w_min, w)
        if self.scroll_dir in ("", "horizontal"):
            h_min = max(h_min, h)

        if self.dgui_obj["relief"] not in (None, DGG.FLAT):
            border_w, border_h = self.dgui_obj["borderWidth"]
            w_min += int(ceil(border_w * 2))
            h_min += int(ceil(border_h * 2))

        if self.sizer_cell:
            self.sizer_cell.sizer.set_min_size_stale()

        return (w_min, h_min)

    def set_size(self, size):

        w, h = new_size = Widget.set_size(self, size)

        if self.dgui_obj["relief"] not in (None, DGG.FLAT):
            border_w, border_h = self.dgui_obj["borderWidth"]
            w -= int(ceil(border_w * 2))
            h -= int(ceil(border_h * 2))

        bar_width = self.dgui_obj["scrollBarWidth"]

        if self.scroll_dir in ("both", "vertical"):
            w -= bar_width

        if self.scroll_dir in ("both", "horizontal"):
            h -= bar_width

        self.canvas_sizer.default_size = (w, h)
        min_size = self.canvas_sizer.min_size
        self.canvas_sizer.update(min_size)
        w, h = self.canvas_sizer.get_size()
        self.dgui_obj["canvasSize"] = (0, w, -h, 0)

        return new_size
