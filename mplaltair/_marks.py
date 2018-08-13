import matplotlib
import numpy as np
from ._data import _convert_to_mpl_date


def _handle_line(chart, ax):
    """Convert encodings, manipulate data if needed, plot on ax.

    Parameters
    ----------
    chart : altair.Chart
        The Altair chart object

    ax
        The Matplotlib axes object

    Notes
    -----
    Fill isn't necessary until mpl-altair can handle multiple plot types in one plot.
    Size is unsupported by both Matplotlib and Altair.
    When both Color and Stroke are provided, color is ignored and stroke is used.
    Shape is unsupported in line graphs unless another plot type is plotted at the same time.
    """
    groups = []
    kwargs = {}

    if chart.encoding.get('opacity'):
        groups.append('opacity')
    if chart.encoding.get('stroke'):
        groups.append('stroke')
    elif chart.encoding.get('color'):
        groups.append('color')

    list_fields = lambda c, g: [chart.encoding[i].field for i in g]
    try:
        for label, subset in chart.data.groupby(list_fields(chart, groups)):
            if 'opacity' in groups:
                kwargs['alpha'] = _opacity_norm(chart, subset[chart.encoding['opacity'].field].iloc[0])

                if 'color' not in groups and 'stroke' not in groups:
                    kwargs['color'] = matplotlib.rcParams['lines.color']
            ax.plot(subset[chart.encoding['x'].field], subset[chart.encoding['y'].field], **kwargs)
    except ValueError:
        ax.plot(chart.encoding['x'].data, chart.encoding['y'].data)


def _opacity_norm(chart, val):
    """
    Normalize the values of a column to be between 0.15 and 1, which is a visible range for opacity.

    Parameters
    ----------
    chart : parse_chart.ChartMetadata
        The Altair chart object
    val
        The specific value to be normalized.

    Returns
    -------
    The normalized value (between 0.15 and 1)
    """
    arr = chart.encoding['opacity'].data
    if chart.encoding['opacity'].type in ['ordinal', 'nominal', 'temporal']:
        unique, indices = np.unique(arr, return_inverse=True)
        arr = indices
        if chart.encoding['opacity'].type == "temporal":
            val = unique.tolist().index(_convert_to_mpl_date(val))
        else:
            val = unique.tolist().index(val)
    data_min, data_max = (arr.min(), arr.max())
    desired_min, desired_max = (0.15, 1)  # Chosen so that the minimum value is visible (aka nonzero)
    return ((val - data_min) / (data_max - data_min)) * (desired_max - desired_min) + desired_min