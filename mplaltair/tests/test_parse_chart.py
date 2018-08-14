import pytest
import altair as alt
import pandas as pd
import mplaltair.parse_chart as parse_chart
from .._data import _convert_to_mpl_date

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
    chart = parse_chart.ChartMetadata(chart)
    for channel in chart.encoding:
        data = chart.encoding[channel].data
        if chart.encoding[channel].type == 'temporal':
            assert list(data) == list(_convert_to_mpl_date(df[column].values))
        else:
            assert list(data) == list(df[column].values)


@pytest.mark.parametrize("column", ['a', 'b', 'c', 'combination'])
def test_data_shorthand_quantitative(column):
    chart = alt.Chart(df).mark_point().encode(alt.X(column))
    chart = parse_chart.ChartMetadata(chart)
    for channel in chart.encoding:
        data = chart.encoding[channel].data
        if chart.encoding[channel].type == 'temporal':
            assert list(data) == list(_convert_to_mpl_date(df[column].values))
        else:
            assert list(data) == list(df[column].values)


@pytest.mark.parametrize("column", ['a', 'b', 'c'])
def test_data_aggregate_quantitative_fail(column):
    """"'Passes' if it raises a NotImplementedError"""
    chart = alt.Chart(df).mark_point().encode(alt.X(field=column, type='quantitative', aggregate='average'))
    with pytest.raises(NotImplementedError):
        chart = parse_chart.ChartMetadata(chart)


def test_data_timeUnit_shorthand_temporal_fail():
    chart = alt.Chart(df).mark_point().encode(alt.X('month(combination):T'))
    with pytest.raises(NotImplementedError):
        chart = parse_chart.ChartMetadata(chart)


def test_data_timeUnit_field_temporal_fail():
    """"'Passes' if it raises a NotImplementedError"""
    chart = alt.Chart(df).mark_point().encode(alt.X(field='combination', type='temporal', timeUnit='month'))
    with pytest.raises(NotImplementedError):
        chart = parse_chart.ChartMetadata(chart)


# _locate_channel_dtype() tests

@pytest.mark.parametrize('column, expected', [
    ('a:Q', 'quantitative'), ('nom:N', 'nominal'), ('ord:O', 'ordinal'), ('combination:T', 'temporal')
])
def test_data_dtype(column, expected):
    chart = alt.Chart(df).mark_point().encode(alt.X(column))
    chart = parse_chart.ChartMetadata(chart)
    for channel in chart.encoding:
        assert chart.encoding[channel].type == expected


def test_data_dtype_fail():
    """"'Passes' if it raises a NotImplementedError"""
    chart = alt.Chart(df).mark_point().encode(opacity=alt.value(.5))
    with pytest.raises(NotImplementedError):
        chart = parse_chart.ChartMetadata(chart)