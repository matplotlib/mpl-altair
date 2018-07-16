import altair as alt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from mplaltair import convert
from .._axis import convert_axis
import pytest

df_quant = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, -3],
    "s": [50, 100, 200.0], "alpha": [.1, .5, .8], "shape": [1, 2, 3], "fill": [1, 2, 3],
    "neg": [-3, -4, -5], 'log': [10, 100, 1000]
})

@pytest.mark.skip
@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha')])
def test_axis_quantitative(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(alt.X(x), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

@pytest.mark.skip
@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha')])
def test_axis_quantitative_false_zero(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(zero=False)),
        alt.Y(y, scale=alt.Scale(zero=False))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

@pytest.mark.skip
@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha')])
def test_axis_quantitative_true_zero(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(zero=True)),
        alt.Y(y, scale=alt.Scale(zero=True))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()


@pytest.mark.parametrize('x,y,x_dom,y_dom', [('a', 'c', [0.5, 4], [-5, 10]), ('neg', 'alpha', [-6, -2], [0, 1])])
def test_axis_quantitative_domain(x, y, x_dom, y_dom):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(domain=x_dom)),
        alt.Y(y, scale=alt.Scale(domain=y_dom))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()


def test_axis_quantitative_log_x():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('log', scale=alt.Scale(type='log')),
        alt.Y('a')
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

def test_axis_quantitative_log_y():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a'),
        alt.Y('log', scale=alt.Scale(type='log'))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()
