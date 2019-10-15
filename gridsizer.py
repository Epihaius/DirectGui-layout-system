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
        # is added;
        # to add items vertically to a grid sizer, set the rows parameter to a
        # non-zero number and columns to zero
        sizer = GridSizer(rows=0, columns=3, gap_h=20, gap_v=10)
        borders = (10, 10, 0, 0)
        gui.sizer.add(sizer, proportion=1., expand=True, borders=borders)

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
        sizer.add(widget, expand_h=True, expand_v=True)

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
        sizer.add(widget, expand_h=True, proportion_v=1.)

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
        sizer.add(widget, alignment_h="right", alignment_v="center_v")

        def toggle_new_button():

            if self.new_widget:
                sizer.remove_item(self.new_widget.sizer_item, destroy=True)
                self.new_widget = None
                toggler["text"] = "Insert n00b button"
                toggler.resetFrameSize()
            else:
                text = ("Hi, I'm new!", "But how?", "What's up?", "*Snooore*")
                button = DirectButton(parent=gui_root, text=text, text_scale=20,
                    borderWidth=(2, 2))
                self.new_widget = Widget(button)
                sizer.add(self.new_widget, alignment_h="center_h", alignment_v="bottom",
                index=-1)
                toggler["text"] = "Remove n00b button"
                toggler.resetFrameSize()

            toggler_widget.resetFrameSize()
            gui.layout()

        toggler = DirectButton(parent=gui_root, text="Insert n00b button", text_scale=20,
            textMayChange=True, borderWidth=(2, 2), command=toggle_new_button)
        toggler_widget = Widget(toggler)
        sizer.add(toggler_widget, expand_h=True, alignment_v="center_v")
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
        sizer.add(widget, alignment_h="center_h", proportion_v=2.)
        # set an explicit vertical proportion for the bottom sizer row; it overrides
        # the vertical proportions set on any item added to that row (in this case,
        # the proportion set on the last added button)
        sizer.set_row_proportion(1, 3.)

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
