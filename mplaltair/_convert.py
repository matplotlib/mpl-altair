import matplotlib.dates as mdates
import numpy as np
from ._data import _locate_channel_data, _locate_channel_dtype, _convert_to_mpl_date

def _allowed_ranged_marks(enc_channel, mark):
    """TODO: DOCS
    """
    return mark in ['area', 'bar', 'rect', 'rule'] if enc_channel in ['x2', 'y2'] else True

def _process_x(dtype, data):
    """Returns the MPL encoding equivalent for Altair x channel
    """
    return ('x', data)


def _process_y(dtype, data):
    """Returns the MPL encoding equivalent for Altair y channel
    """
    return ('y', data)


def _process_x2(dtype, data):
    """Returns the MPL encoding equivalent for Altair x2 channel
    """
    raise NotImplementedError


def _process_y2(dtype, data):
    """Returns the MPL encoding equivalent for Altair y2 channel
    """
    raise NotImplementedError


def _process_color(dtype, data):
    """Returns the MPL encoding equivalent for Altair color channel
    """
    if dtype == 'quantitative':
        return ('c', data)
    elif dtype == 'nominal':
        raise NotImplementedError
    elif dtype == 'ordinal':
        return ('c', data)
    else:  # temporal
        return ('c', data)


def _process_fill(dtype, data):
    """Returns the MPL encoding equivalent for Altair fill channel
    """
    return _process_color(dtype, data)


def _process_shape(dtype, data):
    """Returns the MPL encoding equivalent for Altair shape channel
    """
    raise NotImplementedError


def _process_opacity(dtype, data):
    """Returns the MPL encoding equivalent for Altair opacity channel
    """
    raise NotImplementedError


def _process_size(dtype, data):
    """Returns the MPL encoding equivalent for Altair size channel
    """
    if dtype == 'quantitative':
        return ('s', data)
    elif dtype == 'nominal':
        raise NotImplementedError
    elif dtype == 'ordinal':
        return ('s', data)
    elif dtype == 'temporal':
        raise NotImplementedError


def _process_stroke(dtype, data):
    """Returns the MPL encoding equivalent for Altair stroke channel
    """
    raise NotImplementedError


_mappings = {
    'x': _process_x,
    'y': _process_y,
    'x2': _process_x2,
    'y2': _process_y2,
    'color': _process_color,
    'fill': _process_fill,
    'shape': _process_shape,
    'opacity': _process_opacity,
    'size': _process_size,
    'stroke': _process_stroke,
}

# _line_mapping = {
#     'x': lambda d: ('x', d),
#     'y': lambda d: ('y', d),
#     'args': lambda x, y: [x, y]
# }

def _convert(chart):
    """Convert an altair encoding to a Matplotlib figure


    Parameters
    ----------
    chart
        The Altair chart.

    Returns
    -------
    mapping : dict
        Mapping from parts of the encoding to the Matplotlib artists.  This is
        for later customization.
    """
    mapping = {}

    if not chart.to_dict().get('encoding'):
        raise ValueError("Encoding not provided with the chart specification")

    for enc_channel, enc_spec in chart.to_dict()['encoding'].items():
        if not _allowed_ranged_marks(enc_channel, chart.to_dict()['mark']):
            raise ValueError("Ranged encoding channels like x2, y2 not allowed for Mark: {}".format(chart['mark']))

    for channel in chart.to_dict()['encoding']:
        data = _locate_channel_data(chart, channel)
        dtype = _locate_channel_dtype(chart, channel)

        mapping[_mappings[channel](dtype, data)[0]] = _mappings[channel](dtype, data)[1]

    #     if chart.mark in ['point', 'circle', 'square']:
    #         mapping[_mappings[channel](dtype, data)[0]] = _mappings[channel](dtype, data)[1]
    #     elif chart.mark == 'line' and channel in ['x', 'y']:
    #         mapping[_line_mapping[channel](data)[0]] = _line_mapping[channel](data)[1]
    #
    # if chart.mark == 'line':
    #     mapping['args'] = _line_mapping['args'](mapping['x'], mapping['y'])  # plot() doesn't take kwargs for x and y
    
    return mapping
