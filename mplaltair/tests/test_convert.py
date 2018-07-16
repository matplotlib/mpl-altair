import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt
import pandas as pd
import mplaltair._convert as convert
import pytest

df_temporal = pd.DataFrame({
    "years": pd.date_range('01/01/2015', periods=5, freq='Y'), "months": pd.date_range('1/1/2015', periods=5, freq='M'),
    "days": pd.date_range('1/1/2015', periods=5, freq='D'), "hrs": pd.date_range('1/1/2015', periods=5, freq='H'),
    "combination": pd.to_datetime(['1/1/2015', '1/1/2015 10:00:00', '1/2/2015 00:00', '1/4/2016 10:00', '5/1/2016']),
    "quantitative": [1.1, 2.1, 3.1, 4.1, 5.1]
})


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_x(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['x']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_y(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Y(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['y']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_x2_y2(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X2(column), alt.Y2(column))
    convert.convert_temporal(chart)


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_color(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Color(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['c']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_fill(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Fill(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['c']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_opacity(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Opacity(column))
    convert.convert_temporal(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_shape(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Shape(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['s']) == list(mdates.date2num(df_temporal[column].values))


@pytest.mark.xfail(raises=NotImplementedError, reason="Dates would need to be normalized for the size.")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_size(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Size(column))
    convert.convert_temporal(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well defined in Altair")
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_stroke(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Stroke(column))
    convert.convert_temporal(chart)


@pytest.mark.parametrize("channel", [alt.Color("years"), alt.Fill("years")])
def test_temporal_scatter(channel):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X("years"), channel)
    mapping = convert.convert_temporal(chart)
    mapping['y'] = df_temporal['quantitative'].values
    plt.scatter(**mapping)
    plt.show()


@pytest.mark.xfail(raises=NotImplementedError, reason="specifying timeUnit is not supported yet")
def test_timeUnit():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X('date(combination)'))
    convert.convert_temporal(chart)


@pytest.mark.xfail(raises=AttributeError, reason="convert_temporal only converts temporal encodings")
def test_convert_temporal_fail():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X('quantitative'))
    convert.convert_temporal(chart)
