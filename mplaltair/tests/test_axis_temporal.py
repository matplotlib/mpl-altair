import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
from mplaltair import convert
from .._axis import convert_axis
import pytest

from vega_datasets import data

df = pd.DataFrame({
    "a": [1, 2, 3, 4, 5], "b": [1.2, 2.4, 3.8, 4.5, 5.2], "c": [7, 5, -3, 2, 0],
    "s": [50, 100, 75.0, 150, 200.0], "alpha": [0, .3, .5, .7, .8],
    "neg": [-3, -4, -5, -6, -7], 'log': [1, 11, 100, 1000, 1001], 'log2': [1, 3, 5, 9, 12],
    "years": pd.to_datetime(['1/1/2015', '1/1/2016', '1/1/2017', '1/1/2018', '1/1/2019']),
    "months": pd.to_datetime(['1/1/2015', '2/1/2015', '3/1/2015', '4/1/2015', '5/1/2015']),
    "days": pd.to_datetime(['1/1/2015', '1/2/2015', '1/3/2015', '1/4/2015', '1/5/2015']),
    "hrs": pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00', '1/1/2015 04:00', '1/1/2015 05:00']),
    # "years": pd.date_range('01/01/2015', periods=5, freq='Y'), "months": pd.date_range('1/1/2015', periods=5, freq='M'),
    # "days": pd.date_range('1/1/2015', periods=5, freq='D'), "hrs": pd.date_range('1/1/2015', periods=5, freq='H'),
    "combination": pd.to_datetime(['1/1/2015 00:00', '1/4/2016 10:00', '5/1/2016', '5/1/2016 10:10', '3/3/2016'])
})

df_nonstandard = pd.DataFrame({
    'a': [1, 2, 3],
    'c': ['2015-03-07 12:32:17', '2015-03-08 12:32:17', '2015-03-09 12:32:17'],
    'd': ['2015-03-15', '2015-03-16', '2015-03-17'],
    'e': pd.to_datetime(['1/4/2016 10:00', '5/1/2016 10:10', '3/3/2016'])
})
def test_nonstandard_date():
    chart = alt.Chart(df_nonstandard).mark_point().encode(alt.X('e:T'), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel('year')
    ax.set_ylabel('yield')
    plt.show()

@pytest.mark.xfail(raises=ValueError)
def test_invalid_temporal():
    chart = alt.Chart(df).mark_point().encode(alt.X('a:T'))
    fig, ax = plt.subplots()
    convert_axis(ax, chart)

@pytest.mark.parametrize('x,y', [('months', 'a'), ('a', 'months'), ('a', 'combination')])
def test_axis(x, y):
    chart = alt.Chart(df).mark_point().encode(alt.X(x), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.show()

@pytest.mark.parametrize('y', ['years', 'months', 'days', 'hrs', 'combination'])
def test_axis_temporal_y(y):
    chart = alt.Chart(df).mark_point().encode(alt.X('a'), alt.Y(y))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel('a')
    ax.set_ylabel(y)
    fig.tight_layout()
    plt.show()

@pytest.mark.parametrize('x', ['years', 'months', 'days', 'hrs', 'combination'])
def test_axis_temporal_x(x):
    chart = alt.Chart(df).mark_point().encode(alt.X(x), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel('a')
    fig.tight_layout()
    plt.show()

df_temp = pd.DataFrame({
    'a': [1, 2, 3, 4, 5],
    'utc': pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00', '1/1/2015 04:00', '1/1/2015 05:00'], utc=True),
    'no_utc': pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00', '1/1/2015 04:00', '1/1/2015 05:00']),
    'tz': pd.date_range('1/1/2015', periods=5, freq='H', tz='US/Eastern'),
    'no_tz': pd.date_range('1/1/2015', periods=5, freq='H')
})

@pytest.mark.parametrize('x', ['utc:T', 'no_utc:T', 'tz:T', 'no_tz:T'])
def test_axis_temporal_timezone(x):
    chart = alt.Chart(df_temp).mark_point().encode(alt.X(x), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel('a')
    fig.tight_layout()
    plt.show()

def test_axis_temporal_domain():
    pass

@pytest.mark.parametrize('x,tickCount', [('years', 1), ('months', 3), ('days', 5),
                                         ('hrs', 9), ('combination', 10)])
def test_axis_temporal_tickCount(x, tickCount):
    chart = alt.Chart(df).mark_point().encode(alt.X(x, axis=alt.Axis(tickCount=tickCount)), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel('a')
    fig.tight_layout()
    plt.show()

def test_axis_temporal_nice():
    pass

def test_axis_temporal_type():
    pass
