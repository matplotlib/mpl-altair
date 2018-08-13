import altair as alt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from mplaltair import convert
from .._axis import convert_axis
from parse_chart import ChartMetadata
import pytest

df_quant = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, -3],
    "s": [50, 100, 200.0], "alpha": [0, .5, .8], "shape": [1, 2, 3], "fill": [1, 2, 3],
    "neg": [-3, -4, -5], 'log': [11, 100, 1000], 'log2': [1, 3, 5],
    "years": pd.to_datetime(['1/1/2015', '1/1/2016', '1/1/2017'])
})

df_temp = pd.DataFrame({
    "a": [1, 2, 3, 4, 5],
    "years": pd.to_datetime(['1/1/2015', '1/1/2016', '1/1/2017', '1/1/2018', '1/1/2019']),
    "months": pd.to_datetime(['1/1/2015', '2/1/2015', '3/1/2015', '4/1/2015', '5/1/2015']),
    "days": pd.to_datetime(['1/1/2015', '1/2/2015', '1/3/2015', '1/4/2015', '1/5/2015']),
    "hrs": pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00', '1/1/2015 04:00', '1/1/2015 05:00']),
    "combination": pd.to_datetime(['1/1/2015 00:00', '1/4/2016 10:00', '5/1/2016', '5/1/2016 10:10', '3/3/2016'])
})


@pytest.mark.xfail(raises=TypeError)
def test_invalid_temporal():
    chart = alt.Chart(df_temp).mark_point().encode(alt.X('a:T'))
    convert(chart)


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
def test_axis_more_than_x_and_y():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('b'), color=alt.Color('c'))
    fig, ax = convert(chart)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('df,x,y', [(df_quant, 'a', 'c'), (df_quant, 'neg', 'alpha'),
                                    (df_temp, 'months', 'years'), (df_temp, 'years', 'months'), (df_temp, 'months', 'combination')])
def test_axis(df, x, y):
    chart = alt.Chart(df).mark_point().encode(alt.X(x), alt.Y(y))
    fig, ax = convert(chart)
    return fig


@pytest.mark.xfail(raises=NotImplementedError)
def test_axis_set_tick_formatter_fail():
    """TODO: Remove this test after merge with ordinal/nominal axis conversion.
     This test is just for temporary coverage purposes."""
    from .._axis import _set_tick_formatter
    _, ax = plt.subplots()
    chart = ChartMetadata(alt.Chart(df_quant).mark_point().encode('a:N', 'c:O'))
    _set_tick_formatter(chart.encoding['x'], ax)


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('x,y,zero', [('a', 'c', False), ('neg', 'alpha', False),
                                      ('a', 'c', True), ('neg', 'alpha', True)])
def test_axis_zero_quantitative(x, y, zero):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(x, scale=alt.Scale(zero=zero)),
        alt.Y(y, scale=alt.Scale(zero=zero))
    )
    fig, ax = convert(chart)
    return fig
    # plt.show()


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize(
    'df, x,y,x_dom,y_dom',
    [(df_quant, 'a', 'c', [0.5, 4], [-5, 10]), (df_quant, 'neg', 'alpha', [-6, -2], [0, 1]),
     (df_temp, 'days', 'hrs', ['2014-12-25', '2015-03-01'], ['2015-01-01', '2015-01-03']),
     (df_temp, 'a', 'days', [0.5, 4], [alt.DateTime(year=2014, month="Dec", date=25),
                                       alt.DateTime(year=2015, month="March", date=1)])]
)
def test_axis_domain(df, x, y, x_dom, y_dom):
    chart = alt.Chart(df).mark_point().encode(
        alt.X(x, scale=alt.Scale(domain=x_dom)),
        alt.Y(y, scale=alt.Scale(domain=y_dom))
    )
    fig, ax = convert(chart)
    return fig


@pytest.mark.xfail(raises=NotImplementedError)
def test_axis_unaggregated_quantitative():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a', scale=alt.Scale(domain="unaggregated")),
        alt.Y('c', scale=alt.Scale(domain="unaggregated"))
    )
    convert(chart)


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('df,y,vals', [
    (df_quant, 'b', [-1, 1, 1.5, 2.125, 3]),
    (df_temp, 'months', [alt.DateTime(year=2015, month=1, date=12), alt.DateTime(year=2015, month=4, date=18),
                         alt.DateTime(year=2015, month=5, date=3)])
])
def test_axis_values(df, y, vals):
    chart = alt.Chart(df).mark_point().encode(
        alt.X('a', axis=alt.Axis(values=[-1, 1, 1.5, 2.125, 3])),
        alt.Y(y, axis=alt.Axis(values=vals))
    )
    fig, ax = convert(chart)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('df,x,tickCount', [(df_quant, 'log', 1), (df_quant, 'log', 4), (df_quant, 'log', 9),
                                            (df_temp, 'years', 1), (df_temp, 'years', 4), (df_temp, 'years', 9),
                                            (df_temp, 'hrs', 1), (df_temp, 'hrs', 4), (df_temp, 'hrs', 9),
                                            (df_temp, 'combination', 1), (df_temp, 'combination', 4), (df_temp, 'combination', 9)])
def test_axis_tickCount(df, x, tickCount):
    chart = alt.Chart(df).mark_point().encode(
        alt.X(x, axis=alt.Axis(tickCount=tickCount)), alt.Y('a', axis=alt.Axis(tickCount=tickCount))
    )
    fig, ax = convert(chart)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('df,column,scale_type', [(df_quant, 'log', 'log'), (df_temp, 'years', 'time')])
def test_axis_scale_basic(df, column, scale_type):
    chart = alt.Chart(df).mark_point().encode(
        alt.X(column, scale=alt.Scale(type=scale_type)),
        alt.Y('a')
    )
    fig, ax = convert(chart)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('column,type,base,exponent', [('log','log',10, 1), ('log2', 'log', 2, 1)])
def test_axis_scale_type_x_quantitative(column, type, base, exponent):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X(column, scale=alt.Scale(type=type, base=base, exponent=exponent)),
        alt.Y('a')
    )
    fig, ax = convert(chart)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('column,type,base,exponent', [('log', 'log', 10, 1), ('log2', 'log', 5, 1)])
def test_axis_scale_type_y_quantitative(column, type, base, exponent):
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('a'),
        alt.Y(column, scale=alt.Scale(type=type, base=base, exponent=exponent))
    )
    fig, ax = convert(chart)
    plt.show()
    return fig


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize('df, x, type', [(df_quant, 'a', 'pow'), (df_quant, 'a', 'sqrt'), (df_temp, 'months', 'utc'),
                                         (df_quant, 'a', 'sequential'), (df_quant, 'a', 'ordinal')])
def test_axis_scale_NotImplemented_quantitative(df, x, type):
    chart = alt.Chart(df).mark_point().encode(
        alt.X(x, scale=alt.Scale(type=type)),
        alt.Y('a')
    )
    convert(chart)


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
@pytest.mark.parametrize('df,x,y,format_x,format_y', [
    (df_quant, 'c', 'b', '-.2g', '+.3g'),
])
def test_axis_formatter(df, x, y, format_x, format_y):
    chart = alt.Chart(df).mark_point().encode(
        alt.X(x, axis=alt.Axis(format=format_x)),
        alt.Y(y, axis=alt.Axis(format=format_y))
    )
    fig, ax = convert(chart)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_axis')
def test_axis_formatter_temporal():
    """Note: this test is separate from the other test_axis_formatter test because the parametrization created issues
    with the filename for the image comparison test."""
    chart = alt.Chart(df_temp).mark_point().encode(
        alt.X('months:T', axis=alt.Axis(format='%b %Y')),
        alt.Y('hrs:T', axis=alt.Axis(format='%H:%M:%S'))
    )
    fig, ax = convert(chart)
    return fig


@pytest.mark.xfail(raises=ValueError)
def test_axis_formatter_fail():
    chart = alt.Chart(df_quant).mark_point().encode(
        alt.X('c', axis=alt.Axis(format='-$.2g')),
        alt.Y('b', axis=alt.Axis(format='+.3r'))
    )
    convert(chart)
