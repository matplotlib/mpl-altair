import altair as alt
import pandas as pd
import mplaltair._data as _data
import pytest

df_quantitative = pd.DataFrame({
    "a": [1, 2, 3, 4, 5], "b": [1.1, 2.2, 3.3, 4.4, 5.5], "c": [1, 2.2, 3, 4.4, 5]
})


@pytest.mark.parametrize("column", ['a', 'b', 'c'])
def test_data_field_quantitative(column):
    chart = alt.Chart(df_quantitative).mark_point().encode(alt.X(field=column, type='quantitative'))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
    assert list(data) == list(df_quantitative[column].values)


@pytest.mark.parametrize("column", ['a', 'b', 'c'])
def test_data_shorthand_quantitative(column):
    chart = alt.Chart(df_quantitative).mark_point().encode(alt.X(column))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
    assert list(data) == list(df_quantitative[column].values)


def test_data_value_quantitative():
    chart = alt.Chart(df_quantitative).mark_point().encode(opacity=alt.value(0.5))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
    assert data == 0.5


@pytest.mark.parametrize("column", ['a', 'b', 'c'])
@pytest.mark.xfail(raises=NotImplementedError)
def test_data_aggregate_quantitative(column):
    chart = alt.Chart(df_quantitative).mark_point().encode(alt.X(field=column, type='quantitative', aggregate='average'))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)


@pytest.mark.xfail(raises=ValueError)
def test_data_unexpected_encoding():
    chart = alt.Chart(df_quantitative).mark_point().encode(alt.X('a'))
    _data._locate_channel_data({'unexpected': 'a', 'no_field': 'a', 'no_value': 'a'}, chart.data)