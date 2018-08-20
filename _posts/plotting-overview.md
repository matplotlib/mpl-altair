---
layout: post
title:  "Altair vs Matplotlib Plot Construction Overview"
date:   2018-08-15 14:50:00 -0500
author: "Kimberly Orr"
categories: about
tags: "intro about matplotlib altair"
excerpt_separator: <!--read more-->
---
## Altair
Altair is a Python visualization library built on top of the Vega/Vegalite declarative grammar. As Altair's [overview](https://altair-viz.github.io/getting_started/overview.html) states:
>The key idea is that you are declaring links between data columns and visual encoding channels, such as the x-axis, y-axis, color, etc.

So, the general process for creating a basic Altair plot is to specify your data:
 ```python
alt.Chart(df)
 ``` 
Specify what type of glyph/marker should be used to represent your data:
```python
.mark_point()
```
Then link your data columns with the encoding channels:
 ```python
.encode(x=alt.X("column1"), y=alt.Y("column2"))
 ```
 
So that a finished plot would look like:
 ```python
# import
import altair as alt
# plot
alt.Chart(df).mark_point().encode(
    x=alt.X("column1"), y=alt.Y("column2"), color=alt.Color("column3")
)
```
## Matplotlib
Matplotlib is a powerful object-oriented procedural plotting library. The general process to create a Matplotlib plot is to first create a figure (canvas) and one or more subplots (which are objects that encapsulate plot data to facilitate adding multiple plots to a single canvas) and then add objects to the subplots (like axes, which contain glyphs, etc.). So, instead of linking data with encoding channels, Matplotlib uses an object-oriented interface to place objects on a canvas.

The general thought process is to create the canvas/subplots:
```python
fig, ax = plt.subplots()
```
Add a scatter plot to the axes object of this figure:
```python
ax.scatter(x_array, y_array)
```
Show it:
```python
plt.show()
```

So that a plot of `y_array` vs `x_array` colored by `color_array` would look like this:
```python
import matplotlib.pyplot as plt
# plot
fix, ax = plt.subplots()
ax.scatter(x_array, y_array, c=color_array)
plt.show()
```

## mpl-altair
mpl-altair allows you to create an altair chart as normal and convert/render it as a Matplotlib figure like so:
```python
import altair as alt
import matplotlib.pyplot as plt
import mplaltair
# make an altair chart
chart = alt.Chart(df).mark_point().encode(
    alt.X("column1"), alt.Y("column2")
)
# convert to Matplotlib
fig, ax = mplaltair.convert(chart)
plt.show()
```