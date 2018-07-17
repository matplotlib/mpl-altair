import matplotlib
import altair
from ._convert import _convert

def convert(chart):
    """Convert an altair encoding to a Matplotlib figure


    Parameters
    ----------
    chart
        The Altair chart object generated by Altair

    Returns
    -------
    mapping: dict
        Mapping from parts of the encoding to the Matplotlib artists.
        This is for later customization

    """
    return _convert(chart)
