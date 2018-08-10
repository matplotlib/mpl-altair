import matplotlib
import numpy as np
from ._data import _locate_channel_field, _locate_channel_data, _locate_channel_dtype, _convert_to_mpl_date


def _handle_line(chart, ax):
    """Convert encodings, manipulate data if needed, and plot the line chart on an axes.

    Parameters
    ----------
    chart : altair.Chart
        The Altair chart object

    ax : matplotlib.axes
        The Matplotlib axes object

    Notes
    -----
    Fill isn't necessary until mpl-altair can handle multiple plot types in one plot.
    Size is unsupported by both Matplotlib and Altair.
    When both Color and Stroke are provided, color is ignored and stroke is used.
    Shape is unsupported in line graphs unless another plot type is plotted at the same time.
    """

    groupbys = []
    kwargs = {}

    if 'opacity' in chart.to_dict()['encoding']:
        groupbys.append('opacity')

    if 'stroke' in chart.to_dict()['encoding']:
        groupbys.append('stroke')
    elif 'color' in chart.to_dict()['encoding']:
        groupbys.append('color')

    list_fields = lambda c, g: [_locate_channel_field(c, i) for i in g]
    if len(groupbys) > 0:
        for label, subset in chart.data.groupby(list_fields(chart, groupbys)):
            if 'opacity' in groupbys:
                kwargs['alpha'] = _opacity_norm(chart, _locate_channel_dtype(chart, 'opacity'),
                                                subset[_locate_channel_field(chart, 'opacity')].iloc[0])

                if 'color' not in groupbys and 'stroke' not in groupbys:
                    kwargs['color'] = matplotlib.rcParams['lines.color']
            ax.plot(subset[_locate_channel_field(chart, 'x')], subset[_locate_channel_field(chart, 'y')], **kwargs)
    else:
        ax.plot(_locate_channel_data(chart, 'x'), _locate_channel_data(chart, 'y'))


def _opacity_norm(chart, dtype, val):
    """
    Normalize the values of a column to be between 0.15 and 1, which is a visible range for opacity.

    Parameters
    ----------
    chart : altair.Chart
        The Altair chart object
    dtype : str
        The data type of the column ('quantitative', 'nominal', 'ordinal', or 'temporal')
    val
        The specific value to be normalized.

    Returns
    -------
    The normalized value (between 0.15 and 1)
    """
    arr = _locate_channel_data(chart, 'opacity')
    if dtype in ['ordinal', 'nominal', 'temporal']:
        # map categoricals to numbers
        unique, indices = np.unique(arr, return_inverse=True)
        arr = indices
        if dtype == 'temporal':
            val = unique.tolist().index(_convert_to_mpl_date(val))
        else:
            val = unique.tolist().index(val)
    data_min = arr.min()
    data_max = arr.max()
    desired_min, desired_max = (0.15, 1)  # Chosen so that the minimum value is visible
    return ((val - data_min) / (data_max - data_min)) * (desired_max - desired_min) + desired_min