import pytest

import altair as alt
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mplaltair import convert
from mplaltair._convert import _convert
from mplaltair.parse_chart import ChartMetadata


df = pd.DataFrame({
    'quant': [1, 1.5, 2, 2.5, 3], 'ord': [0, 1, 2, 3, 4], 'nom': ['A', 'B', 'C', 'D', 'E'],
    "years": pd.date_range('01/01/2015', periods=5, freq='Y'), "months": pd.date_range('1/1/2015', periods=5, freq='M'),
    "days": pd.date_range('1/1/2015', periods=5, freq='D'), "hrs": pd.date_range('1/1/2015', periods=5, freq='H'),
    "combination": pd.to_datetime(['1/1/2015', '1/1/2015 10:00:00', '1/2/2015 00:00', '1/4/2016 10:00', '5/1/2016']),
    "quantitative": [1.1, 2.1, 3.1, 4.1, 5.1]
})

df_quant = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, 3],
    "s": [50, 100, 200.0], "alpha": [.1, .5, .8], "shape": [1, 2, 3], "fill": [1, 2, 3]
})


def test_encoding_not_provided():  # TODO: move to the parse_chart tests
    chart_spec = alt.Chart(df).mark_point()
    with pytest.raises(ValueError):
        chart = ChartMetadata(chart_spec)

def test_invalid_encodings():
    chart_spec = alt.Chart(df).encode(x2='quant').mark_point()
    chart = ChartMetadata(chart_spec)
    with pytest.raises(ValueError):
        _convert(chart)

@pytest.mark.xfail(raises=TypeError)
def test_invalid_temporal():  # TODO: move to parse_chart tests???
    chart = alt.Chart(df).mark_point().encode(alt.X('quant:T'))
    ChartMetadata(chart)

@pytest.mark.parametrize('channel', ['quant', 'ord', 'nom'])
def test_convert_x_success(channel):
    chart_spec = alt.Chart(df).encode(x=channel).mark_point()
    chart = ChartMetadata(chart_spec)
    mapping = _convert(chart)
    assert list(mapping['x']) == list(df[channel].values)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_x_success_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.X(column))
    chart = ChartMetadata(chart)
    mapping = _convert(chart)
    assert list(mapping['x']) == list(mdates.date2num(df[column].values))

def test_convert_x_fail():
    with pytest.raises(KeyError):
        chart_spec = ChartMetadata(alt.Chart(df).encode(x='b:N').mark_point())

@pytest.mark.parametrize('channel', ['quant', 'ord', 'nom'])
def test_convert_y_success(channel):
    chart_spec = ChartMetadata(alt.Chart(df).encode(y=channel).mark_point())
    mapping = _convert(chart_spec)
    assert list(mapping['y']) == list(df[channel].values)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_y_success_temporal(column):
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.Y(column)))
    mapping = _convert(chart)
    assert list(mapping['y']) == list(mdates.date2num(df[column].values))

def test_convert_y_fail():
    with pytest.raises(KeyError):
        chart_spec = ChartMetadata(alt.Chart(df).encode(y='b:N').mark_point())

@pytest.mark.xfail(raises=ValueError, reason="It doesn't make sense to have x2 and y2 on scatter plots")
def test_quantitative_x2_y2():
    chart = ChartMetadata(alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('b'), alt.X2('c'), alt.Y2('alpha')))
    _convert(chart)

@pytest.mark.xfail(raises=ValueError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_x2_y2_fail_temporal(column):
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.X2(column), alt.Y2(column)))
    _convert(chart)

@pytest.mark.parametrize('channel,dtype', [('quant','quantitative'), ('ord','ordinal')])
def test_convert_color_success(channel, dtype):
    chart_spec = ChartMetadata(alt.Chart(df).encode(color=alt.Color(field=channel, type=dtype)).mark_point())
    mapping = _convert(chart_spec)
    assert list(mapping['c']) == list(df[channel].values)

def test_convert_color_success_nominal():
    chart_spec = ChartMetadata(alt.Chart(df).encode(color='nom').mark_point())
    with pytest.raises(NotImplementedError):
        _convert(chart_spec)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_color_success_temporal(column):
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.Color(column)))
    mapping = _convert(chart)
    assert list(mapping['c']) == list(mdates.date2num(df[column].values))

def test_convert_color_fail():
    with pytest.raises(KeyError):
        chart_spec = ChartMetadata(alt.Chart(df).encode(color='b:N').mark_point())

@pytest.mark.parametrize('channel,type', [('quant', 'Q'), ('ord', 'O')])
def test_convert_fill(channel, type):
    chart_spec = ChartMetadata(alt.Chart(df).encode(fill='{}:{}'.format(channel, type)).mark_point())
    mapping = _convert(chart_spec)
    assert list(mapping['c']) == list(df[channel].values)

def test_convert_fill_success_nominal():
    chart_spec = ChartMetadata(alt.Chart(df).encode(fill='nom').mark_point())
    with pytest.raises(NotImplementedError):
        _convert(chart_spec)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_fill_success_temporal(column):
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.Fill(column)))
    mapping = _convert(chart)
    assert list(mapping['c']) == list(mdates.date2num(df[column].values))


def test_convert_fill_fail():
    with pytest.raises(KeyError):
        chart_spec = ChartMetadata(alt.Chart(df).encode(fill='b:N').mark_point())

@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
def test_quantitative_shape():
    chart = ChartMetadata(alt.Chart(df_quant).mark_point().encode(alt.Shape('shape')))
    mapping = _convert(chart)

@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_shape_fail_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Shape(column))
    convert(chart)

@pytest.mark.xfail(raises=NotImplementedError, reason="Merge: the dtype for opacity isn't assumed to be quantitative")
def test_quantitative_opacity_value():
    chart = ChartMetadata(alt.Chart(df_quant).mark_point().encode(opacity=alt.value(.5)))

@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
def test_quantitative_opacity_array():
    chart = ChartMetadata(alt.Chart(df_quant).mark_point().encode(alt.Opacity('alpha')))
    _convert(chart)

@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_opacity_fail_temporal(column):
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.Opacity(column)))
    _convert(chart)

@pytest.mark.parametrize('channel,type', [('quant', 'Q'), ('ord', 'O')])
def test_convert_size_success(channel, type):
    chart_spec = ChartMetadata(alt.Chart(df).encode(size='{}:{}'.format(channel, type)).mark_point())
    mapping = _convert(chart_spec)
    assert list(mapping['s']) == list(df[channel].values)

def test_convert_size_success_nominal():
    with pytest.raises(NotImplementedError):
        chart_spec = ChartMetadata(alt.Chart(df).encode(size='nom').mark_point())
        _convert(chart_spec)

def test_convert_size_fail():
    with pytest.raises(KeyError):
        chart_spec = ChartMetadata(alt.Chart(df).encode(size='b:N').mark_point())

@pytest.mark.xfail(raises=NotImplementedError, reason="Dates would need to be normalized for the size.")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_size_fail_temporal(column):
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.Size(column)))
    _convert(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well supported in Altair")
def test_quantitative_stroke():
    chart = ChartMetadata(alt.Chart(df_quant).mark_point().encode(alt.Stroke('fill')))
    _convert(chart)

@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well defined in Altair")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_stroke_fail_temporal(column):
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.Stroke(column)))
    _convert(chart)


# Aggregations

@pytest.mark.xfail(raises=NotImplementedError, reason="Aggregate functions are not supported yet")
def test_quantitative_x_count_y():
    df_count = pd.DataFrame({"a": [1, 1, 2, 3, 5], "b": [1.4, 1.4, 2.9, 3.18, 5.3]})
    chart = ChartMetadata(alt.Chart(df_count).mark_point().encode(alt.X('a'), alt.Y('count()')))


@pytest.mark.xfail(raises=NotImplementedError, reason="specifying timeUnit is not supported yet")
def test_timeUnit():
    chart = ChartMetadata(alt.Chart(df).mark_point().encode(alt.X('date(combination)')))

# Plots

chart_quant = alt.Chart(df_quant).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Color('c:Q'), alt.Size('s')
)
chart_fill_quant = alt.Chart(df_quant).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Fill('fill:Q')
)

@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_convert')
@pytest.mark.parametrize("chart", [chart_quant, chart_fill_quant])
def test_quantitative_scatter(chart):
    fig, ax = convert(chart)
    return fig

@pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_convert')
@pytest.mark.parametrize("channel", [alt.Color("years"), alt.Fill("years")])
def test_scatter_temporal(channel):
    chart = alt.Chart(df).mark_point().encode(
        alt.X("years"),
        alt.Y("quantitative"),
        channel
    )
    fig, ax = convert(chart)
    return fig


# Line plots
df_line = pd.DataFrame({
        'a': [1, 2, 3, 1, 2, 3, 1, 2, 3],
        'b': [3, 2, 1, 7, 8, 9, 4, 5, 6],
        'c': ['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'],
        'd': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'dates': ['1968-08-01', '1968-08-01', '1968-08-01', '2010-08-08', '2010-08-08', '2010-08-08', '2015-03-14', '2015-03-14', '2015-03-14']
    })


class TestLines(object):
    @pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_convert')
    def test_line(self):
        chart = alt.Chart(df_line).mark_line().encode(
            alt.X('a'),
            alt.Y('b'),
        )
        fig, _ = convert(chart)
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_convert')
    @pytest.mark.parametrize('x,y,s', [
        ('a:Q', 'b:Q', 'd:Q'),
        pytest.param('a:N', 'b:N', 'c:N', marks=pytest.mark.xfail(raises=NotImplementedError)),
        pytest.param('a:O', 'b:O', 'c:O', marks=pytest.mark.xfail(raises=NotImplementedError))
    ])
    def test_line_stroke(self, x, y, s):
        chart = alt.Chart(df_line).mark_line().encode(
            alt.X(x),
            alt.Y(y),
            alt.Stroke(s)
        )
        fig, _ = convert(chart)
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_convert')
    def test_line_color(self):
        chart = alt.Chart(df_line).mark_line().encode(
            alt.X('a'),
            alt.Y('b'),
            alt.Color('d')
        )
        fig, _ = convert(chart)
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_convert')
    @pytest.mark.parametrize('o', ['d:Q', 'c:O', 'dates:T'])
    def test_line_opacity(self, o):
        chart = alt.Chart(df_line).mark_line().encode(
            alt.X('a'),
            alt.Y('b'),
            alt.Opacity(o)
        )
        fig, ax = convert(chart)
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline_images/test_convert')
    @pytest.mark.parametrize('c,o', [('d:Q', 'd:Q'), ('c:N', 'c:O'), ('dates:T', 'dates:T')])
    def test_line_opacity_color(self, c, o):
        chart = alt.Chart(df_line).mark_line().encode(
            alt.X('a'),
            alt.Y('b'),
            alt.Color(c),
            alt.Opacity(o)
        )
        fig, ax = convert(chart)
        return fig


class TestBars(object):
    @pytest.mark.xfail(raises=NotImplementedError)
    def test_bar_fail(self):
        chart = alt.Chart(df_line).mark_bar().encode(
            alt.X('a'),
            alt.Y('b'),
        )
        convert(chart)
