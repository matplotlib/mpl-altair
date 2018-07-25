import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
from mplaltair import convert
from .._axis import convert_axis, _set_limits, _set_tick_formatter, _set_tick_locator
from .._data import _locate_channel_dtype, _locate_channel_data, _locate_channel_axis, _locate_channel_scale, _convert_to_mpl_date
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

@pytest.mark.xfail(raises=TypeError)
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


def test_axis_temporal_domain():
    domain = ['2014-12-25', '2015-03-01']
    chart = alt.Chart(df).mark_point().encode(alt.X('a'), alt.Y('days'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)

    for channel in chart.to_dict()['encoding']:
        if channel in ['x', 'y']:
            chart_info = {'ax': ax, 'axis': channel,
                          'data': _locate_channel_data(chart, channel),
                          'dtype': _locate_channel_dtype(chart, channel)}
            if chart_info['dtype'] == 'temporal':
                chart_info['data'] = _convert_to_mpl_date(chart_info['data'])

            scale_info = _locate_channel_scale(chart, channel)
            if channel == 'y':
                scale_info['domain'] = domain
            axis_info = _locate_channel_axis(chart, channel)

            _set_limits(chart_info, scale_info)
            _set_tick_locator(chart_info, axis_info)
            _set_tick_formatter(chart_info, axis_info)
    plt.show()

@pytest.mark.parametrize('x,tickCount', [
    ('years', 1), ('years', 3), ('years', 5), ('years', 9), ('years', 10),
    # ('months', 1), ('months', 3), ('months', 5), ('months', 9), ('months', 10),
    # ('days', 1), ('days', 3), ('days', 5), ('days', 9), ('days', 10),
    ('hrs', 1), ('hrs', 3), ('hrs', 5), ('hrs', 9), ('hrs', 10),
    ('combination', 1), ('combination', 3), ('combination', 5), ('combination', 9), ('combination', 10)
])
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

def test_axis_temporal_values():
    vals = ['1/12/2015', '3/1/2015', '4/18/2015', '5/3/2015']
    chart = alt.Chart(df).mark_point().encode(alt.X('a'), alt.Y('months'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    for channel in chart.to_dict()['encoding']:
        if channel in ['x', 'y']:
            chart_info = {'ax': ax, 'axis': channel,
                          'data': _locate_channel_data(chart, channel),
                          'dtype': _locate_channel_dtype(chart, channel)}
            if chart_info['dtype'] == 'temporal':
                chart_info['data'] = _convert_to_mpl_date(chart_info['data'])

            scale_info = _locate_channel_scale(chart, channel)
            axis_info = _locate_channel_axis(chart, channel)
            if channel == 'y':
                axis_info['values'] = vals

            _set_limits(chart_info, scale_info)
            _set_tick_locator(chart_info, axis_info)
            _set_tick_formatter(chart_info, axis_info)
    ax.set_xlabel('a')
    ax.set_ylabel('months')
    fig.tight_layout()
    plt.show()

def test_axis_temporal_nice():
    pass

def test_axis_temporal_type():
    pass


df_tz = pd.DataFrame({
    'a': [1, 2, 3, 4, 5],
    'utc': pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00', '1/1/2015 04:00', '1/1/2015 05:00'], utc=True),
    'no_utc': pd.to_datetime(['1/1/2015 01:00', '1/1/2015 02:00', '1/1/2015 03:00', '1/1/2015 04:00', '1/1/2015 05:00']),
    'tz': pd.date_range('1/1/2015', periods=5, freq='H', tz='US/Eastern'),
    'no_tz': pd.date_range('1/1/2015', periods=5, freq='H')
})

@pytest.mark.parametrize('x', ['utc:T', 'no_utc:T', 'tz:T', 'no_tz:T'])
def test_axis_temporal_timezone(x):
    chart = alt.Chart(df_tz).mark_point().encode(alt.X(x), alt.Y('a'))
    mapping = convert(chart)
    fig, ax = plt.subplots()
    ax.scatter(**mapping)
    convert_axis(ax, chart)
    ax.set_xlabel(x)
    ax.set_ylabel('a')
    fig.tight_layout()
    plt.show()
