
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

def _convert(chart):
    """Convert an altair encoding to a Matplotlib figure


    Parameters
    ----------
    chart : parse_chart.ChartMetadata
        Data and metadata for the Altair chart

    Returns
    -------
    mapping : dict
        Mapping from parts of the encoding to the Matplotlib artists.  This is
        for later customization.
    """
    mapping = {}


    for enc_channel in chart.encoding:
        if not _allowed_ranged_marks(enc_channel, chart.mark):
            raise ValueError("Ranged encoding channels like x2, y2 not allowed for Mark: {}".format(chart.mark))

    for k, channel in chart.encoding.items():
        mapping[_mappings[k](channel.type, channel.data)[0]] = _mappings[k](channel.type, channel.data)[1]

    return mapping
