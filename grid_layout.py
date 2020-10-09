#!/usr/bin/env python

# Author: Epihaius
# Date: 2019-10-06
# Last revision: 2020-10-08
#
# This is a basic example of how to use the sizer-based GUI system.
# It specifically showcases the growth of a Sizer in two directions.
# Cells are always added in a specific "primary" direction, which is
# either horizontal or vertical. However, by specifying a non-zero
# limit to the number of cells that can be added this way, the number
# of cells exceeding this limit are added to additional rows (if the
# primary direction is horizontal) or columns, resulting in a grid-like
# layout of its cells.

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from gui import *


class MyApp:

    def __init__(self):

        # initialize the Panda3D showbase
        self.showbase = showbase = ShowBase()

        # the root node of all DirectGui widgets needs to be pixel2d in order to work
        # with the automatic layout system
        self.gui_root = gui_root = showbase.pixel2d

        # initialize the GUI system
        self.gui = gui = GUI(showbase)

        # Build the GUI layout

        # add a horizontally expanding title bar
        title = "Panda3D: grid layout example"
        label = DirectLabel(parent=gui_root, text=title, frameSize=(0, 0, -20, 30),
            text_scale=20, borderWidth=(6, 6), relief=DGG.SUNKEN)
        widget = Widget(label)
        borders = (10, 10, 20, 10)
        # by default, the title bar will take up all of the width and height of its
        # cell (the default value for the `alignments` parameter of the `Sizer.add`
        # method is `("expand", "expand")`), but the cell itself still needs to be
        # able to take up the entire width of the window; this is done by setting
        # the horizontal proportion (which gets applied to the cell's column) to a
        # value bigger than zero
        gui.sizer.add(widget, proportions=(1., 0.), borders=borders)

        # add a horizontal sizer that will be expanded vertically and horizontally;
        # setting `prim_limit` to 3 will horizontally add up to 3 cells to the sizer;
        # a new row will automatically be created when a 4th object is added, resulting
        # in a grid-like layout
        sizer = Sizer("horizontal", prim_limit=3, gaps=(20, 10))
        borders = (10, 10, 0, 0)
        gui.sizer.add(sizer, proportions=(1., 1.), borders=borders)

        # set explicit horizontal proportions for some of the sizer columns
        sizer.set_column_proportion(1, 2.)
        sizer.set_column_proportion(2, 1.)

        def clear_proportions():

            sizer.clear_proportions()
            gui.layout()

        text = "Clear explicit proportions"
        button = DirectButton(parent=gui_root, text=text, text_wordwrap=6.,
            text_scale=20, borderWidth=(2, 2), command=clear_proportions)
        widget = Widget(button)
        sizer.add(widget)

        def toggle_column1_proportion():

            if sizer.has_column_proportion(1):
                sizer.clear_column_proportion(1)
            else:
                sizer.set_column_proportion(1, 2.)

            gui.layout()

        text = "Toggle explicit column proportion"
        button = DirectButton(parent=gui_root, text=text, text_wordwrap=5.,
            text_scale=20, borderWidth=(2, 2), command=toggle_column1_proportion)
        widget = Widget(button)
        sizer.add(widget, proportions=(0., 1.))

        def toggle_column2_proportion():

            if sizer.has_column_proportion(2):
                sizer.clear_column_proportion(2)
            else:
                sizer.set_column_proportion(2, 1.)

            gui.layout()

        text = "Toggle explicit column proportion"
        button = DirectButton(parent=gui_root, text=text, text_wordwrap=5.,
            text_scale=15, borderWidth=(2, 2), command=toggle_column2_proportion)
        widget = Widget(button)
        sizer.add(widget, alignments=("max", "center"))

        def toggle_new_button():

            if self.new_widget:
                sizer.remove_cell(self.new_widget.sizer_cell, destroy=True)
                self.new_widget = None
                toggler["text"] = "Insert n00b button"
                toggler.resetFrameSize()
            else:
                text = ("Hi, I'm new!", "But how?", "What's up?", "*Snooore*")
                button = DirectButton(parent=gui_root, text=text, text_scale=20,
                    borderWidth=(2, 2))
                self.new_widget = Widget(button)
                sizer.add(self.new_widget, alignments=("center", "max"), index=-1)
                toggler["text"] = "Remove n00b button"
                toggler.resetFrameSize()

            toggler_widget.resetFrameSize()
            gui.layout()

        toggler = DirectButton(parent=gui_root, text="Insert n00b button", text_scale=20,
            textMayChange=True, borderWidth=(2, 2), command=toggle_new_button)
        toggler_widget = Widget(toggler)
        sizer.add(toggler_widget, alignments=("expand", "center"))
        self.new_widget = None

        def toggle_row_proportion():

            if sizer.has_row_proportion(1):
                sizer.clear_row_proportion(1)
            else:
                sizer.set_row_proportion(1, 3.)

            gui.layout()

        text = "Toggle explicit row proportion"
        button = DirectButton(parent=gui_root, text=text, text_wordwrap=5.,
            text_scale=20, borderWidth=(2, 2), command=toggle_row_proportion)
        widget = Widget(button)
        sizer.add(widget, proportions=(0., 2.), alignments=("center", "expand"))
        # set an explicit vertical proportion for the bottom sizer row; it overrides
        # the vertical proportions associated with any cells of that row (in this
        # case, the proportion associated with the cell containing the last button added)
        sizer.set_row_proportion(1, 3.)

        # add a horizontally expanding status bar
        status_text = "GUI ready"
        label = DirectLabel(parent=gui_root, text=status_text, text_pos=(20, -10),
            textMayChange=1, frameSize=(0, 0, -10, 10), text_scale=20,
            text_align=TextNode.A_left)
        widget = Widget(label)
        borders = (10, 10, 10, 20)
        gui.sizer.add(widget, proportions=(1., 0.), borders=borders)

        # let the GUI system create the layout
        gui.layout()

        # run the app
        showbase.run()


MyApp()
