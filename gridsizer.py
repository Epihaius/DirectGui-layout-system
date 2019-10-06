#!/usr/bin/env python

# Author: Epihaius
# Date: 2019-10-06
#
# This is a basic example of how to use the sizer-based GUI system.
# It specifically showcases the use of a GridSizer.

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
        title = "Panda3D: grid sizer layout example"
        label = DirectLabel(parent=gui_root, text=title, frameSize=(0, 0, -20, 30),
            text_scale=20, borderWidth=(6, 6), relief=DGG.SUNKEN)
        widget = Widget(label)
        borders = (10, 10, 20, 10)
        gui.sizer.add(widget, expand=True, borders=borders)

        # add a grid sizer that will be proportionately resized vertically and
        # expanded horizontally;
        # setting rows to 0 and columns to 3 will horizontally add up to 3 items
        # to the sizer; a new row will automatically be created when a 4th item
        # is added; to add items vertically to a grid sizer, set the rows parameter
        # to a non-zero number and columns to zero
        sizer = GridSizer(rows=0, columns=3, gap_h=20, gap_v=10)
        borders = (10, 10, 20, 10)
        gui.sizer.add(sizer, proportion=1., expand=True, borders=borders)

        # add a first row of empty spaces, some of which are resized proportionately
        # in the horizontal direction, to force those proportions onto the
        # corresponding sizer columns
        sizer.add((0, 0))
        sizer.add((0, 0), proportion_h=2.)
        sizer.add((0, 0), proportion_h=1.)

        button = DirectButton(parent=gui_root, text="Item0", text_scale=20,
            borderWidth=(2, 2))
        widget = Widget(button)
        sizer.add(widget, resize_h=True, resize_v=True)
        button = DirectButton(parent=gui_root, text="Item1", text_scale=20,
            borderWidth=(2, 2))
        widget = Widget(button)
        sizer.add(widget, resize_h=True, proportion_v=1.)
        button = DirectButton(parent=gui_root, text="Item2", text_scale=20,
            borderWidth=(2, 2))
        widget = Widget(button)
        sizer.add(widget, alignment_h="right", alignment_v="center_v")

        def remove_button():

            sizer.remove_item(widget_to_remove.sizer_item, destroy=True)
            gui.layout()

        button = DirectButton(parent=gui_root, text="Another item: Item3", text_scale=20,
            borderWidth=(2, 2))
        widget = Widget(button)
        sizer.add(widget, resize_h=True, alignment_v="center_v")
        button = DirectButton(parent=gui_root, text="Remove me", text_scale=20,
            borderWidth=(2, 2), command=remove_button)
        widget_to_remove = Widget(button)
        sizer.add(widget_to_remove, alignment_h="center_h", alignment_v="bottom")
        button = DirectButton(parent=gui_root, text="Item5", text_scale=20,
            borderWidth=(2, 2))
        widget = Widget(button)
        sizer.add(widget, alignment_h="center_h", proportion_v=2.)

        # add a horizontally expanding status bar
        status_text = "GUI ready"
        label = DirectLabel(parent=gui_root, text=status_text, text_pos=(20, -10),
            textMayChange=1, frameSize=(0, 0, -10, 10), text_scale=20,
            text_align=TextNode.A_left)
        widget = Widget(label)
        borders = (10, 10, 10, 20)
        gui.sizer.add(widget, expand=True, borders=borders)

        # let the GUI system create the layout
        gui.layout()

        # run the app
        showbase.run()


MyApp()
