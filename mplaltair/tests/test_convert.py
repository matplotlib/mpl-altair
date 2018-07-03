import matplotlib.pyplot as plt
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
    assert list(mapping['x']) == list(df_temporal[column].values)


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_y(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Y(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['y']) == list(df_temporal[column].values)


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_color(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Color(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['c']) == list(df_temporal[column].values)


@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_fill(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Fill(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['c']) == list(df_temporal[column].values)


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_opacity(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Opacity(column))
    convert.convert_temporal(chart)


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_shape(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Shape(column))
    convert.convert_temporal(chart)


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_size(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Size(column))
    mapping = convert.convert_temporal(chart)
    assert list(mapping['s']) == list(df_temporal[column].values)


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize("column", ["years", "months", "days", "hrs", "combination"])
def test_temporal_stroke(column):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.Stroke(column))
    convert.convert_temporal(chart)


@pytest.mark.parametrize("channel", [alt.Color("years"), alt.Fill("years")])
def test_temporal_scatter(channel):
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X("years"), alt.Y("quantitative"), channel)
    mapping = convert.convert_temporal(chart)
    plt.scatter(**mapping)
    plt.show()
