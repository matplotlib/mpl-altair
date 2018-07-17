import altair as alt
import pandas as pd
import mplaltair._data as _data
import pytest

df = pd.DataFrame({
    "a": [1, 2, 3, 4, 5], "b": [1.1, 2.2, 3.3, 4.4, 5.5], "c": [1, 2.2, 3, 4.4, 5],
    "nom": ['a', 'b', 'c', 'd', 'e'], "ord": [1, 2, 3, 4, 5],
    "years": pd.date_range('01/01/2015', periods=5, freq='Y'), "months": pd.date_range('1/1/2015', periods=5, freq='M'),
    "days": pd.date_range('1/1/2015', periods=5, freq='D'), "hrs": pd.date_range('1/1/2015', periods=5, freq='H'),
    "combination": pd.to_datetime(['1/1/2015', '1/1/2015 10:00:00', '1/2/2015 00:00', '1/4/2016 10:00', '5/1/2016']),
    "quantitative": [1.1, 2.1, 3.1, 4.1, 5.1]
})


# _locate_channel_data() tests

def test_data_field():
    chart = alt.Chart(df).mark_point().encode(alt.X(field='combination', type='temporal'))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)
    assert list(data) == list(df['combination'].values)


def test_data_shorthand():
    chart = alt.Chart(df).mark_point().encode(alt.X('combination'))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)
    assert list(data) == list(df['combination'].values)


@pytest.mark.xfail(raises=NotImplementedError)
def test_data_timeUnit_shorthand():
    chart = alt.Chart(df).mark_point().encode(alt.X('month(combination):T'))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)


@pytest.mark.xfail(raises=NotImplementedError)
def test_data_timeUnit_field():
    chart = alt.Chart(df).mark_point().encode(alt.X(field='combination', type='temporal', timeUnit='month'))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)


@pytest.mark.xfail
def test_data_aggregate_temporal():
    chart = alt.Chart(df).mark_point().encode(alt.X(field='years', type='temporal', aggregate='average'))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)


def test_data_value_redundant():
    """This test is redundant after merging with convert-numeric"""
    chart = alt.Chart(df).mark_point().encode(alt.X('years'), opacity=alt.value(0.5))
    _data._locate_channel_data(chart, 'opacity')


# _locate_channel_dtype() tests

@pytest.mark.parametrize('column, expected', [
    ('a:Q', 'quantitative'), ('nom:N', 'nominal'), ('ord:O', 'ordinal'), ('combination:T', 'temporal')
])
def test_data_dtype(column, expected):
    chart = alt.Chart(df).mark_point().encode(alt.X(column))
    for channel in chart.to_dict()['encoding']:
        dtype = _data._locate_channel_dtype(chart, channel)
    assert dtype == expected


@pytest.mark.xfail(raises=NotImplementedError)
def test_data_dtype_fail():
    chart = alt.Chart(df).mark_point().encode(opacity=alt.value(.5))
    for channel in chart.to_dict()['encoding']:
        dtype = _data._locate_channel_dtype(chart, channel)
    assert dtype == 'quantitative'
