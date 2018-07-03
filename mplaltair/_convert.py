from altair.utils.core import parse_shorthand
from altair.utils.schemapi import Undefined

_mpl_temporal_equivalent = {
    'x': (lambda d: _process_x(d)),
    'y': (lambda d: _process_y(d)),
    'x2': (lambda d: _process_not_implemented(d)),  # NotImplementedError - ALT
    'y2': (lambda d: _process_not_implemented(d)),  # NotImplementedError - ALT
    'color': (lambda d: _process_color(d)),
    'fill': (lambda d: _process_fill(d)),
    'opacity': (lambda d: _process_opacity(d)),  # NotImplementedError for array-like opacities - MPL
    'shape': (lambda d: _process_shape(d)),  # NotImplementedError - MPL
    'size': (lambda d: _process_size(d)),  # NotImplementedError - MPL
    'stroke': (lambda d: _process_not_implemented(d)),  # NotImplementedError - ALT
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

    for encoding_channel in chart.to_dict()['encoding']:
        channel = chart.encoding[encoding_channel]
        data = _locate_channel_data(channel, chart.data)
        mapping[_mpl_temporal_equivalent[encoding_channel](data)[0]] = _mpl_temporal_equivalent[encoding_channel](data)[1]

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

    if hasattr(channel, "value") and channel.value is not Undefined:  # from the value version of the channel
        return channel.value
    elif hasattr(channel, "aggregate") and channel.aggregate is not Undefined:
        return _aggregate_channel()
    elif hasattr(channel, "field") and channel.field is not Undefined:
        return data[channel.field].values
    elif hasattr(channel, "shorthand") and channel.shorthand is not Undefined:
        parsed = parse_shorthand(channel.shorthand, data)
        if "aggregate" in parsed:
            return _aggregate_channel()
        elif "field" in parsed:
            return data[parsed['field']].values
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
    raise NotImplementedError


def _process_shape(data):
    raise NotImplementedError


def _process_size(data):
    raise NotImplementedError


def _process_not_implemented(data):
    raise NotImplementedError
