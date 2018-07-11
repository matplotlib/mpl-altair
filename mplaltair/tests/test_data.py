import pytest
import pandas as pd
from vega_datasets import data
from .._data import _normalize_data
from .._exceptions import ValidationError

def test_data_list():
    spec = {
        "data": {
            "values": [{"a": 1, "b": 2}, {"c": 3, "d": 4}]

        }
    }
    assert type(_normalize_data(spec)["data"]) == pd.DataFrame

def test_data_url():
    spec = {
        "data": {
            "url": data.cars.url
        }
    }
    assert type(_normalize_data(spec)["data"]) == pd.DataFrame

def test_data_no_pass():
    spec = {}
    with pytest.raises(ValidationError):
        _normalize_data(spec)

def test_data_invalid():
    spec = {
        "data": {
            "source": "path"
        }
    }
    with pytest.raises(NotImplementedError):
        _normalize_data(spec)