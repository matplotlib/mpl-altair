import matplotlib.dates as mdates
from ._data import _locate_channel_data


def _convert(chart):
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
        data = _locate_channel_data(chart, channel)
        try:
            data = mdates.date2num(data)  # Convert dates to Matplotlib dates
        except AttributeError:
            raise
        mapping[_mpl_temporal_equivalent[channel](data)[0]] = _mpl_temporal_equivalent[channel](data)[1]

    return mapping


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


_mpl_temporal_equivalent = {
    'x': _process_temporal_x,
    'y': _process_temporal_y,
    'x2': _process_temporal_not_implemented,  # NotImplementedError - ALT
    'y2': _process_temporal_not_implemented,  # NotImplementedError - ALT
    'color': _process_temporal_color,
    'fill': _process_temporal_fill,
    'opacity': _process_temporal_opacity,  # NotImplementedError - MPL
    'shape': _process_temporal_shape,  # NotImplementedError - MPL
    'size': _process_temporal_size,  # NotImplementedError - MPL
    'stroke': _process_temporal_not_implemented,  # NotImplementedError - ALT
}
