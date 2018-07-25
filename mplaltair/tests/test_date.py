from .._date import convert_to_mpl_date
import pytest
import pandas as pd
import altair as alt
import matplotlib.dates as mdates

df_nonstandard = pd.DataFrame({
    'a': [1, 2, 3],
    'c': ['2015-03-07 12:32:17', '2015-03-08 12:32:17', '2015-03-09 12:32:17'],
    'd': ['2015-03-15', '2015-03-16', '2015-03-17'],
    'e': pd.to_datetime(['1/4/2016 10:00', '5/1/2016 10:10', '3/3/2016'])
})

def test_str():
    assert list(convert_to_mpl_date(df_nonstandard['c'].values)) == list(mdates.datestr2num(df_nonstandard['c']))

def test_datetime64():
    assert list(convert_to_mpl_date(df_nonstandard['e'].values)) == list(mdates.date2num(df_nonstandard['e']))