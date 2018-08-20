---
layout: post
title:  "Making a Bar Chart"
date:   2018-08-15 16:00:00 -0500
author: "Kimberly Orr", "Nabarun Pal"
categories: user-guide
tags: "intro about bar"
excerpt_separator: <!--read more-->
---

# Making a Bar Chart
At the time of writing, mpl-altair does not support bar charts, so this post will show how to create a bar chart in Altair, Matplotlib, and how mpl-altair _should_ implement bar chart conversion in the future.

We'll work with the following long-form DataFrame for this example:
```python
import pandas as pd
df = pd.DataFrame({
    'group': ['1', '1', '2', '2', '3', '3', '4', '4', '5', '5'],
    'variable': ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'],
    'scores': [20, 25, 35, 32, 30, 34, 35, 20, 27, 25]
})
```

## Altair
For this dataset, specifying the color will automatically stack the bar charts.
```python
import altair as alt
alt.Chart(df).mark_bar().encode(
    x='group',
    y='scores',
    color='variable'
)
```
![png](pics/altair-to-mpl-bar_0.png)

## Matplotlib
This is a little more complicated in Matplotlib. Since Matplotlib is procedural, we have to manually tell Matplotlib to stack the bars. Also notice that we are calling a new function now (`ax.bar()`) to get a bar plot.

To stack group b on top of group a, we have to use the `bottom` kwarg to tell Matplotlib where we want the bottom of each bar to be. A clean way to do this is to create an array that keeps track of the bottoms of the bars.

So, in this example, we first plot group a with bottom initialized to zeros (so that each bar starts at zero). After we plot group b, we update bottom to contain group a's scores. Then, we plot group b with the updated bottom array.

```python
import matplotlib.pyplot as plt
```
```python
fig, ax = plt.subplots()

bottom = np.zeros(len(df['group'].unique()))  # initialize to zeros so the bottom of group a is zero
for label, scores in df.groupby('variable'):
    ax.bar(scores['group'], scores['scores'], bottom=bottom, label=label)
    bottom += scores['scores']  # set bottom to be the top of the current group

ax.set_xlabel('groups')
ax.set_ylabel('scores')
ax.legend()
plt.grid()
plt.show()
```
Both produce:

![png](pics/altair-to-mpl-bar_1.png)


## mpl-altair
At the time of writing, mpl-altair doesn't support bar charts.

If mpl-altair supported bar charts, this is how an Altair chart would get rendered in mpl-altair:
```python
import altair as alt
import matplotlib.pyplot as plt
import mplaltair
chart = alt.Chart(df).mark_bar().encode(
    x='group',
    y='scores',
    color='variable'
)
fig, ax = mplaltair.convert(chart)
plt.show()
```