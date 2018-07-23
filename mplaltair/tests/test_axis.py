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
    "years": pd.to_datetime(['1/1/2015', '1/1/2016', '1/1/2017']),
    "months": pd.to_datetime(['1/1/2015', '2/1/2015', '3/1/2015']),
    "days": pd.to_datetime(['1/1/2015', '1/2/2015', '1/3/2015']),
    "hrs": pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00']),
    # "years": pd.date_range('01/01/2015', periods=3, freq='Y'), "months": pd.date_range('1/1/2015', periods=3, freq='M'),
    # "days": pd.date_range('1/1/2015', periods=3, freq='D'), "hrs": pd.date_range('1/1/2015', periods=3, freq='H'),
    "combination": pd.to_datetime(['1/1/2015 00:00', '1/4/2016 10:00', '5/1/2016'])
})

@pytest.mark.skip(reason="in test_axis_temporal")
@pytest.mark.xfail(raises=AttributeError)
def test_invalid_temporal():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a:T'))
    fig, ax = plt.subplots()
    convert_axis(ax, chart)

def test_axis_dtype():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('years'), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    assert _locate_channel_dtype(chart, 'x') == 'temporal'

@pytest.mark.skip
def test_axis_more_than_x_and_y():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('b'), color=alt.Color('c'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

# @pytest.mark.skip
@pytest.mark.parametrize('x,y', [
    ('a', 'c'), ('neg', 'alpha'),
    ('months', 'a'), ('a', 'months'), ('a', 'combination')])
def test_axis(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(alt.X(x), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.show()

@pytest.mark.skip(reason="in test_axis_temporal")
@pytest.mark.parametrize('y', ['years', 'months', 'days', 'hrs', 'combination'])
def test_axis_temporal_y(y):
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel('a')
    ax.set_ylabel(y)
    fig.tight_layout()
    plt.show()

@pytest.mark.skip(reason="in test_axis_temporal")
@pytest.mark.parametrize('x', ['years', 'months', 'days', 'hrs', 'combination'])
def test_axis_temporal_x(x):
    chart = alt.Chart(df_quant).mark_point().encode(alt.X(x), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel('a')
    fig.tight_layout()
    plt.show()

# @pytest.mark.skip
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
    ax.set_xlabel("Zero {}".format(zero))
    ax.set_ylabel("Zero {}".format(zero))
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
def test_axis_fixed_ticks_quantitative():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3])),
        alt.Y('b', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3]))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    plt.show()

# @pytest.mark.skip
@pytest.mark.parametrize('x,y', [(1, 1), (4, 4), (9, 9)])
def test_axis_tickCount_quantitative(x, y):
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


# Scale type tests

# @pytest.mark.skip
@pytest.mark.parametrize('column,type', [('log', 'log'), ('a', 'pow')])
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

# @pytest.mark.skip
@pytest.mark.parametrize('column,type,base,exponent', [('log','log',10, 1), ('log2', 'log', 2, 1),
                                                       ('a','pow',10, .5), ('log','pow',10,2), ('a','sqrt',10,1)])
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

# @pytest.mark.skip
@pytest.mark.parametrize('column,type,base,exponent', [('log','log',10,1), ('log2','log',5,1),
                                                       ('a','pow',10,.5), ('log','pow',10,2), ('a','sqrt',10,1)])
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
@pytest.mark.parametrize('type', ['time', 'utc', 'sequential', 'ordinal'])
def test_axis_scale_NotImplemented(type):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', scale=alt.Scale(type=type)),
        alt.Y('a')
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
