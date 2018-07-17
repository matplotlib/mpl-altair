import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt
import pandas as pd
from mplaltair import convert
import pytest

df_temporal = pd.DataFrame({
    "years": pd.date_range('01/01/2015', periods=5, freq='Y'), "months": pd.date_range('1/1/2015', periods=5, freq='M'),
    "days": pd.date_range('1/1/2015', periods=5, freq='D'), "hrs": pd.date_range('1/1/2015', periods=5, freq='H'),
    "combination": pd.to_datetime(['1/1/2015', '1/1/2015 10:00:00', '1/2/2015 00:00', '1/4/2016 10:00', '5/1/2016']),
    "quantitative": [1.1, 2.1, 3.1, 4.1, 5.1]
})


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_x_temporal_success(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X(column))
    mapping = convert(chart)
    assert list(mapping['x']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.xfail(raises=KeyError)
def test_convert_x_fail():
    chart = alt.Chart(df_temporal).encode(x='b:N').mark_point()
    convert(chart)


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_y_temporal_success(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Y(column))
    mapping = convert(chart)
    assert list(mapping['y']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.xfail(raises=KeyError)
def test_convert_x_fail():
    chart = alt.Chart(df_temporal).encode(y='b:N').mark_point()
    convert(chart)


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_x2_y2_temporal_fail(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X2(column), alt.Y2(column))
    convert(chart)


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_color_temporal_success(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Color(column))
    mapping = convert(chart)
    assert list(mapping['c']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.xfail(raises=KeyError)
def test_convert_color_fail():
    chart = alt.Chart(df_temporal).encode(color='b:N').mark_point()
    convert(chart)


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_fill_temporal_success(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Fill(column))
    mapping = convert(chart)
    assert list(mapping['c']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.xfail(raises=KeyError)
def test_convert_fill_fail():
    chart = alt.Chart(df_temporal).encode(fill='b:N').mark_point()
    convert(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_opacity_temporal_fail(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Opacity(column))
    convert(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_shape_temporal_fail(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Shape(column))
    convert(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="Dates would need to be normalized for the size.")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_size_temoral_fail(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Size(column))
    convert(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well defined in Altair")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_convert_stroke_temporal_fail(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Stroke(column))
    convert(chart)


@pytest.mark.parametrize("channel", [alt.Color("years"), alt.Fill("years")])
def test_convert_scatter_temporal(channel):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X("years"), channel)
    mapping = convert(chart)
    mapping['y'] = df_temporal['quantitative'].values
    plt.scatter(**mapping)
    plt.show()


@pytest.mark.xfail(raises=NotImplementedError, reason="specifying timeUnit is not supported yet")
def test_timeUnit_fail():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X('date(combination)'))
    convert(chart)


@pytest.mark.xfail(raises=AttributeError, reason="convert_temporal only converts temporal encodings")
def test_convert_temporal_fail():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X('quantitative'))
    convert(chart)
