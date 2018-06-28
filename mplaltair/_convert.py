from altair.utils.core import parse_shorthand
from altair.utils.schemapi import Undefined


# mapping: altair channel: mpl kwargs for scatter() (and plot(), sort of)
_mpl_scatter_equivalent = {
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
        data = _locate_channel_data(channel, chart.data)
        mapping[_mpl_scatter_equivalent[encoding_channel]] = data

    return mapping


def _locate_channel_data(channel, data):
    if hasattr(channel, "value") and channel.value is not Undefined:
        return channel.value
    elif hasattr(channel, "aggregate") and channel.aggregate is not Undefined:
        return _aggregate_channel()
    elif hasattr(channel, "field") and channel.field is not Undefined:
        return data[channel.field].values
    elif hasattr(channel, "shorthand") and channel.shorthand is not Undefined:
        parsed = parse_shorthand(channel.shorthand, data)
        if "field" in parsed:
            return data[parsed['field']].values
    else:
        raise ValueError("Cannot find data for the channel")


def _aggregate_channel():
    # TODO implement proper handling of aggregate functions
    return []
