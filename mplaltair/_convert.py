from altair.utils.core import parse_shorthand
from altair.utils.schemapi import Undefined

_mappings = {
    'x': lambda e, d: _process_x(e, d),
    'y': lambda e, d: _process_y(e, d),
    'color': lambda e, d: _process_color(e, d)
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

    for channel in chart.to_dict()['encoding']:  # I was unable to get a key-value mapping from only the encoding
        mpl_equivalent, converted_data = _mappings[channel](chart.encoding, chart.data)
        mapping[mpl_equivalent] = converted_data

    return mapping


def _process_x(encoding, data):
    if encoding.x.field is not Undefined:
        return "x", data[encoding.x.field].values

    if parse_shorthand(encoding.x.shorthand, data)['field']:
        return "x", data[parse_shorthand(encoding.x.shorthand, data)['field']].values

    return "x", None


def _process_y(encoding, data):
    if encoding.x.field is not Undefined:
        return "y", data[encoding.y.field].values

    if parse_shorthand(encoding.y.shorthand, data)['field']:
        return "y", data[parse_shorthand(encoding.y.shorthand, data)['field']].values

    return "y", None


def _process_color(encoding, data):
    if encoding.color.field is not Undefined:
        return "c", data[encoding.color.field].values

    if parse_shorthand(encoding.color.shorthand, data)['field']:
        return "c", data[parse_shorthand(encoding.color.shorthand, data)['field']].values

    return "c", None
