import pytest

import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from mplaltair import convert


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


def test_encoding_not_provided():
    chart_spec = alt.Chart(df).mark_point()
    with pytest.raises(ValueError):
        convert(chart_spec)

def test_invalid_encodings():
    chart_spec = alt.Chart(df).encode(x2='quant').mark_point()
    with pytest.raises(ValueError):
        convert(chart_spec)

@pytest.mark.xfail(raises=AttributeError)
def test_invalid_temporal():
    chart = alt.Chart(df).mark_point().encode(alt.X('quant:T'))
    convert(chart)

@pytest.mark.parametrize('channel', ['quant', 'ord', 'nom'])
def test_convert_x_success(channel):
    chart_spec = alt.Chart(df).encode(x=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df[channel].values)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_x_success_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.X(column))
    mapping = convert(chart)
    assert list(mapping['x']) == list(mdates.date2num(df[column].values))

def test_convert_x_fail():
    chart_spec = alt.Chart(df).encode(x='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.parametrize('channel', ['quant', 'ord', 'nom'])
def test_convert_y_success(channel):
    chart_spec = alt.Chart(df).encode(y=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['y']) == list(df[channel].values)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_y_success_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Y(column))
    mapping = convert(chart)
    assert list(mapping['y']) == list(mdates.date2num(df[column].values))

def test_convert_y_fail():
    chart_spec = alt.Chart(df).encode(y='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.xfail(raises=ValueError, reason="It doesn't make sense to have x2 and y2 on scatter plots")
def test_quantitative_x2_y2():
    chart = alt.Chart(df_quant).mark_point().encode(alt.X('a'), alt.Y('b'), alt.X2('c'), alt.Y2('alpha'))
    convert(chart)

@pytest.mark.xfail(raises=ValueError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_x2_y2_fail_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.X2(column), alt.Y2(column))
    convert(chart)

@pytest.mark.parametrize('channel,dtype', [('quant','quantitative'), ('ord','ordinal')])
def test_convert_color_success(channel, dtype):
    chart_spec = alt.Chart(df).encode(color=alt.Color(field=channel, type=dtype)).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df[channel].values)

def test_convert_color_success_nominal():
    chart_spec = alt.Chart(df).encode(color='nom').mark_point()
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_color_success_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Color(column))
    mapping = convert(chart)
    assert list(mapping['c']) == list(mdates.date2num(df[column].values))

def test_convert_color_fail():
    chart_spec = alt.Chart(df).encode(color='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.parametrize('channel', ['quant', 'ord'])
def test_convert_fill(channel):
    chart_spec = alt.Chart(df).encode(fill=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df[channel].values)

def test_convert_fill_success_nominal():
    chart_spec = alt.Chart(df).encode(fill='nom').mark_point()
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_fill_success_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Fill(column))
    mapping = convert(chart)
    assert list(mapping['c']) == list(mdates.date2num(df[column].values))

def test_convert_fill_fail():
    chart_spec = alt.Chart(df).encode(fill='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
def test_quantitative_shape():
    chart = alt.Chart(df_quant).mark_point().encode(alt.Shape('shape'))
    mapping = convert(chart)
    assert list(mapping['marker']) == list(df_quant['shape'].values)

@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_shape_fail_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Shape(column))
    mapping = convert(chart)
    assert list(mapping['s']) == list(mdates.date2num(df[column].values))

@pytest.mark.xfail(raises=NotImplementedError, reason="Merge: the dtype for opacity isn't assumed to be quantitative")
def test_quantitative_opacity_value():
    chart = alt.Chart(df_quant).mark_point().encode(opacity=alt.value(.5))
    mapping = convert(chart)
    assert mapping['alpha'] == 0.5

@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
def test_quantitative_opacity_array():
    chart = alt.Chart(df_quant).mark_point().encode(alt.Opacity('alpha'))
    convert(chart)

@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_opacity_fail_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Opacity(column))
    convert(chart)

@pytest.mark.parametrize('channel,dtype', [('quant','quantitative'), ('ord', 'ordinal')])
def test_convert_size_success(channel, dtype):
    chart_spec = alt.Chart(df).encode(size=alt.Size(field=channel, type=dtype)).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['s']) == list(df[channel].values)

def test_convert_size_success_nominal():
    chart_spec = alt.Chart(df).encode(size='nom').mark_point()
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

def test_convert_size_fail():
    chart_spec = alt.Chart(df).encode(size='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.xfail(raises=NotImplementedError, reason="Dates would need to be normalized for the size.")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_size_fail_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Size(column))
    convert(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well supported in Altair")
def test_quantitative_stroke():
    chart = alt.Chart(df_quant).mark_point().encode(alt.Stroke('fill'))
    convert(chart)

@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well defined in Altair")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_stroke_fail_temporal(column):
    chart = alt.Chart(df).mark_point().encode(alt.Stroke(column))
    convert(chart)


# Aggregations

@pytest.mark.xfail(raises=NotImplementedError, reason="Aggregate functions are not supported yet")
def test_quantitative_x_count_y():
    df_count = pd.DataFrame({"a": [1, 1, 2, 3, 5], "b": [1.4, 1.4, 2.9, 3.18, 5.3]})
    chart = alt.Chart(df_count).mark_point().encode(alt.X('a'), alt.Y('count()'))
    mapping = convert(chart)
    assert list(mapping['x']) == list(df_count['a'].values)
    assert list(mapping['y']) == list(df_count.groupby(['a']).count().values)

@pytest.mark.xfail(raises=NotImplementedError, reason="specifying timeUnit is not supported yet")
def test_timeUnit():
    chart = alt.Chart(df).mark_point().encode(alt.X('date(combination)'))
    convert(chart)

# Plots

chart_quant = alt.Chart(df_quant).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Color('c:Q'), alt.Size('s')
)
chart_fill_quant = alt.Chart(df_quant).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Fill('fill:Q')
)

@pytest.mark.parametrize("chart", [chart_quant, chart_fill_quant])
def test_quantitative_scatter(chart):
    mapping = convert(chart)
    plt.scatter(**mapping)
    plt.show()

@pytest.mark.parametrize("channel", [alt.Color("years"), alt.Fill("years")])
def test_scatter_temporal(channel):
    chart = alt.Chart(df).mark_point().encode(alt.X("years"), channel)
    mapping = convert(chart)
    mapping['y'] = df['quantitative'].values
    plt.scatter(**mapping)
    plt.show()
