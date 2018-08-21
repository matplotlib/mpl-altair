---
layout: post
title:  "What's supported in mpl-altair"
date:   2018-08-21 4:15:00 -0500
author: "Kimberly Orr"
categories: about
tags: "about"
excerpt_separator: <!--read more-->
---

# What is supported in mpl-altair?

**Supported Marks**
- mark_circle
- mark_point
- mark_square
- mark_line


**Supported Encodings**

channel | supported marks
:--- | :---
x | circle, point, square, line
y | circle, point, square, line
color | circle*, point*, square*, line
fill | point*, line
size |
stroke | line

*Only quantitative and temporal data are supported for these encodings.

**Supported Axis modifications**

ex:
```python
alt.Chart(df).mark_point().encode(
    alt.X('a:Q', axis=alt.Axis(format='.2g'))
)
```

attribute | support notes
:--- | :---
domain |
format | Supported
grid |
labelAngle | supported?
labelBound |
labelFlush |
labelOverlap |
labelPadding |
labels |
maxExtent |
minExtent |
offset |
orient |
position |
tickCount | Supported
tickSize |
ticks |
title |
titleMaxLength |
titlePadding |
values | Supported
zindex |

**Supported Scale modifications**

ex:
```python
alt.Chart(df).mark_point().encode(
    alt.X('a:Q', scale=alt.Scale(type='log'))
)
```

attribute | support notes
--- | ---
base | supported
clamp |
domain | supported
exponent |
interpolate |
nice |
padding |
paddingInner |
paddingOuter |
range |
rangeStep |
round |
scheme |
type | linear, log, time scales supported
zero | supported
