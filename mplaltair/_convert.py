import matplotlib
import altair

from ._data import _normalize_data

def _process_data_mappings(f):
    """Decorator for processing the data inside the encoding spec

    This is meant to resolve aggregates and other artefacts
    """
    def g(enc_spec, data):
        # FIXME: This should be replaced by a proper aggregation handling
        if enc_spec.get("aggregate"):
            raise NotImplementedError
        
        return f(enc_spec, data)
    return g

def _allowed_ranged_marks(enc_channel, mark):
    """TODO: DOCS
    """
    return mark in ['area', 'bar', 'rect', 'rule'] if enc_channel in ['x2', 'y2'] else True

def _get_column(enc_spec, data):
    try:
        field = enc_spec.get('field')
        if not field:
            raise ValueError("Field not specified in the encoding x")
        return data[enc_spec['field']]
    except KeyError:
        raise KeyError("{} does not match any column in the data".format(enc_spec))

@_process_data_mappings
def _process_x(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair x channel
    """
    dx = _get_column(enc_spec, data)
    return ('x', dx)

@_process_data_mappings
def _process_y(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair y channel
    """
    dy = _get_column(enc_spec, data)
    return ('y', dy)

@_process_data_mappings
def _process_x2(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair x2 channel
    """
    raise NotImplementedError

@_process_data_mappings
def _process_y2(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair y2 channel
    """
    raise NotImplementedError

@_process_data_mappings
def _process_color(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair color channel
    """
    dc = _get_column(enc_spec, data)

    dtype = enc_spec['type']
    if dtype == 'quantitative':
        return ('c', dc)
    elif dtype == 'nominal':
        raise NotImplementedError
    elif dtype == 'ordinal':
        return ('c', dc)
    elif dtype == 'temporal':
        raise NotImplementedError

@_process_data_mappings
def _process_fill(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair fill channel
    """
    return _process_color(enc_spec, data)

@_process_data_mappings
def _process_shape(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair shape channel
    """
    raise NotImplementedError

@_process_data_mappings
def _process_opacity(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair opacity channel
    """
    raise NotImplementedError

@_process_data_mappings
def _process_size(enc_spec, data):
    """Returns the MPL encoding equivalent for Altair size channel
    """
    ds = _get_column(enc_spec, data)

    dtype = enc_spec['type']
    if dtype == 'quantitative':
        return ('s', ds)
    elif dtype == 'nominal':
        raise NotImplementedError
    elif dtype == 'ordinal':
        return ('s', ds)
    elif dtype == 'temporal':
        raise NotImplementedError

@_process_data_mappings
def _process_stroke(enc_spec, data):
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

def convert(spec):
    """Convert an altair encoding to a Matplotlib figure


    Parameters
    ----------
    encoding
        The Altair encoding of the plot.

    figure : matplotib.figure.Figure, optional
        # TODO: generalize this to 'thing that supports gridspec slicing?

    Returns
    -------
    figure : matplotlib.figure.Figure
        The Figure with all artists in it (ready to be saved or shown)

    mapping : dict
        Mapping from parts of the encoding to the Matplotlib artists.  This is
        for later customization.
    """
    mapping = {}

    spec = _normalize_data(spec)
    data = spec['data']
    
    encoding = spec.get('encoding')
    mark = spec.get('mark')

    if not encoding:
        raise ValueError("Encoding not provided with the chart specification")

    for enc_channel, enc_spec in encoding.items():
        if not _allowed_ranged_marks(enc_channel, mark):
            raise ValueError("Ranged encoding channels like x2, y2 not allowed for Mark: {}".format(spec['mark']))

        mpl_encoding_channel, data = _mappings[enc_channel](enc_spec, data)
        mapping[mpl_encoding_channel] = data
    
    return mapping
