import altair as alt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from mplaltair import convert
from .._axis import convert_axis
import pytest

from .._data import _locate_channel_dtype

df_quant = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, -3],
    "s": [50, 100, 200.0], "alpha": [0, .5, .8], "shape": [1, 2, 3], "fill": [1, 2, 3],
    "neg": [-3, -4, -5], 'log': [11, 100, 1000], 'log2': [1, 3, 5],
    "years": pd.date_range('01/01/2015', periods=3, freq='Y'), "months": pd.date_range('1/1/2015', periods=3, freq='M'),
    "days": pd.date_range('1/1/2015', periods=3, freq='D'), "hrs": pd.date_range('1/1/2015', periods=3, freq='H'),
    "combination": pd.to_datetime(['1/1/2015 00:00', '1/4/2016 10:00', '5/1/2016'])
})


def test_axis_dtype():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('years'), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    assert _locate_channel_dtype(chart, 'x') == 'temporal'

# @pytest.mark.skip
def test_axis_more_than_x_and_y():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('b'), color=alt.Color('c'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

# @pytest.mark.skip
@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha'), ('months', 'a')])
def test_axis_quantitative(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(alt.X(x), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.show()

# @pytest.mark.skip
@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha')])
def test_axis_false_zero_quantitative(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(zero=False)),
        alt.Y(y, scale=alt.Scale(zero=False))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel("Zero False")
    ax.set_ylabel("Zero False")
    plt.show()

# @pytest.mark.skip
@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha')])
def test_axis_true_zero_quantitative(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(zero=True)),
        alt.Y(y, scale=alt.Scale(zero=True))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel("Zero True")
    ax.set_ylabel("Zero True")
    plt.show()

# @pytest.mark.skip
@pytest.mark.parametrize('x,y,x_dom,y_dom', [('a', 'c', [0.5, 4], [-5, 10]), ('neg', 'alpha', [-6, -2], [0, 1])])
def test_axis_domain_quantitative(x, y, x_dom, y_dom):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(domain=x_dom)),
        alt.Y(y, scale=alt.Scale(domain=y_dom))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(str(x_dom))
    ax.set_ylabel(str(y_dom))
    plt.show()

# @pytest.mark.skip
@pytest.mark.xfail(raises=NotImplementedError)
def test_axis_unaggregated_quantitative():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', scale=alt.Scale(domain="unaggregated")),
        alt.Y('c', scale=alt.Scale(domain="unaggregated"))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    plt.close()
    convert_axis(ax, chart)

# @pytest.mark.skip
@pytest.mark.parametrize('column,type,base', [('log','log',10), ('log2', 'log', 2), pytest.param('log','pow',10, marks=pytest.mark.xfail)])
def test_axis_scale_type_x_quantitative(column, type, base):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(column, scale=alt.Scale(type=type, base=base)),
        alt.Y('a')
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

# @pytest.mark.skip
@pytest.mark.parametrize('column,type,base,exponent', [('log','log',10,1), ('log2','log',5,1), pytest.param('log','pow',10,2, marks=pytest.mark.xfail)])
def test_axis_scale_type_y_quantitative(column, type, base, exponent):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a'),
        alt.Y(column, scale=alt.Scale(type=type, base=base, exponent=exponent))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

# @pytest.mark.skip
def test_axis_fixed_ticks_quantitative():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3])), alt.Y('b', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3]))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()


@pytest.mark.parametrize('x,y', [(1, 1), (3, 3), (5,5)])
def test_axis_tickCount(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('log', axis=alt.Axis(tickCount=x)), alt.Y('a', axis=alt.Axis(tickCount=y))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(str(x))
    ax.set_ylabel(str(y))
    plt.show()