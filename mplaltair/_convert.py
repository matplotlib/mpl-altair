# mapping of altair channel to mpl kwargs for scatter()
_mpl_scatter_equivalent = {
    'x': (lambda d: _process_x(d)),
    'y': (lambda d: _process_y(d)),
    'x2': (lambda d: _process_not_implemented(d)),  # NotImplementedError - ALT
    'y2': (lambda d: _process_not_implemented(d)),  # NotImplementedError - ALT
    'color': (lambda d: _process_color(d)),
    'fill': (lambda d: _process_fill(d)),
    'opacity': (lambda d: _process_opacity(d)),  # NotImplementedError for array-like opacities - MPL
    'shape': (lambda d: _process_shape(d)),  # NotImplementedError - MPL
    'size': (lambda d: _process_size(d)),
    'stroke': (lambda d: _process_not_implemented(d)),  # NotImplementedError - ALT
}


def convert_quantitative(chart):
    """Convert quantitative Altair encodings to their Matplotlib equivalents


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

    for channel in chart.to_dict()['encoding']:  # Need chart to get dictionary of channels from the encoding
        data = _locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
        mapping[_mpl_scatter_equivalent[channel](data)[0]] = _mpl_scatter_equivalent[channel](data)[1]

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

    if channel.get('value'):  # from the value version of the channel
        return channel.get('value')
    elif channel.get('aggregate'):
        return _aggregate_channel()
    elif channel.get('field'):
        return data[channel.get('field')].values
    else:
        raise ValueError("Cannot find data for the channel")


def _aggregate_channel():
    raise NotImplementedError


def _process_x(data):
    return "x", data


def _process_y(data):
    return "y", data


def _process_color(data):
    return "c", data


def _process_fill(data):
    return "c", data


def _process_opacity(data):
    if not isinstance(data, (float, int)):
        raise NotImplementedError
    else:
        return "alpha", data


def _process_shape(data):
    raise NotImplementedError


def _process_size(data):
    return "s", data


def _process_not_implemented(data):
    raise NotImplementedError
