---
layout: post
title:  "How to Use mpl-altair"
date:   2018-08-21 3:45:00 -0500
author: "Kimberly Orr"
categories: about
tags: "intro about"
excerpt_separator: <!--read more-->
---

**Process**
1. create a chart using Altair
2. call mplaltair's `convert` function
3. show the figure or add to it using Matplotlib

```python
import pandas as pd
df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [1, 10, 1000, 10000]})

# Step 1
import altair as alt
import matplotlib.pyplot as plt
import mplaltair
chart = alt.Chart(df).mark_point().encode(
    alt.X('x'), alt.Y('y', alt.Scale(type='log'))
)

# Step 2
fig, ax = mplaltair.convert(chart)

# Step 3
plt.show()
```

