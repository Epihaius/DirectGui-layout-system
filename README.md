# DirectGui-layout-system

This is an automatic layout management system for Panda3D's DirectGui.
It uses "sizers", a kind of abstract containers that can be filled in a certain direction with widgets, sizes (empty space) and other sizers, so they can be nested as deeply as needed.

The aim of this system is to provide an intuitive and automatic alternative to having to manually specify position and size of widgets and to maintain that layout whenever the window size changes.

The provided main.py script produces the following layout at a very small resolution:

![Layout_at_small_res](https://github.com/Epihaius/DirectGui-layout-system/blob/master/Layout%20at%20very%20small%20resolution.png "Layout at very small resolution")

As you can see, even when the widgets no longer fit in the window, they are not scaled down to an unpractical small size (which is how DirectGui handles things), but text retains its size and therefore remains legible.

[More screenshots](https://github.com/Epihaius/DirectGui-layout-system/wiki/Screenshots)
