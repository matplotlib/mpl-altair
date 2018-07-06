import json
import pytest

import altair as alt
import pandas as pd

from .._convert import convert

df = pd.DataFrame({'quant': [1, 1.5, 2], 'ord': [0, 1, 2], 'nom': ['A', 'B', 'C']})

@pytest.mark.xfail
def test_convert_x_success_quantitative():
    chart_spec = json.loads(alt.Chart(df).encode(x='quant').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df.quant.values)

@pytest.mark.xfail
def test_convert_x_success_ordinal():
    chart_spec = json.loads(alt.Chart(df).encode(x='ord').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df.ord.values)

@pytest.mark.xfail
def test_convert_x_success_nominal():
    chart_spec = json.loads(alt.Chart(df).encode(x='nom').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df.nom.values)

@pytest.mark.xfail
def test_convert_x_fail():
    chart_spec = json.loads(alt.Chart(df).encode(x='b:N').mark_point().to_json())
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.xfail
def test_convert_y_success_quantitative():
    chart_spec = json.loads(alt.Chart(df).encode(y='quant').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['y']) == list(df.quant.values)

@pytest.mark.xfail
def test_convert_y_success_ordinal():
    chart_spec = json.loads(alt.Chart(df).encode(y='ord').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['y']) == list(df.ord.values)

@pytest.mark.xfail
def test_convert_y_success_nominal():
    chart_spec = json.loads(alt.Chart(df).encode(y='nom').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['y']) == list(df.nom.values)

@pytest.mark.xfail
def test_convert_y_fail():
    chart_spec = json.loads(alt.Chart(df).encode(y='b:N').mark_point().to_json())
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.xfail
def test_convert_color_success_quantitative():
    chart_spec = json.loads(alt.Chart(df).encode(color='quant').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df.quant.values)

@pytest.mark.xfail
def test_convert_color_success_ordinal():
    chart_spec = json.loads(alt.Chart(df).encode(color='ord').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df.ord.values)

@pytest.mark.xfail
def test_convert_color_success_nominal():
    chart_spec = json.loads(alt.Chart(df).encode(color='nom').mark_point().to_json())
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

@pytest.mark.xfail
def test_convert_color_fail():
    chart_spec = json.loads(alt.Chart(df).encode(color='b:N').mark_point().to_json())
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.xfail
def test_convert_fill_success_quantitative():
    chart_spec = json.loads(alt.Chart(df).encode(fill='quant').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df.quant.values)

@pytest.mark.xfail
def test_convert_fill_success_ordinal():
    chart_spec = json.loads(alt.Chart(df).encode(fill='ord').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['c']) == list(df.ord.values)

@pytest.mark.xfail
def test_convert_fill_success_nominal():
    chart_spec = json.loads(alt.Chart(df).encode(fill='nom').mark_point().to_json())
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

@pytest.mark.xfail
def test_convert_fill_fail():
    chart_spec = json.loads(alt.Chart(df).encode(fill='b:N').mark_point().to_json())
    with pytest.raises(KeyError):
        convert(chart_spec)

@pytest.mark.xfail
def test_convert_size_success_quantitative():
    chart_spec = json.loads(alt.Chart(df).encode(size='quant').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['s']) == list(df.quant.values)

@pytest.mark.xfail
def test_convert_size_success_ordinal():
    chart_spec = json.loads(alt.Chart(df).encode(size='ord').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['s']) == list(df.ord.values)

@pytest.mark.xfail
def test_convert_size_success_nominal():
    chart_spec = json.loads(alt.Chart(df).encode(size='nom').mark_point().to_json())
    with pytest.raises(NotImplementedError):
        convert(chart_spec)

@pytest.mark.xfail
def test_convert_size_fail():
    chart_spec = json.loads(alt.Chart(df).encode(size='b:N').mark_point().to_json())
    with pytest.raises(KeyError):
        convert(chart_spec)
