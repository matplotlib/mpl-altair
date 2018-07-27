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
    "years": pd.to_datetime(['1/1/2015', '1/1/2016', '1/1/2017'])
})


def test_axis_dtype():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('years'), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    assert _locate_channel_dtype(chart, 'x') == 'temporal'


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
def test_axis_more_than_x_and_y():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('b'), color=alt.Color('c'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    # plt.show()
    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('x,y', [('a', 'c'), ('neg', 'alpha')])
def test_axis(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(alt.X(x), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    fig.tight_layout()
    return fig

@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
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
    fig.tight_layout()
    return fig



@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
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
    fig.tight_layout()
    return fig


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


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
def test_axis_fixed_ticks_quantitative():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3])),
        alt.Y('b', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3]))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('x,y', [(1, 1), (4, 4), (9, 9)])
def test_axis_tickCount_quantitative(x, y):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('log', axis=alt.Axis(tickCount=x)), alt.Y('a', axis=alt.Axis(tickCount=y))
    )
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    fig.tight_layout()
    return fig



# Scale type tests

@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
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
    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
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
    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
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
    fig.tight_layout()
    return fig

@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
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
