#!/usr/bin/env python

# Author: Epihaius
# Date: 2019-10-04
# Last revision: 2020-10-08
#
# This is a basic example of how to use the sizer-based GUI system.
# It specifically showcases how to handle a DirectScrolledFrame.

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
        title = "Panda3D: scrolled frame layout example"
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

        # add a horizontally growable sizer that will be expanded horizontally
        self.frame_area_sizer = sizer = Sizer("horizontal")
        borders = (10, 10, 20, 10)
        gui.sizer.add(sizer, proportions=(1., 0.), borders=borders)

        # add a vertically growable subsizer to the previous sizer;
        # set the vertical gap between each two of its cells to 10 pixels
        # (this is a more convenient alternative to setting the same borders
        # for all but the last of its cells, i.e. `(0, 0, 10, 0)`)
        btn_sizer = Sizer("vertical", gaps=(0, 10))
        borders = (0, 20, 0, 0)
        sizer.add(btn_sizer, borders=borders)

        # add horizontally expanding buttons to the subsizer;
        # they will have the same width, determined by the initially largest button
        text = "Add button to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_button)
        widget = Widget(button)
        btn_sizer.add(widget)
        text = "Add checkbutton to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_checkbutton)
        widget = Widget(button)
        btn_sizer.add(widget)
        text = "Add radiobuttons to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_radiobuttons)
        widget = Widget(button)
        btn_sizer.add(widget)
        text = "Add slider to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_slider)
        widget = Widget(button)
        btn_sizer.add(widget)
        text = "Add sub-layout to frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=20,
            borderWidth=(2, 2), command=self.__add_layout)
        widget = Widget(button)
        btn_sizer.add(widget)
        # add vertical space with a fixed size
        btn_sizer.add((0, 30))
        text = "Destroy frame"
        button = DirectButton(parent=gui_root, text=text, text_scale=25,
            textMayChange=True, borderWidth=(3, 3), command=self.__toggle_frame)
        self.frame_toggle_button = widget = Widget(button)
        btn_sizer.add(widget)

        # add some horizontally stretching space, so that widgets added after it
        # will be pushed to the right
        sizer.add((0, 0), proportions=(1., 0.))

        self.has_frame = False
        # add a frame resizable in both directions and taking up two thirds of
        # the available horizontal space (because of the ratio of the proportions
        # used for the frame and the stretching space that was previously added)
        self.__toggle_frame(update_layout=False)

        # add a non-resizing input field, centered horizontally and vertically within
        # its cell, which itself is assigned all of the space available to it, by
        # setting its proportions to 1.0
        field = DirectEntry(parent=gui_root, text_scale=20, focus=1)
        widget = Widget(field)
        gui.sizer.add(widget, proportions=(1., 1.), alignments=("center", "center"))

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

    def __toggle_frame(self, update_layout=True):

        self.has_frame = not self.has_frame

        if self.has_frame:

            # add a frame resizable in both directions and taking up two thirds of
            # the available horizontal space (because of the ratio of the proportions
            # used for the frame and the stretching space that was previously added)
            frame = DirectScrolledFrame(parent=self.gui_root, manageScrollBars=True,
                autoHideScrollBars=True, frameColor=(.5, .6, .7, 1.), scrollBarWidth=20,
                borderWidth=(3, 3), relief=DGG.RIDGE)
            self.frame_widget = widget = ScrolledFrameWidget(frame, "vertical")
            self.frame_area_sizer.add(widget, proportions=(2., 1.))
            self.frame = frame = frame.getCanvas()
            # all child widgets of a scrolled frame need to be added to its canvas sizer
            # in order to manage their layout
            self.frame_sizer = frame_sizer = widget.canvas_sizer

            # add a horizontally expanding label with right-aligned text to the frame
            text = "right-aligned text"
            label = DirectLabel(parent=frame, text=text,
                text_scale=20, text_align=TextNode.A_right)
            widget = Widget(label)
            borders = (10, 10, 20, 10)
            frame_sizer.add(widget, proportions=(1., 0.), borders=borders)

            # add some vertically stretching space to the frame, so that widgets added
            # after it will be pushed downwards
            frame_sizer.add((0, 0), proportions=(0., 1.))

            # add a non-resizing, right-aligned button to the frame
            text = "Button in frame "
            button = DirectButton(parent=frame, text=text, text_scale=20, borderWidth=(2, 2))
            widget = Widget(button)
            borders = (0, 10, 10, 20)
            frame_sizer.add(widget, alignments=("max", "min"), borders=borders)
            self.frame_toggle_button.dgui_obj["text"] = "Destroy frame"

        else:

            # remove the frame, destroying it and all of its child widgets
            self.frame_area_sizer.remove_cell(self.frame_widget.sizer_cell, destroy=True)
            self.frame = frame = None
            # make the button text very long to see how it affects the layout
            text = "Create a new frame to the right"
            self.frame_toggle_button.dgui_obj["text"] = text

        if update_layout:
            self.frame_toggle_button.reset_frame_size()
            # update the GUI layout
            self.gui.layout()

    def __add_button(self):

        if not self.has_frame:
            return

        def remove_button():

            self.frame_sizer.remove_cell(widget.sizer_cell, destroy=True)
            self.gui.layout()

        button = DirectButton(parent=self.frame, text=("Feel free to remove me", "Goodbye!",
            "Yeah I'm still here", "So useless"), borderWidth=(6, 6),
            text_scale=20, command=remove_button)
        widget = Widget(button)
        borders = (10, 10, 10, 10)
        # add the button to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(widget, proportions=(1., 0.), borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()

    def __add_checkbutton(self):

        if not self.has_frame:
            return

        btn = DirectCheckButton(parent=self.frame, text="CheckButton",
            text_scale=20, boxPlacement="right", borderWidth=(2, 2), indicator_text_scale=20,
            indicator_text_pos=(0, 4), indicator_borderWidth=(2, 2), boxBorder=1)
        widget = Widget(btn)
        borders = (10, 10, 10, 10)
        # add the checkbutton to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(widget, proportions=(1., 0.), borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()

    def __add_radiobuttons(self):

        if not self.has_frame:
            return

        v = [0]
        buttons = [
            DirectRadioButton(parent=self.frame, text='RadioButton0', variable=v,
                value=[0], boxPlacement="right", text_scale=20, indicator_text_pos=(0, 5),
                borderWidth=(2, 2), indicator_text_scale=20, indicator_borderWidth=(2, 2)),
            DirectRadioButton(parent=self.frame, text='RadioButton1', variable=v,
                value=[1], boxPlacement="right", text_scale=20, indicator_text_pos=(0, 5),
                borderWidth=(2, 2), indicator_text_scale=20, indicator_borderWidth=(2, 2))
        ]
        borders = (10, 10, 10, 10)

        for button in reversed(buttons):
            widget = Widget(button)
            # add the radiobuttons to the frame, below the right-aligned text label, using index=1
            self.frame_sizer.add(widget, proportions=(1., 0.), borders=borders, index=1)
            button.setOthers(buttons)

        # update the GUI layout
        self.gui.layout()

    def __add_slider(self):

        if not self.has_frame:
            return

        slider = DirectSlider(parent=self.frame, range=(0,100), value=50,
            pageSize=10, thumb_frameSize=(-10, 10, -15, 15), frameSize=(0, 0, -15, 15),
            frameColor=(.3, .3, .3, 1.), borderWidth=(3, 3))
        widget = Widget(slider)
        borders = (10, 10, 10, 10)
        # add the slider to the frame, below the right-aligned text label, using index=1
        self.frame_sizer.add(widget, proportions=(1., 0.), borders=borders, index=1)

        # update the GUI layout
        self.gui.layout()

    def __add_layout(self):

        if not self.has_frame:
            return

        def remove_sizer():

            self.frame_sizer.remove_cell(subsizer.sizer_cell, destroy=True)
            self.gui.layout()

        # create a sizer to manage a sub-layout that can be as complex as desired
        subsizer = Sizer("horizontal")
        # add the sizer managing the sub-layout to the frame, below the right-aligned
        # text label, using index=1
        self.frame_sizer.add(subsizer, proportions=(1., 0.), borders=(10, 10, 10, 10), index=1)

        # Build a sub-layout of any complexity

        v_sizer = Sizer("vertical")
        subsizer.add(v_sizer)
        button = DirectButton(parent=self.frame, text="Button", borderWidth=(6, 6),
            text_scale=20)
        widget = Widget(button)
        v_sizer.add(widget, borders=(0, 0, 10, 0))
        button = DirectButton(parent=self.frame, text="Destroy sub-layout",
            borderWidth=(6, 6), text_scale=20, text_wordwrap=5., command=remove_sizer)
        widget = Widget(button)
        v_sizer.add(widget)
        button = DirectButton(parent=self.frame, text="Centered button",
            borderWidth=(6, 6), text_scale=20, text_wordwrap=5.)
        widget = Widget(button)
        subsizer.add(widget, proportions=(1., 0.), alignments=("center", "center"),
            borders=(5, 5, 0, 0))

        # update the GUI layout
        self.gui.layout()


MyApp()
