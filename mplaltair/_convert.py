from ._data import _locate_channel_data

def _convert(chart):
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
        data = _locate_channel_data(chart, channel)
        mapping[_mpl_scatter_equivalent[channel](data)[0]] = _mpl_scatter_equivalent[channel](data)[1]

    return mapping


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


# mapping of altair channel to mpl kwargs for scatter()
_mpl_scatter_equivalent = {
    'x': _process_x,
    'y': _process_y,
    'x2': _process_not_implemented,  # NotImplementedError - ALT
    'y2': _process_not_implemented,  # NotImplementedError - ALT
    'color': _process_color,
    'fill': _process_fill,
    'opacity': _process_opacity,  # NotImplementedError for array-like opacities - MPL
    'shape': _process_shape,  # NotImplementedError - MPL
    'size': _process_size,
    'stroke': _process_not_implemented,  # NotImplementedError - ALT
}
