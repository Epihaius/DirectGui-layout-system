#!/usr/bin/env python

# Author: Epihaius
# Date: 2019-09-23
# Last revision: 2020-10-08
#
# This is a basic example of how to use the sizer-based GUI system.
# It specifically showcases how to handle a DirectScrolledList.

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

        # add a horizontally expanding title bar
        title = "Panda3D: scrolled list layout example"
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

        # add a horizontally growable sizer that will be proportionately resized
        # vertically and horizontally
        sizer = Sizer("horizontal")
        borders = (10, 10, 20, 10)
        gui.sizer.add(sizer, proportions=(1., 1.), borders=borders)

        # add a vertically growable subsizer to the previous sizer;
        # set the vertical gap between each two of its cells to 10 pixels
        # (this is a more convenient alternative to setting the same borders
        # for all but the last of its cells, i.e. `(0, 0, 10, 0)`)
        btn_sizer = Sizer("vertical", gaps=(0, 10))
        borders = (0, 20, 0, 0)
        sizer.add(btn_sizer, borders=borders)

        # add a couple of horizontally expanding buttons to the subsizer;
        # they will have the same width, determined by the initially largest button
        text = "My Button"
        button = DirectButton(parent=gui_root, text=text, text_scale=20, borderWidth=(2, 2))
        widget = Widget(button)
        btn_sizer.add(widget)
        text = "Insert list into frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__insert_list)
        widget = Widget(button)
        btn_sizer.add(widget)
        # add vertical space with a fixed size
        btn_sizer.add((0, 30))
        text = "A third button"
        button = DirectButton(parent=gui_root, text=text, text_scale=20, borderWidth=(2, 2))
        widget = Widget(button)
        btn_sizer.add(widget)

        # add some horizontally stretching space, so that widgets added after it
        # will be pushed to the right
        sizer.add((0, 0), proportions=(1., 0.))

        # add a frame resizable in both directions and taking up two thirds of
        # the available horizontal space (because of the ratio of the proportions
        # used for the frame and the stretching space that was previously added)
        self.frame = frame = DirectFrame(parent=gui_root, frameColor=(.5, .6, .7, 1.))
        widget = Widget(frame)
        sizer.add(widget, proportions=(2., 1.))

        # assign a sizer to the frame to manage the layout of its child widgets
        self.frame_sizer = frame_sizer = Sizer("vertical")
        widget.sizer = frame_sizer

        # add a horizontally expanding label with right-aligned text to the frame
        text = "right-aligned text"
        label = DirectLabel(parent=frame, text=text,
            text_scale=20, text_align=TextNode.A_right)
        widget = Widget(label)
        borders = (10, 10, 20, 10)
        frame_sizer.add(widget, proportions=(1., 0.), borders=borders)

        # add a non-resizing, right-aligned button to the frame
        text = "Button in frame "
        button = DirectButton(parent=frame, text=text, text_scale=20, borderWidth=(2, 2))
        widget = Widget(button)
        borders = (0, 10, 10, 20)
        frame_sizer.add(widget, alignments=("max", "min"), borders=borders)

        # add a non-resizing input field, centered horizontally within its cell,
        # which itself is assigned all of the width available to it, by setting
        # its horizontal proportion to 1.0
        field = DirectEntry(parent=gui_root, text_scale=20, focus=1)
        widget = Widget(field)
        gui.sizer.add(widget, proportions=(1., 0.), alignments=("center", "min"))

        # add a horizontally expanding status bar
        status_text = "GUI ready and awaiting input"
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

    def __insert_list(self):

        scrolled_list = DirectScrolledList(
            parent=self.frame,

            decButton_text="Dec",
            decButton_text_scale=20,
            decButton_borderWidth=(4, 4),

            incButton_text="Inc",
            incButton_text_scale=20,
            incButton_borderWidth=(4, 4),

            frameColor=(1., 0., 0., .5),
            forceHeight=29  # item height
        )

        list_widget = ScrolledListWidget(
            scrolled_list,
            # the width of the scroll buttons will take up 20 % of the available
            # space, since they are surrounded by space that is stretched using
            # a proportion of 1.: .25 / (1. + .25) = 1/5 = .2
            scrollbtn_proportion=.25,
            scrollbtn_borders=(5, 5, 10, 10),
            itemframe_borders=(5, 5, 0, 0),
            margins=(10, 10)  # left and right borders around the items in the frame
        )

        b1 = DirectButton(text=("Button1", "click!", "roll", "disabled"),
            borderWidth=(4, 4), relief=2, text_scale=20)

        b2 = DirectButton(text=("Feel free to remove me", "Goodbye!",
            "Yeah I'm still here", "Not now"), borderWidth=(4, 4), relief=2,
            text_scale=20, command=lambda: self.__remove_item(list_widget, b2))

        list_widget.add_item(b1)
        list_widget.add_item(b2)

        checkbtn = DirectCheckButton(text="CheckButton",
            text_scale=20, boxPlacement="right", borderWidth=(3, 3), indicator_text_scale=20,
            indicator_text_pos=(0, 4), indicator_borderWidth=(2, 2), boxBorder=1)
        list_widget.add_item(checkbtn)

        l1 = DirectLabel(text="Test1", text_scale=20)
        l2 = DirectLabel(text="Test2", text_scale=20)
        l3 = DirectLabel(text="Test3", text_scale=20)

        list_widget.add_item(l1)
        list_widget.add_item(l2)
        list_widget.add_item(l3)

        for fruit in ['apple', 'pear', 'banana', 'orange']:
            l = DirectLabel(text=fruit, text_scale=20)
            list_widget.add_item(l)

        borders = (10, 10, 5, 5)
        # add the list to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(list_widget, proportions=(1., 1.), borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()

    def __remove_item(self, list_widget, item):

        list_widget.remove_item(item)

        # update the GUI layout
        self.gui.layout()


MyApp()
