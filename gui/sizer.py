# Author: Epihaius
# Date: 2019-09-23
#
# This module contains classes to implement a "sizer" system, the purpose of
# which is to maintain the layout of widgets when resizing the window.

from panda3d.core import *


class SizerItem:

    def __init__(self, sizer, obj, obj_type, proportion=0., expand=False,
                 alignment="", borders=None):

        self._sizer = sizer
        self._obj = obj
        self._type = obj_type
        self.proportion = proportion
        self.expand = expand
        self.alignment = alignment

        if borders is None:
            outer_borders = (0, 0, 0, 0)
        else:
            outer_borders = borders

        l, r, b, t = self._borders = outer_borders
        self._obj_offset = (l, t)

        if obj_type == "size":
            w, h = obj
        else:
            w, h = obj.min_size

        w += l + r
        h += b + t
        self._size = self._min_size = (w, h)

        self._preserve_obj = False

    def destroy(self):

        self._sizer = None

        if not (self._preserve_obj or self._type == "size"):
            self._obj.destroy()

        self._obj = None
        self._type = ""
        self.proportion = 0
        self.expand = False
        self.alignment = ""
        self._borders = (0, 0, 0, 0)
        self._obj_offset = (0, 0)
        self._size = self._min_size = (0, 0)

    def __getitem__(key):

        if key == "proportion":
            return self.proportion
        elif key == "expand":
            return self.expand
        elif key == "alignment":
            return self.alignment
        elif key == "borders":
            return self.borders

    def __setitem__(self, key, value):

        if key == "proportion":
            self.proportion = value
        elif key == "expand":
            self.expand = value
        elif key == "alignment":
            self.alignment = value
        elif key == "borders":
            self.borders = value

    @property
    def sizer(self):

        return self._sizer

    @sizer.setter
    def sizer(self, sizer):

        self._sizer = sizer

        if self._type == "sizer":
            self._obj.owner = sizer

    @property
    def object(self):

        return self._obj

    @property
    def type(self):

        return self._type

    @property
    def borders(self):

        return self._borders

    @borders.setter
    def borders(self, borders):

        if borders is None:
            outer_borders = (0, 0, 0, 0)
        else:
            outer_borders = borders

        l, r, b, t = self._borders = outer_borders
        self._obj_offset = (l, t)

    @property
    def object_offset(self):

        return self._obj_offset

    @property
    def min_size(self):

        return self._min_size

    def update_min_size(self):

        if self._type == "size":
            w, h = self._obj
        if self._type == "sizer":
            w, h = self._obj.update_min_size()
        if self._type == "widget":
            w, h = self._obj.min_size

        l, r, b, t = self._borders
        w += l + r
        h += b + t
        self._min_size = (w, h)

        return self._min_size

    def get_size(self):

        return self._size

    def set_size(self, size):

        width, height = self._size = size
        x = y = 0
        l, r, b, t = self._borders

        if self._type != "size":

            width -= l + r
            height -= t + b
            x += l
            y += t
            grow_dir = self._sizer.grow_dir
            w, h = self._obj.min_size

            if grow_dir == "horizontal":
                if not self.expand:
                    if self.alignment == "bottom":
                        y += height - h
                    elif self.alignment == "center_v":
                        y += (height - h) // 2
            elif grow_dir == "vertical":
                if not self.expand:
                    if self.alignment == "right":
                        x += width - w
                    elif self.alignment == "center_h":
                        x += (width - w) // 2

            w_new, h_new = w, h

            if grow_dir == "horizontal":
                if self.proportion > 0.:
                    w_new = width
                if self.expand:
                    h_new = height
            elif grow_dir == "vertical":
                if self.proportion > 0.:
                    h_new = height
                if self.expand:
                    w_new = width

            new_size = (w_new, h_new)
            self._obj.set_size(new_size)

        self._obj_offset = (x, y)

    def preserve_object(self, preserve=True):

        self._preserve_obj = preserve


class Sizer:

    _count = 0

    def __init__(self, grow_dir):

        self._type = "sizer"
        self._sizer_type = "sizer"
        self.owner = None
        # the SizerItem this sizer is tracked by, in case it is a subsizer
        self.sizer_item = None
        self.grow_dir = grow_dir  # "horizontal" or "vertical"
        self._pos = (0, 0)
        # minimum size without any contents
        self._default_size = (0, 0)
        # minimum size needed to accommodate current contents, bigger than or
        # equal to default size
        self._min_size = (0, 0)
        self._is_min_size_stale = True
        # current size, bigger than or equal to minimum size needed for current
        # contents
        self._size = (0, 0)
        self._items = []

        self.guiId = "sizer_{}".format(Sizer._count)
        Sizer._count += 1

    def destroy(self):

        for item in self._items:
            item.destroy()

        self._items = []
        self.owner = None
        self.sizer_item = None

    def clear(self, destroy_items=False):

        if destroy_items:
            for item in self._items:
                item.destroy()

        self._items = []
        self.set_min_size_stale()

    def __getitem__(key):

        if key == "guiId":
            return self.guiId
        elif key == "grow_dir":
            return self.grow_dir
        elif key == "default_size":
            return self._default_size

    def __setitem__(self, key, value):

        if key == "guiId":
            self.guiId = value
        elif key == "grow_dir":
            self.grow_dir = value
        elif key == "default_size":
            self.set_default_size(value)

    @property
    def type(self):

        return self._type

    @property
    def sizer_type(self):

        return self._sizer_type

    def add(self, obj, proportion=0., expand=False, alignment="", borders=None, index=None):

        obj_type = "size" if type(obj) == tuple else obj.type
        item = SizerItem(self, obj, obj_type, proportion, expand, alignment, borders)

        if index is None:
            self._items.append(item)
        else:
            self._items.insert(index, item)

        self.set_min_size_stale()

        if obj_type == "sizer":
            obj.owner = self

        if obj_type != "size":
            obj.sizer_item = item

        return item

    def add_item(self, item, index=None):

        item.sizer = self

        if index is None:
            self._items.append(item)
        else:
            self._items.insert(index, item)

        self.set_min_size_stale()

    def remove_item(self, item, destroy=False):

        self._items.remove(item)
        item.sizer = None

        if destroy:
            item.destroy()

        self.set_min_size_stale()

    def get_item_index(self, item):

        return self._items.index(item)

    def get_item(self, index):

        return self._items[index]

    @property
    def items(self):

        return self._items

    def get_item_count(self):

        return len(self._items)

    def get_widgets(self, include_children=True):

        widgets = []

        for item in self._items:

            if item.type == "widget":

                widget = item.object
                widgets.append(widget)

                if include_children:

                    sizer = widget.sizer

                    if sizer:
                        widgets.extend(sizer.get_widgets())

            elif item.type == "sizer":

                widgets.extend(item.object.get_widgets(include_children))

        return widgets

    def get_pos(self):

        x, y = self._pos

        return (x, y)

    def set_pos(self, pos):

        self._pos = pos

    def get_default_size(self):

        return self._default_size

    def set_default_size(self, size):

        w_d, h_d = self._default_size = size
        w_min, h_min = self._min_size
        self._min_size = w_min, h_min = (max(w_d, w_min), max(h_d, h_min))
        w, h = self._size
        self._size = (max(w_min, w), max(h_min, h))

        if self.sizer_item:
            self.sizer_item.update_min_size()

        self.set_min_size_stale()

    def set_min_size_stale(self, stale=True):

        self._is_min_size_stale = stale

        if stale and self.owner:

            if self.owner.type == "sizer":

                self.owner.set_min_size_stale()

            elif self.owner.type == "widget":

                item = self.owner.sizer_item

                if item:

                    item_sizer = item.sizer

                    if item_sizer:
                        item_sizer.set_min_size_stale()

    @property
    def min_size(self):

        return self._min_size

    @min_size.setter
    def min_size(self, size):
        """
        Force the minimum size, ignoring default and actual sizes.
        Only use in very specific cases where the size is not supposed to change.

        """

        self._min_size = size
        self._is_min_size_stale = False

    def update_min_size(self):

        if not self._is_min_size_stale:
            return self._min_size

        width = height = 0

        for item in self._items:

            if item.type == "widget":

                sizer = item.object.sizer

                if sizer:
                    sizer.update_min_size()

            w, h = item.update_min_size()

            if self.grow_dir == "horizontal":
                width += w
            else:
                width = max(width, w)

            if self.grow_dir == "vertical":
                height += h
            else:
                height = max(height, h)

        w_d, h_d = self._default_size
        self._min_size = width, height = (max(w_d, width), max(h_d, height))
        self._is_min_size_stale = False
        w, h = self._size
        self._size = (max(width, w), max(height, h))

        return self._min_size

    def __check_proportions(self, items, total_size, sizes, dim):

        proportions = [i.proportion for i in items]
        p_sum = sum(proportions)
        tmp_size = total_size

        for item, proportion in zip(items, proportions):

            s_min = item.min_size[dim]
            s_new = int(round(tmp_size * proportion / p_sum))

            if s_new < s_min:
                items.remove(item)
                index = self._items.index(item)
                sizes[index] = s_min
                total_size -= s_min
                return True, total_size

            p_sum -= proportion
            tmp_size -= s_new

        return False, total_size

    def get_size(self):

        return self._size

    def set_size(self, size, force=False):

        if force:
            self._size = size
            return

        width, height = size
        w_min, h_min = size_min = list(self.min_size)
        self._size = (max(w_min, width), max(h_min, height))
        dim = 0 if self.grow_dir == "horizontal" else 1
        w_min, h_min = size_min
        width, height = (max(w_min, width), max(h_min, height))

        widths = heights = None

        if self.grow_dir == "horizontal":

            widths = [0] * len(self._items)
            sizer_items = self._items[:]

            for index, item in enumerate(self._items):

                proportion = item.proportion

                if proportion == 0.:
                    sizer_items.remove(item)
                    w_min = item.min_size[0]
                    width -= w_min
                    widths[index] = w_min

            check_proportions = True

            while check_proportions:
                check_proportions, width = self.__check_proportions(sizer_items,
                                                                    width, widths, 0)

            proportions = [i.proportion for i in sizer_items]
            p_sum = sum(proportions)
            sizer_items = [(i.min_size[0], i) for i in sizer_items]
            last_item = sizer_items.pop() if sizer_items else None

            for w_min, item in sizer_items:

                proportion = item.proportion
                index = self._items.index(item)
                w_new = int(round(width * proportion / p_sum))

                if w_new < w_min:
                    w_new = w_min

                p_sum -= proportion
                width -= w_new
                widths[index] = w_new

            if last_item:
                w_min, item = last_item
                index = self._items.index(item)
                widths[index] = width

        elif self.grow_dir == "vertical":

            heights = [0] * len(self._items)
            sizer_items = self._items[:]

            for index, item in enumerate(self._items):

                proportion = item.proportion

                if proportion == 0.:
                    sizer_items.remove(item)
                    h_min = item.min_size[1]
                    height -= h_min
                    heights[index] = h_min

            check_proportions = True

            while check_proportions:
                check_proportions, height = self.__check_proportions(sizer_items,
                                                                     height, heights, 1)

            proportions = [i.proportion for i in sizer_items]
            p_sum = sum(proportions)
            sizer_items = [(i.min_size[1], i) for i in sizer_items]
            last_item = sizer_items.pop() if sizer_items else None

            for h_min, item in sizer_items:

                proportion = item.proportion
                index = self._items.index(item)
                h_new = int(round(height * proportion / p_sum))

                if h_new < h_min:
                    h_new = h_min

                p_sum -= proportion
                height -= h_new
                heights[index] = h_new

            if last_item:
                h_min, item = last_item
                index = self._items.index(item)
                heights[index] = height

        if not (widths or heights):
            return

        if not widths:
            widths = [width] * len(self._items)

        if not heights:
            heights = [height] * len(self._items)

        for item, w, h in zip(self._items, widths, heights):
            item.set_size((w, h))

    def calculate_positions(self, start_pos=(0, 0)):

        x, y = start_x, start_y = start_pos

        for item in self._items:

            obj = item.object
            w, h = item.get_size()
            offset_x, offset_y = item.object_offset
            pos = (x + offset_x, y + offset_y)

            if item.type == "widget":

                obj.set_pos(pos)
                sizer = obj.sizer

                if sizer:
                    sizer.calculate_positions()

            elif item.type == "sizer":

                obj.set_pos(pos)
                obj.calculate_positions(pos)

            if self.grow_dir == "horizontal":
                x += w

            if self.grow_dir == "vertical":
                y += h

    def update(self, size=None):

        self.update_min_size()

        if size:
            self.set_size(size)
            self.calculate_positions()


class GridDataItem:

    def __init__(self, obj, proportion_h, proportion_v, resize_h, resize_v,
                 alignment_h, alignment_v, borders):

        self._data = (obj, proportion_h, proportion_v, resize_h, resize_v,
                      alignment_h, alignment_v, borders)

    def get_data(self):

        return self._data


class GridSizer(Sizer):

    def __init__(self, rows=0, columns=0, gap_h=0, gap_v=0):

        Sizer.__init__(self, "both")

        self._sizer_type = "grid_sizer"
        self._max_rows = rows
        self._max_cols = columns
        self._gaps = {"horizontal": gap_h, "vertical": gap_v}
        self._sizers = {"horizontal": Sizer("horizontal"), "vertical": Sizer("vertical")}
        self._data_items = []

    def destroy(self):

        self._items = []

        Sizer.destroy(self)

        self._sizers["horizontal"].destroy()
        self._sizers["vertical"].destroy()
        self._sizers = {}
        self._data_items = []

    def clear(self, destroy_items=False):

        self._items = []

        Sizer.clear(self, destroy_items)

        self._sizers["horizontal"].clear(destroy_items)
        self._sizers["vertical"].clear(destroy_items)
        self._data_items = []

    def __add_to_horizontal_sizer(self, obj, proportion=0., borders=None, index=None):

        # A horizontal help sizer is used to compute the widths of the columns,
        # especially important when horizontal proportions are needed.
        # The calculated width of a column is then set as the default width of
        # the corresponding outer cell sizers.

        gap = self._gaps["horizontal"]
        sizer = self._sizers["horizontal"]
        column_sizer_items = sizer.items
        column_count = len(column_sizer_items)

        if index is None:
            if column_count == 0:
                column_sizer = Sizer("vertical")
                sizer.add(column_sizer, expand=True)
            else:
                column_sizer = column_sizer_items[-1].object
                if column_sizer.get_item_count() == self._max_rows * 2 - 1:
                    sizer.add((gap, 0))
                    column_sizer = Sizer("vertical")
                    sizer.add(column_sizer, expand=True)
        elif index < column_count:
            column_sizer = column_sizer_items[index].object
        else:
            if index > 0:
                sizer.add((gap, 0))
            column_sizer = Sizer("vertical")
            sizer.add(column_sizer, expand=True)

        if column_sizer.items:
            column_sizer.add((0, 0))

        column_sizer.add(obj, borders=borders)

        column_sizer_item = column_sizer.sizer_item
        column_proportion = column_sizer_item.proportion
        # the column sizer should have the largest of the horizontal proportions that were passed
        # for its items; all of its items that should resize proportionally in the horizontal
        # direction will end up with the same width, as if they were all given that same largest
        # proportion
        column_proportion = max(column_proportion, proportion)
        column_sizer_item.proportion = column_proportion

    def __add_to_vertical_sizer(self, obj, proportion_h=0., proportion_v=0.,
                                resize_h=False, resize_v=False,
                                alignment_h="", alignment_v="",
                                borders=None, index=None):

        # Each object added to the vertical help sizer is wrapped in a nested "cell sizer", i.e.
        # a horizontal inner cell sizer inside a vertical outer cell sizer.
        # The outer cell sizer expands within its horizontal row sizer, while the inner cell sizer
        # is added with proportion=1. to the outer cell sizer.
        # No proportion needs to be set for an outer cell sizer, since its default width will be
        # set to the width of the corresponding column sizer of the horizontal help sizer, after
        # that one has been resized.
        # To resize the added object in the vertical direction, it needs to expand (the actual
        # proportion applied to the object is the one set on the row sizer).
        # To resize the added object in the horizontal direction, it needs a non-zero proportion
        # (any value will do; the actual proportion applied to the object is the one set on the
        # column sizer), while its inner cell sizer needs to expand.
        # To align the added object vertically, it simply needs to have the desired alignment set.
        # To align the added object horizontally, its inner cell sizer needs to have the desired
        # alignment set.

        gap_v = self._gaps["vertical"]
        gap_h = self._gaps["horizontal"]
        sizer = self._sizers["vertical"]
        row_sizer_items = sizer.items
        row_count = len(row_sizer_items)

        if index is None:
            if row_count == 0:
                row_sizer = Sizer("horizontal")
                sizer.add(row_sizer, expand=True)
            else:
                row_sizer = row_sizer_items[-1].object
                if row_sizer.get_item_count() == self._max_cols * 2 - 1:
                    sizer.add((0, gap_v))
                    row_sizer = Sizer("horizontal")
                    sizer.add(row_sizer, expand=True)
        elif index < row_count:
            row_sizer = row_sizer_items[index].object
        else:
            if index > 0:
                sizer.add((0, gap_v))
            row_sizer = Sizer("horizontal")
            sizer.add(row_sizer, expand=True)

        row_sizer_item = row_sizer.sizer_item
        row_proportion = row_sizer_item.proportion
        # the row sizer should have the largest of the vertical proportions that were passed for
        # its items; all of its items that should resize proportionally in the vertical direction
        # will end up with the same height, as if they were all given that same largest proportion
        row_proportion = max(row_proportion, proportion_v)
        row_sizer_item.proportion = row_proportion

        if row_sizer.items:
            row_sizer.add((gap_h, 0))

        outer_cell_sizer = Sizer("vertical")
        row_sizer.add(outer_cell_sizer, expand=True)
        inner_cell_sizer = Sizer("horizontal")
        expand = resize_h or proportion_h > 0.
        outer_cell_sizer.add(inner_cell_sizer, 1., expand, alignment_h)
        proportion = 1. if expand else 0.
        expand = resize_v or proportion_v > 0.

        return inner_cell_sizer.add(obj, proportion, expand, alignment_v, borders)

    def add(self, obj, proportion_h=0., proportion_v=0., resize_h=False, resize_v=False,
            alignment_h="", alignment_v="", borders=None, rebuilding=False):

        grow_dir = "vertical" if self._max_rows == 0 else "horizontal"

        if grow_dir == "vertical":
            item = self.__add_to_vertical_sizer(obj, proportion_h, proportion_v,
                                                resize_h, resize_v,
                                                alignment_h, alignment_v, borders)
        else:
            self.__add_to_horizontal_sizer(obj, proportion_h)

        index = self._sizers[grow_dir].items[-1].object.get_item_count() - 1

        if grow_dir == "vertical":
            self.__add_to_horizontal_sizer(obj, proportion_h, borders, index)
        else:
            item = self.__add_to_vertical_sizer(obj, proportion_h, proportion_v,
                                                resize_h, resize_v,
                                                alignment_h, alignment_v, borders, index)

        if item.type != "size":
            obj.sizer_item = item

        if not rebuilding:
            self._items.append(item)
            self._data_items.append(GridDataItem(obj, proportion_h, proportion_v,
                                                 resize_h, resize_v,
                                                 alignment_h, alignment_v, borders))

        Sizer.set_min_size_stale(self)

        return item

    def rebuild(self):

        sizer = self._sizers["horizontal"]

        for column_item in sizer.items[::2]:
            for item in column_item.object.items[::2]:
                item.preserve_object()

        sizer.destroy()

        sizer = self._sizers["vertical"]

        for row_item in sizer.items[::2]:
            for item in row_item.object.items[::2]:
                item.object.get_item(0).object.get_item(0).preserve_object()

        sizer.destroy()

        self._sizers = {"horizontal": Sizer("horizontal"), "vertical": Sizer("vertical")}

        for item in self._data_items:
            self.add(*item.get_data(), rebuilding=True)

    def add_item(self, item, index=None): pass

    def remove_item(self, item, destroy=False, rebuild=True):

        Sizer.set_min_size_stale(self)

        index = self._items.index(item)
        self._items.remove(item)
        del self._data_items[index]

        if destroy:
            item.destroy()

        if rebuild:
            self.rebuild()

    def get_widgets(self, include_children=True):

        return self._sizers["horizontal"].get_widgets(include_children)

    def set_pos(self, pos):

        Sizer.set_pos(self, pos)

        self._sizers["vertical"].set_pos(pos)

    def set_default_size(self, size):

        Sizer.set_default_size(self, size)

        self._sizers["horizontal"].set_default_size(size)
        self._sizers["vertical"].set_default_size(size)

    def set_min_size_stale(self, stale=True):

        Sizer.set_min_size_stale(self, stale)

        self._sizers["horizontal"].set_min_size_stale(stale)
        self._sizers["vertical"].set_min_size_stale(stale)

    def update_min_size(self):

        min_w = self._sizers["horizontal"].update_min_size()[0]
        min_h = self._sizers["vertical"].update_min_size()[1]
        min_size = (min_w, min_h)
        self.min_size = min_size

        return min_size

    def set_size(self, size, force=False):

        sizer_h = self._sizers["horizontal"]
        sizer_v = self._sizers["vertical"]

        # compute the widths of the column sizers
        sizer_h.set_size(size, force)

        row_sizers = [i.object for i in sizer_v.items[::2]]
        # retrieve the widths of the column sizers (the slice removes the horizontal gaps)
        widths = [i.get_size()[0] for i in sizer_h.items[::2]]

        for row_sizer in row_sizers:
            for cell_sizer_item, w in zip(row_sizer.items[::2], widths):
                cell_sizer_item.object.set_default_size((w, 0))

        sizer_v.set_size(size, force)

        new_size = sizer_v.get_size()
        Sizer.set_size(self, new_size, force=True)

    def calculate_positions(self, start_pos=(0, 0)):

        self._sizers["vertical"].calculate_positions(start_pos)
