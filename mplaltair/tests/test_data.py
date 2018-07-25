import altair as alt
import pandas as pd
import matplotlib.dates as mdates
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

@pytest.mark.parametrize("column, dtype", [
    ('a', 'quantitative'), ('b', 'quantitative'), ('c', 'quantitative'), ('combination', 'temporal')
])
def test_data_field_quantitative(column, dtype):
    chart = alt.Chart(df).mark_point().encode(alt.X(field=column, type=dtype))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)
    assert list(data) == list(df[column].values)


@pytest.mark.parametrize("column", ['a', 'b', 'c', 'combination'])
def test_data_shorthand_quantitative(column):
    chart = alt.Chart(df).mark_point().encode(alt.X(column))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)
    assert list(data) == list(df[column].values)


def test_data_value_quantitative():
    chart = alt.Chart(df).mark_point().encode(opacity=alt.value(0.5))
    for channel in chart.to_dict()['encoding']:
        data = _data._locate_channel_data(chart, channel)
    assert data == 0.5


@pytest.mark.parametrize("column", ['a', 'b', 'c'])
def test_data_aggregate_quantitative_fail(column):
    """"'Passes' if it raises a NotImplementedError"""
    chart = alt.Chart(df).mark_point().encode(alt.X(field=column, type='quantitative', aggregate='average'))
    for channel in chart.to_dict()['encoding']:
        with pytest.raises(NotImplementedError):
            data = _data._locate_channel_data(chart, channel)


def test_data_timeUnit_shorthand_temporal_fail():
    chart = alt.Chart(df).mark_point().encode(alt.X('month(combination):T'))
    for channel in chart.to_dict()['encoding']:
        with pytest.raises(NotImplementedError):
            data = _data._locate_channel_data(chart, channel)


def test_data_timeUnit_field_temporal_fail():
    """"'Passes' if it raises a NotImplementedError"""
    chart = alt.Chart(df).mark_point().encode(alt.X(field='combination', type='temporal', timeUnit='month'))
    for channel in chart.to_dict()['encoding']:
        with pytest.raises(NotImplementedError):
            data = _data._locate_channel_data(chart, channel)


# _locate_channel_dtype() tests

@pytest.mark.parametrize('column, expected', [
    ('a:Q', 'quantitative'), ('nom:N', 'nominal'), ('ord:O', 'ordinal'), ('combination:T', 'temporal')
])
def test_data_dtype(column, expected):
    chart = alt.Chart(df).mark_point().encode(alt.X(column))
    for channel in chart.to_dict()['encoding']:
        dtype = _data._locate_channel_dtype(chart, channel)
    assert dtype == expected


def test_data_dtype_fail():
    """"'Passes' if it raises a NotImplementedError"""
    chart = alt.Chart(df).mark_point().encode(opacity=alt.value(.5))
    for channel in chart.to_dict()['encoding']:
        with pytest.raises(NotImplementedError):
            dtype = _data._locate_channel_dtype(chart, channel)
    assert dtype == 'quantitative'


# TODO: _locate_channel_scale() tests

# TODO: _locate channel_axis() tests


# test date conversion:

df_nonstandard = pd.DataFrame({
    'a': [1, 2, 3],
    'c': ['2015-03-07 12:32:17', '2015-03-08 12:32:17', '2015-03-09 12:32:17'],
    'd': ['2015-03-15', '2015-03-16', '2015-03-17'],
    'e': pd.to_datetime(['1/4/2016 10:00', '5/1/2016 10:10', '3/3/2016'])
})

def test_str():
    assert list(_data._convert_to_mpl_date(df_nonstandard['c'].values)) == list(mdates.datestr2num(df_nonstandard['c']))

def test_datetime64():
    assert list(_data._convert_to_mpl_date(df_nonstandard['e'].values)) == list(mdates.date2num(df_nonstandard['e']))
