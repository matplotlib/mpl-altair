from urllib.request import urlopen
from urllib.error import HTTPError

import pandas as pd

_PD_READERS = {
    'json': pd.read_json,
    'csv': pd.read_csv
}

def _get_format(url):
    """Gives back the format of the file from url

    WARNING: It might break. Trying to find a better way.
    """
    return url.split('.')[-1]

def _fetch(url):
    """Downloads the file from the given url as a Pandas DataFrame

    Parameters
    ----------
    url : string
    URL of the file to be downloaded

    Returns
    -------
    pd.DataFrame
    Data in the format of a DataFrame

    Raises
    ------
    NotImplementedError
    Raises when an unsupported file format is given as an URL
    """
    try:
        ext = _get_format(url)
        reader = _PD_READERS[ext]
        df = reader(urlopen(url).read())
    except KeyError:
        raise NotImplementedError('File format not implemented')
    return df
