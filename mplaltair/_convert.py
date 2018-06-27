from altair.utils.core import parse_shorthand
from altair.utils.schemapi import Undefined


# mapping: altair channel: mpl kwargs for scatter() (and plot(), sort of)
_mpl_equivalent = {
    'x': 'x',
    'y': 'y',
    'color': 'c',
    'size': 's',
    'opacity': 'alpha',
    'shape': 'marker'
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

    for encoding_channel in chart.to_dict()['encoding']:  # Need chart to get dictionary of channels from the encoding

        channel = chart.encoding[encoding_channel]

        if channel.field is not Undefined:
            data = chart.data[channel.field].values
        elif parse_shorthand(channel.shorthand, chart.data)['field'] is not Undefined:
            data = chart.data[parse_shorthand(channel.shorthand, chart.data)['field']].values
        else:
            # TODO fail nicely
            data = []

        mapping[_mpl_equivalent[encoding_channel]] = data

    return mapping