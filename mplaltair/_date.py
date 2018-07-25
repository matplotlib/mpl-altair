import altair as alt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime
import collections


def convert_to_mpl_date(data):
    """Converts dates to matplotlib dates"""
    if hasattr(data, "values"):
        # unpack pandas series or dataframe
        data = data.values

    # TODO: parse both single values and sequences/iterables
    new_data = []
    for i in data:
        if isinstance(i, str):  # string format for dates
            new_data.append(mdates.datestr2num(i))
        elif isinstance(i, np.datetime64):  # sequence of datetimes, datetime64s
            new_data.append(mdates.date2num(i))
        elif isinstance(i, dict):  # Altair DateTime
            """Allowed formats (for domain):
            YYYY, 
            YYYY-MM(-01), YYYY-MM-DD, YYYY(-01)-DD, 
            ^ plus hh, hh:mm, hh:mm:ss, hh(:00):ss, (0):mm:ss
            Could turn dict into iso datetime string and then use dateutil.parser.isoparse() or datestr2num()
            """
            raise NotImplementedError
        else:
            raise ValueError

    return new_data