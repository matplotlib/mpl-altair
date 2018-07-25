from ._exceptions import ValidationError
import matplotlib.dates as mdates
import numpy as np

def _locate_channel_dtype(chart, channel):
    """Locates dtype used for each channel
        Parameters
        ----------
        chart
            The Altair chart
        channel
            The Altair channel being examined

        Returns
        -------
        A string representing the data type from the Altair chart ('quantitative', 'ordinal', 'numeric', 'temporal')
        """

    channel_val = chart.to_dict()['encoding'][channel]
    if channel_val.get('type'):
        return channel_val.get('type')
    else:
        # TODO: find some way to deal with 'value' so that, opacity, for instance, can be plotted with a value defined
        if channel_val.get('value'):
            raise NotImplementedError
        raise NotImplementedError


def _locate_channel_data(chart, channel):
    """Locates data used for each channel

    Parameters
    ----------
    chart
        The Altair chart
    channel
        The Altair channel being examined

    Returns
    -------
    A numpy ndarray containing the data used for the channel

    Raises
    ------
    ValidationError
        Raised when the specification does not contain any data attribute

    """

    channel_val = chart.to_dict()['encoding'][channel]
    if channel_val.get('value'):
        return channel_val.get('value')
    elif channel_val.get('aggregate'):
        return _aggregate_channel()
    elif channel_val.get('timeUnit'):
        return _handle_timeUnit()
    else:  # field is required if the above are not present.
        return chart.data[channel_val.get('field')].values


def _aggregate_channel():
    raise NotImplementedError


def _handle_timeUnit():
    raise NotImplementedError


def _locate_channel_scale(chart, channel):
    """Locates the channel's scale information. Note that this implementation is a little
    different (and a little cleaner) than the other locate functions in this module.

    Parameters
    ----------
    chart
        The Altair chart
    channel
        The Altair channel being examined

    Returns
    -------
    A dictionary with the scale information
    """
    channel_val = chart.to_dict()['encoding'][channel]
    if channel_val.get('scale'):
        return channel_val.get('scale')
    else:
        return {}


def _locate_channel_axis(chart, channel):
    """Locates the channel's scale information. Note that this implementation is a little
    different (and a little cleaner) than the other locate functions in this module.

    Parameters
    ----------
    chart
        The Altair chart
    channel
        The Altair channel being examined

    Returns
    -------
    A dictionary with the axis information
    """
    channel_val = chart.to_dict()['encoding'][channel]
    if channel_val.get('axis'):
        return channel_val.get('axis')
    else:
        return {}

def _convert_to_mpl_date(data):
    """Converts datetime, datetime64, strings, and Altair DateTime objects to matplotlib dates"""

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
            raise TypeError

    return new_data