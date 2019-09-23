#!/usr/bin/env python

# Author: Epihaius
# Date: 2019-09-23
#
# This is a basic example of how to use the sizer-based GUI system.

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
        gui_root = showbase.pixel2d

        # initialize the GUI system
        gui = GUI(showbase)

        # Build the GUI layout

        # add horizontally stretching title bar
        title = "Panda3D: GUI layout example"
        label = DirectLabel(parent=gui_root, text=title, text_align=TextNode.A_center,
            text_pos=(0, -.5), textMayChange=1, frameSize=(-10, 10, -.5, .5), scale=20)
        widget = Widget(label, "horizontal")
        borders = (10, 10, 20, 10)
        gui.add(widget, expand=True, borders=borders)

        # add a horizontal sizer that can stretch (expand) horizontally
        sizer = Sizer("horizontal")
        borders = (10, 10, 20, 10)
        gui.add(sizer, expand=True, borders=borders)

        # add a vertical, non-stretching subsizer to the previous sizer
        btn_sizer = Sizer("vertical")
        borders = (0, 20, 0, 0)
        sizer.add(btn_sizer, borders=borders)

        # add a couple of horizontally stretching buttons to the subsizer;
        # they will have the same width, determined by the initially largest button
        borders = (0, 0, 10, 0)
        text = "Button 1"
        button = DirectButton(parent=gui_root, text=text, scale=20)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True, borders=borders)
        text = "Another button"
        button = DirectButton(parent=gui_root, text=text, scale=20)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True)
        # add vertical space with a fixed size
        btn_sizer.add((0, 50))
        text = "A third button"
        button = DirectButton(parent=gui_root, text=text, scale=20)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True)

        # add some horizontally stretching space, so that widgets added after it
        # will be pushed to the right
        sizer.add((0, 0), proportion=1.)

        # add a frame stretching in both directions and taking up two thirds of
        # the available horizontal space (because of the ratio of the proportions
        # used for the frame and the stretching space that was previously added)
        frame = DirectFrame(parent=gui_root, frameColor=(.5, .6, .7, 1.))
        widget = Widget(frame, "both")
        sizer.add(widget, expand=True, proportion=2.)

        # assign a sizer to the frame to manage the layout of its child widgets
        frame_sizer = Sizer("vertical")
        widget.set_sizer(frame_sizer)

        # add some vertically stretching space to the frame, so that widgets added
        # after it will be pushed downwards
        frame_sizer.add((0, 0), proportion=1.)
        text = "Button in frame "
        button = DirectButton(parent=frame, text=text, scale=20)
        widget = Widget(button, "horizontal")
        borders = (0, 20, 10, 0)
        frame_sizer.add(widget, alignment="right", borders=borders)

        # add some vertically stretching space to the GUI, so that widgets added
        # after it will be pushed downwards
        gui.add((0, 0), proportion=1.)

        # add a non-stretching input field, centered horizontally
        field = DirectEntry(parent=gui_root, frameSize=(0, 10, -1, 1), scale=20, focus=1)
        widget = Widget(field)
        gui.add(widget, alignment="center_h")

        # add another vertically stretching space with the same proportion, to keep
        # the input field centered vertically within the available vertical space
        gui.add((0, 0), proportion=1.)

        # add a horizontally stretching status bar
        status_text = "GUI ready and awaiting input"
        label = DirectLabel(parent=gui_root, text=status_text, text_pos=(10, -.5),
            textMayChange=1, frameSize=(0, 1, -.5, .5), scale=20)
        widget = Widget(label, "horizontal")
        borders = (10, 10, 10, 20)
        gui.add(widget, expand=True, borders=borders)

        # the GUI system needs to do some final setup
        gui.finalize()

        # run the app
        showbase.run()


MyApp()
