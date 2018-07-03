import matplotlib
import altair


# TODO rename this?
def convert(encoding, *, figure=None):
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
    if figure is None:
        from matplotlib import pyplot as plt
        figure = plt.figure()

    mapping = {}

    return figure, mapping
