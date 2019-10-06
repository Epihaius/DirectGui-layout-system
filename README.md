# DirectGui-layout-system

This is an automatic layout management system for Panda3D's DirectGui.
It uses "sizers", a kind of abstract containers that can be filled in a certain direction with widgets, sizes (empty space) and other sizers, so they can be nested as deeply as needed.

The aim of this system is to provide an intuitive and automatic alternative to having to manually specify position and size of widgets and to maintain that layout whenever the window size changes.

The provided main.py script produces the following layout:

![Layout at default resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Layout%20at%20default%20resolution.png)
![Layout at reduced resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Layout%20at%20reduced%20resolution.png)
![Layout at very small resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Layout%20at%20very%20small%20resolution.png)

As you can see, even when the widgets no longer fit in the window, they are not scaled down to an unpractical small size (which is how DirectGui handles things), but text retains its size and therefore remains legible.

Run scrolled_list.py to see how a DirectScrolledList can be controlled using this layout system:

![Scrolled list at default resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Scrolled%20list%20at%20default%20resolution.png)
![Scrolled list at reduced resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Scrolled%20list%20at%20reduced%20resolution.png)

Run scrolled_frame.py to see how a DirectScrolledFrame can be controlled using this layout system:

![Scrolled frame at default resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Scrolled%20frame%20at%20default%20resolution.png)
![Scrolled frame at reduced resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Scrolled%20frame%20at%20reduced%20resolution.png)

Run gridsizer.py to see the effect of a grid sizer:

![Grid sizer at default resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Grid%20sizer%20at%20default%20resolution.png)
![Grid sizer at very small resolution](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Grid%20sizer%20at%20very%20small%20resolution.png)
