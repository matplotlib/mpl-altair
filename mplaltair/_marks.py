import matplotlib
import numpy as np
from ._data import _locate_channel_field, _locate_channel_data, _locate_channel_dtype, _convert_to_mpl_date


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

    if 'opacity' in chart.to_dict()['encoding']:
        groups.append('opacity')

    if 'stroke' in chart.to_dict()['encoding']:
        groups.append('stroke')
    elif 'color' in chart.to_dict()['encoding']:
        groups.append('color')

    list_fields = lambda c, g: [_locate_channel_field(c, i) for i in g]
    if len(groups) > 0:
        for label, subset in chart.data.groupby(list_fields(chart, groups)):
            if 'opacity' in groups:
                kwargs['alpha'] = _opacity_norm(chart, _locate_channel_dtype(chart, 'opacity'),
                                                subset[_locate_channel_field(chart, 'opacity')].iloc[0])

                if 'color' not in groups and 'stroke' not in groups:
                    kwargs['color'] = matplotlib.rcParams['lines.color']
            ax.plot(subset[_locate_channel_field(chart, 'x')], subset[_locate_channel_field(chart, 'y')], **kwargs)
    else:
        ax.plot(_locate_channel_data(chart, 'x'), _locate_channel_data(chart, 'y'))


def _opacity_norm(chart, dtype, val):
    arr = _locate_channel_data(chart, 'opacity')
    if dtype in ['ordinal', 'nominal', 'temporal']:
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