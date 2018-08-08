import pytest
import pandas as pd
from vega_datasets import data

from mplaltair import _utils

def test_get_format():
    assert _utils._get_format(data.cars.url) == 'json'

def test_fetch_success():
    assert type(_utils._fetch(data.cars.url)) == pd.DataFrame

def test_fetch_error():
    with pytest.raises(NotImplementedError):
        _utils._fetch('https://test.tld/dataset.tsv')
