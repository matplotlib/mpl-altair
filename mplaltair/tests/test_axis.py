import altair as alt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from mplaltair import convert
from .._axis import convert_axis
import numpy as np
import pytest

from .._data import _locate_channel_dtype

df_quant = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, -3],
    "s": [50, 100, 200.0], "alpha": [0, .5, .8], "shape": [1, 2, 3], "fill": [1, 2, 3],
    "neg": [-3, -4, -5], 'log': [11, 100, 1000], 'log2': [1, 3, 5],
    "years": pd.to_datetime(['1/1/2015', '1/1/2016', '1/1/2017']),
    "months": pd.to_datetime(['1/1/2015', '2/1/2015', '3/1/2015']),
    "days": pd.to_datetime(['1/1/2015', '1/2/2015', '1/3/2015']),
    "hrs": pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00']),
    # "years": pd.date_range('01/01/2015', periods=3, freq='Y'), "months": pd.date_range('1/1/2015', periods=3, freq='M'),
    # "days": pd.date_range('1/1/2015', periods=3, freq='D'), "hrs": pd.date_range('1/1/2015', periods=3, freq='H'),
    "combination": pd.to_datetime(['1/1/2015 00:00', '1/4/2016 10:00', '5/1/2016'])
})


def test_axis_dtype():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('years'), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    assert _locate_channel_dtype(chart, 'x') == 'temporal'


def test_axis_more_than_x_and_y():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('b'), color=alt.Color('c'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()


@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha')])
def test_axis(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(alt.X(x), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    xvmin, xvmax = ax.xaxis.get_view_interval()
    yvmin, yvmax = ax.yaxis.get_view_interval()
    assert int(xvmin) == int(0 if min(df_quant[x]) >= 0 else min(df_quant[x]))
    assert int(xvmax) == int(max(df_quant[x]) if max(df_quant[x]) >= 0 else 0)
    assert int(yvmin) == int(0 if min(df_quant[y]) >= 0 else min(df_quant[y]))
    assert int(yvmax) == int(max(df_quant[y]) if max(df_quant[y]) >= 0 else 0)


@pytest.mark.parametrize('x,y,zero', [('a', 'c', False), ('neg', 'alpha', False),
                                      ('a', 'c', True), ('neg', 'alpha', True)])
def test_axis_zero_quantitative(x, y, zero):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(zero=zero)),
        alt.Y(y, scale=alt.Scale(zero=zero))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)

    xticks = ax.xaxis.get_ticklocs()
    if min(df_quant[x]) >= 0 and zero:
        assert -.5 <= xticks[0] <= .5
    else:
        assert min(df_quant[x]) - 1 <= xticks[0] <= min(df_quant[x]) + 1
    if max(df_quant[x]) <= 0 and zero:
        assert -.5 <= xticks[-1] <= .5
    else:
        assert max(df_quant[x]) - 1 <= xticks[-1] <= max(df_quant[x]) + 1
    yticks = ax.yaxis.get_ticklocs()
    if min(df_quant[y]) >= 0 and zero:
        assert -.5 <= yticks[0] <= .5
    else:
        assert min(df_quant[y]) - 1 <= yticks[0] <= min(df_quant[y]) + 1
    if max(df_quant[y]) <= 0 and zero:
        assert -.5 <= yticks[-1] <= .5
    else:
        assert max(df_quant[y]) - 1 <= yticks[-1] <= max(df_quant[y]) + 1



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
    xvmin, xvmax = ax.xaxis.get_view_interval()
    yvmin, yvmax = ax.yaxis.get_view_interval()
    assert xvmin == x_dom[0]
    assert xvmax == x_dom[1]
    assert yvmin == y_dom[0]
    assert yvmax == y_dom[1]


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


def test_axis_fixed_ticks_quantitative():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3])),
        alt.Y('b', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3]))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    assert list(ax.xaxis.get_major_locator().tick_values(1, 1)) == [-1, 1, 1.5, 2.125, 3]


@pytest.mark.parametrize('x,y', [(1, 1), (4, 4), (9, 9)])
def test_axis_tickCount_quantitative(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('log', axis=alt.Axis(tickCount=x)), alt.Y('a', axis=alt.Axis(tickCount=y))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    xticks = ax.xaxis.get_ticklocs()
    buffer = 10  # TODO: make this number less magic
    assert x - buffer <= len(xticks) <= x + buffer
    yticks = ax.yaxis.get_ticklocs()
    assert y - buffer <= len(yticks) <= y + buffer



# Scale type tests


@pytest.mark.parametrize('column,type', [('log', 'log')])
def test_axis_scale_basic(column, type):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(column, scale=alt.Scale(type=type)),
        alt.Y('a')
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel("{} {}".format(column, type))
    ax.set_ylabel('a')
    plt.show()


@pytest.mark.parametrize('column,type,base,exponent', [('log','log',10, 1), ('log2', 'log', 2, 1)])
def test_axis_scale_type_x_quantitative(column, type, base, exponent):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(column, scale=alt.Scale(type=type, base=base, exponent=exponent)),
        alt.Y('a')
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel("{} {} {} {}".format(column, type, base, exponent))
    ax.set_ylabel('a')
    plt.show()


@pytest.mark.parametrize('column,type,base,exponent', [('log','log',10,1), ('log2','log',5,1)])
def test_axis_scale_type_y_quantitative(column, type, base, exponent):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a'),
        alt.Y(column, scale=alt.Scale(type=type, base=base, exponent=exponent))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel('a')
    ax.set_ylabel("{} {} {} {}".format(column, type, base, exponent))
    plt.show()

@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize('type', ['pow', 'sqrt', 'sequential', 'ordinal'])
def test_axis_scale_NotImplemented_quantitative(type):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', scale=alt.Scale(type=type)),
        alt.Y('a')
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
