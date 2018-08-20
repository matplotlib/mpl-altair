import pandas as pd
from ._exceptions import ValidationError
from ._utils import _fetch
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from datetime import datetime
import numpy as np


def _normalize_data(chart):
    """Converts the data to a Pandas dataframe

    Parameters
    ----------
    chart : altair.Chart
    The vega-lite specification in json format

    Returns
    -------
    None

    Raises
    ------
    ValidationError
    Raised when the specification does not contain any data attribute

    NotImplementedError
    Raised when the data specification has an unsupported data source
    """

    spec = chart.to_dict()

    if spec['data'].get('url'):
        df = pd.DataFrame(_fetch(spec['data']['url']))
    elif spec['data'].get('values'):
        return
    else:
        raise NotImplementedError('Given data specification is unsupported at the moment.')

    chart.data = df


def _convert_to_mpl_date(data):
    """Converts datetime, datetime64, strings, and Altair DateTime objects to Matplotlib dates.

    Parameters
    ----------
    data : datetime.datetime, numpy.datetime64, str, Altair DateTime, or sequences of any of these
        The data to be converted to a Matplotlib date

    Returns
    -------
    new_data : list
        A list containing the converted date(s)
    """

    if cbook.iterable(data) and not isinstance(data, str) and not isinstance(data, dict):
        if len(data) == 0:
            return []
        else:
            return np.asarray([_convert_to_mpl_date(i) for i in data])
    else:
        if isinstance(data, str):  # string format for dates
            data = mdates.datestr2num(data)
        elif isinstance(data, np.datetime64):  # sequence of datetimes, datetime64s
            data = mdates.date2num(data)
        elif isinstance(data, dict):  # Altair DateTime
            data = mdates.date2num(_altair_DateTime_to_datetime(data))
        else:
            raise TypeError
        return data


def _altair_DateTime_to_datetime(dt):
    """Convert dictionary representation of an Altair DateTime to datetime object

    Parameters
    ----------
    dt : dict
        The dictionary representation of the Altair DateTime object to be converted.

    Returns
    -------
    A datetime object
    """
    MONTHS = {'Jan': 1, 'January': 1, 'Feb': 2, 'February': 2, 'Mar': 3, 'March': 3, 'Apr': 4, 'April': 4,
              'May': 5, 'Jun': 6, 'June': 6, 'Jul': 7, 'July': 7, 'Aug': 8, 'August': 8, 'Sep': 9, 'Sept': 9,
              'September': 9, 'Oct': 10, 'October': 10, 'Nov': 11, 'November': 11, 'Dec': 12, 'December': 12}

    alt_to_datetime_kw_mapping = {'date': 'day', 'hours': 'hour', 'milliseconds': 'microsecond', 'minutes': 'minute',
                       'month': 'month', 'seconds': 'second', 'year': 'year'}

    datetime_kwargs = {'year': 0, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}

    if 'day' in dt or 'quarter' in dt:
        raise NotImplementedError
    if 'year' not in dt:
        raise KeyError('A year must be provided.')
    if 'month' not in dt:
        dt['month'] = 1  # Default to January
    else:
        if isinstance(dt['month'], str):  # convert from str to number form for months
            dt['month'] = MONTHS[dt['month']]
    if 'date' not in dt:
        dt['date'] = 1  # Default to the first of the month
    if 'milliseconds' in dt:
        dt['milliseconds'] = dt['milliseconds']*1000  # convert to microseconds
    if 'utc' in dt:
        raise NotImplementedError("mpl-altair currently doesn't support timezones.")

    for k, v in dt.items():
        datetime_kwargs[alt_to_datetime_kw_mapping[k]] = v

    return datetime(**datetime_kwargs)
