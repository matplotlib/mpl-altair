import matplotlib.dates as mdates
from ._data import _locate_channel_data, _locate_channel_dtype, _locate_channel_scale


def _set_lims(scale_info):
    """Limits need to have the minimum value, maximum value, and if it should start at zero"""

    if scale_info['dtype'] == 'quantitative':
        _axis_mappings = {
            'x': {'min': 'left', 'max': 'right'},
            'y': {'min': 'bottom', 'max': 'top'},
        }
        lims = {}

        if 'domain' in scale_info:
            # do domain things and return b/c domain takes precedence over zero
            pass

        if min(scale_info['data']) > 0:
            if 'zero' not in scale_info or scale_info['zero'] == True:
                lims[_axis_mappings[scale_info['axis']].get('min')] = 0  # quantitative sets min to be 0 by default
            else:
                lims[_axis_mappings[scale_info['axis']].get('min')] = min(scale_info['data'])  # basic approach

        if max(scale_info['data']) < 0:
            if 'zero' not in scale_info or scale_info['zero'] == True:
                lims[_axis_mappings[scale_info['axis']].get('max')] = 0
            else:
                lims[_axis_mappings[scale_info['axis']].get('max')] = max(scale_info['data'])  # basic approach

        # set the limits
        if scale_info['axis'] == 'x':
            scale_info['ax'].set_xlim(**lims)
        else:
            scale_info['ax'].set_ylim(**lims)


def _set_scale_type(scale_info):
    """Scale Type needs to have the scale type and optionally base and optionally pow"""
    pass

def _set_tick_locator(scale_info):
    """Tick Locator needs to have a lot of information"""
    pass

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
        if channel in ['x', 'y']:
            scale_info = _locate_channel_scale(chart, channel)
            scale_info['ax'] = ax
            scale_info['axis'] = channel
            scale_info['data'] = _locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
            scale_info['dtype'] = _locate_channel_dtype(chart.to_dict()['encoding'][channel], chart.data)
            _set_lims(scale_info)
            _set_scale_type(scale_info)
            _set_tick_locator(scale_info)
