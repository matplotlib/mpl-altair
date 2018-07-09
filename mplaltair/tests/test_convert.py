import pytest

import altair as alt
import pandas as pd

from .._convert import convert

df = pd.DataFrame({'quant': [1, 1.5, 2], 'ord': [0, 1, 2], 'nom': ['A', 'B', 'C']})

@pytest.mark.parametrize('channel', ['quant', 'ord', 'nom'])
def test_convert_x_success(channel):
    chart_spec = alt.Chart(df).encode(x=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df[channel].values)

def test_convert_x_fail():
    chart_spec = alt.Chart(df).encode(x='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.parametrize('channel', ['quant', 'ord', 'nom'])
def test_convert_y_success(channel):
    chart_spec = alt.Chart(df).encode(y=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['y']) == list(df[channel].values)

def test_convert_y_fail():
    chart_spec = alt.Chart(df).encode(y='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.parametrize('channel', ['quant', 'ord'])
def test_convert_color_success(channel):
    chart_spec = alt.Chart(df).encode(color=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df[channel].values)

def test_convert_color_success_nominal():
    chart_spec = alt.Chart(df).encode(color='nom').mark_point()
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

def test_convert_color_fail():
    chart_spec = alt.Chart(df).encode(color='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.parametrize('channel', ['quant', 'ord'])
def test_convert_fill(channel):
    chart_spec = alt.Chart(df).encode(fill=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df[channel].values)

def test_convert_fill_success_nominal():
    chart_spec = alt.Chart(df).encode(fill='nom').mark_point()
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

def test_convert_fill_fail():
    chart_spec = alt.Chart(df).encode(fill='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.parametrize('channel', ['quant', 'ord'])
def test_convert_size_success(channel):
    chart_spec = alt.Chart(df).encode(size=channel).mark_point()
    mapping = convert(chart_spec)
    assert list(mapping['s']) == list(df[channel].values)

def test_convert_size_success_nominal():
    chart_spec = alt.Chart(df).encode(size='nom').mark_point()
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

def test_convert_size_fail():
    chart_spec = alt.Chart(df).encode(size='b:N').mark_point()
    with pytest.raises(KeyError):
        convert(chart_spec)
