import json
import pytest

import altair as alt
import pandas as pd

from .._convert import convert

df = pd.DataFrame({'quant': [1, 1.5, 2], 'ord': [0, 1, 2], 'nom': ['A', 'B', 'C']})

def test_convert_x_success_quantitative():
    chart_spec = json.loads(alt.Chart(df).encode(x='quant').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df.quant.values)

def test_convert_x_success_ordinal():
    chart_spec = json.loads(alt.Chart(df).encode(x='ord').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df.ord.values)

def test_convert_x_success_nominal():
    chart_spec = json.loads(alt.Chart(df).encode(x='nom').mark_point().to_json())
    mapping = convert(chart_spec)
    assert list(mapping['x']) == list(df.nom.values)

def test_convert_x_fail():
    chart_spec = json.loads(alt.Chart(df).encode(x='b:N').mark_point().to_json())
    with pytest.raises(KeyError):
        convert(chart_spec)
