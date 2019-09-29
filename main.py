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
        self.gui = gui = GUI(showbase)

        # Build the GUI layout

        # add a horizontally stretching title bar
        title = "Panda3D: GUI layout example"
        label = DirectLabel(parent=gui_root, text=title, frameSize=(0, 0, -20, 30),
            text_scale=20, borderWidth=(6, 6), relief=DGG.SUNKEN)
        widget = Widget(label, "horizontal")
        borders = (10, 10, 20, 10)
        gui.sizer.add(widget, expand=True, borders=borders)

        # add a horizontal sizer that can stretch (expand) horizontally
        sizer = Sizer("horizontal")
        borders = (10, 10, 20, 10)
        gui.sizer.add(sizer, expand=True, borders=borders)

        # add a vertical, non-stretching subsizer to the previous sizer
        btn_sizer = Sizer("vertical")
        borders = (0, 20, 0, 0)
        sizer.add(btn_sizer, borders=borders)

        # add horizontally stretching buttons to the subsizer;
        # they will have the same width, determined by the initially largest button
        borders = (0, 0, 10, 0)
        text = "Add button to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_button)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True, borders=borders)
        text = "Add checkbutton to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_checkbutton)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True, borders=borders)
        text = "Add radiobuttons to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_radiobuttons)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True, borders=borders)
        text = "Add menu to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_menu)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True, borders=borders)
        text = "Add slider to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_slider)
        widget = Widget(button, "horizontal")
        btn_sizer.add(widget, expand=True)

        # add some horizontally stretching space, so that widgets added after it
        # will be pushed to the right
        sizer.add((0, 0), proportion=1.)

        # add a frame stretching in both directions and taking up two thirds of
        # the available horizontal space (because of the ratio of the proportions
        # used for the frame and the stretching space that was previously added)
        self.frame = frame = DirectFrame(parent=gui_root, frameColor=(.5, .6, .7, 1.))
        widget = Widget(frame, "both")
        sizer.add(widget, expand=True, proportion=2.)

        # assign a sizer to the frame to manage the layout of its child widgets
        self.frame_sizer = frame_sizer = Sizer("vertical")
        widget.set_sizer(frame_sizer)

        # add a horizontally stretching label with right-aligned text to the frame
        text = "right-aligned text"
        label = DirectLabel(parent=frame, text=text,
            text_scale=20, text_align=TextNode.A_right)
        widget = Widget(label, "horizontal")
        borders = (10, 10, 20, 10)
        frame_sizer.add(widget, expand=True, borders=borders)

        # add some vertically stretching space to the frame, so that widgets added
        # after it will be pushed downwards
        frame_sizer.add((0, 0), proportion=1.)

        # add a non-stretching, right-aligned button to the frame
        text = "Button in frame "
        button = DirectButton(parent=frame, text=text, text_scale=20, borderWidth=(2, 2))
        widget = Widget(button)
        borders = (0, 10, 10, 20)
        frame_sizer.add(widget, alignment="right", borders=borders)

        # add some vertically stretching space to the GUI, so that widgets added
        # after it will be pushed downwards
        gui.sizer.add((0, 0), proportion=1.)

        # add a non-stretching input field, centered horizontally
        field = DirectEntry(parent=gui_root, text_scale=20, focus=1)
        widget = Widget(field)
        gui.sizer.add(widget, alignment="center_h")

        # add another vertically stretching space with the same proportion, to keep
        # the input field centered vertically within the available vertical space
        gui.sizer.add((0, 0), proportion=1.)

        # add a horizontally stretching status bar
        status_text = "GUI ready and awaiting input"
        label = DirectLabel(parent=gui_root, text=status_text, text_pos=(20, -10),
            textMayChange=1, frameSize=(0, 0, -10, 10), text_scale=20, text_align=TextNode.A_left)
        widget = Widget(label, "horizontal")
        borders = (10, 10, 10, 20)
        gui.sizer.add(widget, expand=True, borders=borders)

        # let the GUI system create the layout
        gui.layout()

        # run the app
        showbase.run()

    def __add_button(self):

        text = "Another Button"
        button = DirectButton(parent=self.frame, text=text, text_scale=20, borderWidth=(6, 6))
        widget = Widget(button, "horizontal")
        borders = (10, 10, 10, 10)
        # add the button to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(widget, expand=True, borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()

    def __add_checkbutton(self):

        btn = DirectCheckButton(parent=self.frame, text="CheckButton",
            scale=20, boxPlacement="right")
        widget = Widget(btn, "horizontal")
        borders = (10, 10, 10, 10)
        # add the checkbutton to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(widget, expand=True, borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()

    def __add_radiobuttons(self):

        v = [0]
        buttons = [
            DirectRadioButton(parent=self.frame, text='RadioButton0', variable=v,
                value=[0], boxPlacement="right", scale=20),
            DirectRadioButton(parent=self.frame, text='RadioButton1', variable=v,
                value=[1], boxPlacement="right", scale=20)
        ]
        borders = (10, 10, 10, 10)

        for button in reversed(buttons):
            widget = Widget(button, "horizontal")
            # add the radiobuttons to the frame, below the right-aligned text label, using index=1
            self.frame_sizer.add(widget, expand=True, borders=borders, index=1)
            button.setOthers(buttons)

        # update the GUI layout
        self.gui.layout()

    def __add_menu(self):

        menu = DirectOptionMenu(parent=self.frame, text="options", scale=20,
            borderWidth=(.3, .3), items=["item1","item2","item3"], initialitem=2,
            frameSize=(0, .25, -.75, .75), highlightColor=(.65, .65, .65, 1.),
            text_pos=(.5, -.25), popupMarkerBorder=(.6, 0.))
        widget = Widget(menu, "horizontal")
        borders = (10, 10, 10, 10)
        # add the menu to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(widget, expand=True, borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()

    def __add_slider(self):

        slider = DirectSlider(parent=self.frame, range=(0,100), value=50,
            pageSize=10, thumb_frameSize=(-10, 10, -15, 15),
            frameSize=(0, 0, -15, 15), borderWidth=(3, 3))
        widget = Widget(slider, "horizontal")
        borders = (10, 10, 10, 10)
        # add the slider to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(widget, expand=True, borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()


MyApp()
