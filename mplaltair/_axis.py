import matplotlib.dates as mdates
from ._data import _locate_channel_data, _locate_channel_dtype, _locate_channel_scale


def _set_limits(channel):
    """Set the axis limits on the Matplotlib axis

    Parameters
    ----------
    channel : dict
        The mapping of the channel metadata and the scale data

    """

    if channel['dtype'] == 'quantitative':
        _axis_kwargs = {
            'x': {'min': 'left', 'max': 'right'},
            'y': {'min': 'bottom', 'max': 'top'},
        }

        lims = {}

        # determine limits
        if 'domain' in channel:  # domain takes precedence over zero in Altair
            if channel['domain'] == 'unaggregated':
                raise NotImplementedError
            else:
                lims[_axis_kwargs[channel['axis']].get('min')] = channel['domain'][0]
                lims[_axis_kwargs[channel['axis']].get('max')] = channel['domain'][1]
        else:
            if ('zero' not in channel or channel['zero'] == True) and min(channel['data']) > 0:
                lims[_axis_kwargs[channel['axis']].get('min')] = 0  # quantitative sets min to be 0 by default
            else:
                lims[_axis_kwargs[channel['axis']].get('min')] = min(channel['data'])  # basic approach

            if ('zero' not in channel or channel['zero'] == True) and max(channel['data']) < 0:
                lims[_axis_kwargs[channel['axis']].get('max')] = 0
            else:
                lims[_axis_kwargs[channel['axis']].get('max')] = max(channel['data'])  # basic approach

        # set the limits
        if channel['axis'] == 'x':
            channel['ax'].set_xlim(**lims)
        else:
            channel['ax'].set_ylim(**lims)
    else:
        raise NotImplementedError


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
            _set_limits(scale_info)
            _set_scale_type(scale_info)
            _set_tick_locator(scale_info)
