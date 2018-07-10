import altair as alt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from .._convert import convert
from .._axis import convert_axis

df_quant = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, -3],
    "s": [50, 100, 200.0], "alpha": [.1, .5, .8], "shape": [1, 2, 3], "fill": [1, 2, 3]
})

def test_axis_quantitative():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('c'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()
