import matplotlib.dates as mdates
from ._data import _locate_channel_data, _locate_channel_dtype


def _setup_locator(chart):
    pass


def _setup_lims(data, dtype, axis):
    _axis_mappings = {
        'x': {'min': 'left', 'max': 'right'},
        'y': {'min': 'bottom', 'max': 'top'},
    }
    lims = {}
    if dtype == 'quantitative':
        if min(data) > 0:
            lims[_axis_mappings[axis].get('min')] = 0
        else:
            lims[_axis_mappings[axis].get('min')] = min(data)

        lims[_axis_mappings[axis].get('max')] = max(data)
        return lims
    else:
        return None

def convert_axis(ax, chart):
    """Convert elements of the altair chart to Matplotlib axis properties

    Parameters
    ----------
    ax
        The Matplotlib axis to be modified
    chart
        The Altair chart
    """

    for channel in chart.to_dict()['encoding']:
        if channel == 'x' or channel == 'y':
            data = _locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
            dtype = _locate_channel_dtype(chart.to_dict()['encoding'][channel], chart.data)
            if dtype == 'temporal':
                try:
                    data = mdates.date2num(data)  # Convert dates to Matplotlib dates
                except ValueError:
                    raise
            if channel == 'x':
                xlims = _setup_lims(data, dtype, 'x')
                xloc = None  # Not implemented yet
            else:  # channel == 'y'
                ylims = _setup_lims(data, dtype, 'y')
                yloc = None  # Not implemented yet
        else:
            print("No data for axis")

    if xloc is not None:
        ax.xaxis.set_major_locator(xloc)
    if yloc is not None:
        ax.yaxis.set_minor_locator(yloc)
    if xlims is not None:
        ax.set_xlim(**xlims)
    if ylims is not None:
        ax.set_ylim(**ylims)