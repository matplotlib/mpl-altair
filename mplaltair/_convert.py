import matplotlib.dates as mdates

_mpl_temporal_equivalent = {
    'x': (lambda d: _process_temporal_x(d)),
    'y': (lambda d: _process_temporal_y(d)),
    'x2': (lambda d: _process_temporal_not_implemented(d)),  # NotImplementedError - ALT
    'y2': (lambda d: _process_temporal_not_implemented(d)),  # NotImplementedError - ALT
    'color': (lambda d: _process_temporal_color(d)),
    'fill': (lambda d: _process_temporal_fill(d)),
    'opacity': (lambda d: _process_temporal_opacity(d)),  # NotImplementedError - MPL
    'shape': (lambda d: _process_temporal_shape(d)),  # NotImplementedError - MPL
    'size': (lambda d: _process_temporal_size(d)),  # NotImplementedError - MPL
    'stroke': (lambda d: _process_temporal_not_implemented(d)),  # NotImplementedError - ALT
}


def convert_temporal(chart):
    """Convert temporal Altair encodings to their Matplotlib equivalents

    Parameters
    ----------
    chart
        The Altair chart

    Returns
    -------
    mapping : dict
        Mapping from parts of the encoding to the Matplotlib equivalent.

    """

    mapping = {}

    for channel in chart.to_dict()['encoding']:
        data = _locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
        try:
            data = mdates.date2num(data)  # Convert dates to Matplotlib dates
        except AttributeError:
            raise
        mapping[_mpl_temporal_equivalent[channel](data)[0]] = _mpl_temporal_equivalent[channel](data)[1]

    return mapping


def _locate_channel_data(channel, data):
    """Locates data used for each channel

    Parameters
    ----------
    channel
        The encoding channel from the Altair chart
    data : Pandas DataFrame
        Data from the Altair chart

    Returns
    -------
    A numpy ndarray containing the data used for the channel

    """

    if channel.get('value'):
        return channel.get('value')
    elif channel.get('aggregate'):
        return _aggregate_channel()
    elif channel.get('timeUnit'):
        return _handle_timeUnit()
    elif channel.get('field'):
        return data[channel.get('field')].values
    else:
        raise ValueError("Cannot find data for the channel")


def _aggregate_channel():
    raise NotImplementedError


def _handle_timeUnit():
    raise NotImplementedError


def _process_temporal_x(data):
    return "x", data


def _process_temporal_y(data):
    return "y", data


def _process_temporal_color(data):
    return "c", data


def _process_temporal_fill(data):
    return "c", data


def _process_temporal_opacity(data):
    raise NotImplementedError


def _process_temporal_shape(data):
    raise NotImplementedError


def _process_temporal_size(data):
    raise NotImplementedError


def _process_temporal_not_implemented(data):
    raise NotImplementedError
