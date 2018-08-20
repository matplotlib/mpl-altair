import altair as alt
import pandas as pd
import matplotlib.dates as mdates
import mplaltair._data as _data
import pytest
from vega_datasets import data


df = pd.DataFrame({
    "a": [1, 2, 3, 4, 5], "b": [1.1, 2.2, 3.3, 4.4, 5.5], "c": [1, 2.2, 3, 4.4, 5],
    "nom": ['a', 'b', 'c', 'd', 'e'], "ord": [1, 2, 3, 4, 5],
    "years": pd.date_range('01/01/2015', periods=5, freq='Y'), "months": pd.date_range('1/1/2015', periods=5, freq='M'),
    "days": pd.date_range('1/1/2015', periods=5, freq='D'), "hrs": pd.date_range('1/1/2015', periods=5, freq='H'),
    "combination": pd.to_datetime(['1/1/2015', '1/1/2015 10:00:00', '1/2/2015 00:00', '1/4/2016 10:00', '5/1/2016']),
    "quantitative": [1.1, 2.1, 3.1, 4.1, 5.1]
})


def test_data_list():
    chart = alt.Chart(pd.DataFrame({'a': [1], 'b': [2], 'c': [3]})).mark_point()
    _data._normalize_data(chart)
    assert type(chart.data) == pd.DataFrame

def test_data_url():
    chart = alt.Chart(data.cars.url).mark_point()
    _data._normalize_data(chart)
    assert type(chart.data) == pd.DataFrame

# test date conversion:

df_nonstandard = pd.DataFrame({
    'a': [1, 2, 3],
    'c': ['2015-03-07 12:32:17', '2015-03-08 12:32:17', '2015-03-09 12:32:17'],
    'd': ['2015-03-15', '2015-03-16', '2015-03-17'],
    'e': pd.to_datetime(['1/4/2016 10:00', '5/1/2016 10:10', '3/3/2016'])
})

def test_convert_to_mpl_str():
    assert list(_data._convert_to_mpl_date(df_nonstandard['c'].values)) == list(mdates.datestr2num(df_nonstandard['c']))

def test_convert_to_mpl_datetime64():
    assert list(_data._convert_to_mpl_date(df_nonstandard['e'].values)) == list(mdates.date2num(df_nonstandard['e']))

def test_convert_to_mpl_altair_datetime():
    dates = [alt.DateTime(year=2015, date=7).to_dict(), alt.DateTime(year=2015, month="March", date=20).to_dict()]
    assert list(_data._convert_to_mpl_date(dates)) == list(mdates.datestr2num(['2015-01-07', '2015-03-20']))

def test_convert_to_mpl_empty():
    assert _data._convert_to_mpl_date([]) == []

@pytest.mark.parametrize('date,expected', [
    (df_nonstandard['c'].values[0], mdates.datestr2num(df_nonstandard['c'].values[0])),
    (df_nonstandard['e'].values[0], mdates.date2num(df_nonstandard['e'].values[0])),
    (alt.DateTime(year=2015, month="March", date=7).to_dict(), mdates.datestr2num('2015-03-07'))
])
def test_convert_to_mpl_single_vals(date, expected):
    assert _data._convert_to_mpl_date(date) == expected

@pytest.mark.parametrize('date,expected', [
    (alt.DateTime(year=2015, month="March", date=7).to_dict(), '2015-03-07'),
    (alt.DateTime(year=2015, date=7).to_dict(), '2015-01-07'),
    (alt.DateTime(year=2015, month=3).to_dict(), '2015-03-01'),
    (alt.DateTime(year=2015, date=7, milliseconds=1).to_dict(), '2015-01-07 00:00:00.001'),
    pytest.param(alt.DateTime(day="Mon").to_dict(), '2015-01-07', marks=pytest.mark.xfail(raises=NotImplementedError)),
    pytest.param(alt.DateTime(year=2015, date=20, quarter=1).to_dict(), '2015-01-20', marks=pytest.mark.xfail(raises=NotImplementedError)),
    pytest.param(alt.DateTime(year=2015, date=20, utc=True).to_dict(), '2015-01-07', marks=pytest.mark.xfail(raises=NotImplementedError)),
    pytest.param(alt.DateTime(date=20).to_dict(), '2015-01-07', marks=pytest.mark.xfail(raises=KeyError)),
])
def test_altair_datetime(date, expected):
    assert mdates.date2num(_data._altair_DateTime_to_datetime(date)) == mdates.datestr2num(expected)
