---
layout: post
title:  "Making a Line Plot"
date:   2018-08-15 15:30:00 -0500
author: "Kimberly Orr and Nabarun Pal"
categories: user-guide
tags: "intro about line"
excerpt_separator: <!--read more-->
---

# Making a Line Plot
Altair works best with [long-form](https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data) data. This is where each row contains a single observation along with all of its metadata stored as values.

Matplotlib works a little better with wide-form data.

Since mpl-altair converts from Altair to Matplotlib, let's look at how to create a line plot using Altair, Matplotlib, and mpl-altair with the following long-form data.

```python
import pandas as pd
df = pd.DataFrame({
    'set': [1, 2, 1, 2, 1, 2, 1, 2],
    'amount': [1, 4, 5, 3, 1, 7, 2, 9],
    'location': ['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd']
})
```
If you need a scenario to help think about the data, imagine that you're running an experiment in several different locations and you take two measurements for each location. Now you want to visualize how the amount changed between the two sets of measurements at each location.

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>set</th>
      <th>amount</th>
      <th>location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>a</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>4</td>
      <td>a</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>5</td>
      <td>b</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>3</td>
      <td>b</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>1</td>
      <td>c</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2</td>
      <td>7</td>
      <td>c</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>2</td>
      <td>d</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2</td>
      <td>9</td>
      <td>d</td>
    </tr>
  </tbody>
</table>
</div>

## Altair
If we want to plot lines to show how each location changed between set one and set two,
we need to specify the data, tell Altair to plot lines with `mark_line()`, link the x
encoding channel with 'set', the y channel with 'amount', and the color channel with 'location'.
```python
import altair as alt
alt.Chart(df).mark_line().encode(
    alt.X('set'),
    alt.Y('amount'),
    alt.Color('location')
)
```
![png](pics/altair-to-mpl-line_0.png)

## Matplotlib
In Matplotlib, just like with a categorical scatter plot, we have to plot a new line for every location.
Specifying a label with each line allows us to generate a legend with `ax.legend()`.
```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
for loc, subset in df.groupby('location'):
    ax.plot('set', 'amount', data=subset, label=loc)
ax.set_xlabel('set')
ax.set_ylabel('amount')
ax.legend(title='location')
plt.grid()
plt.show()
```
![png](pics/altair-to-mpl-line_1.png)

## mpl-altair
To render the Altair chart using Matplotlib:
```python
import altair as alt
import matplotlib.pyplot as plt
import mplaltair
chart = alt.Chart(df).mark_line().encode(
    alt.X('set'),
    alt.Y('amount'),
    alt.Color('location')
)
fig, ax = mplaltair.convert(chart)
plt.show()
```
![png](pics/altair-to-mpl-line_2.png)