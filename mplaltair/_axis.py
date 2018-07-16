import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from ._data import _locate_channel_data, _locate_channel_dtype, _locate_channel_scale, _locate_channel_axis


def _set_limits(channel, scale):
    """Set the axis limits on the Matplotlib axis

    Parameters
    ----------
    scale : dict
        The mapping of the scale metadata and the scale data

    """

    if channel['dtype'] == 'quantitative':
        _axis_kwargs = {
            'x': {'min': 'left', 'max': 'right'},
            'y': {'min': 'bottom', 'max': 'top'},
        }

        lims = {}

        # determine limits
        if 'domain' in scale:  # domain takes precedence over zero in Altair
            if scale['domain'] == 'unaggregated':
                raise NotImplementedError
            else:
                lims[_axis_kwargs[channel['axis']].get('min')] = scale['domain'][0]
                lims[_axis_kwargs[channel['axis']].get('max')] = scale['domain'][1]
        else:
            if ('zero' not in scale or scale['zero'] == True) and min(channel['data']) > 0:
                lims[_axis_kwargs[channel['axis']].get('min')] = 0  # quantitative sets min to be 0 by default
            else:
                lims[_axis_kwargs[channel['axis']].get('min')] = min(channel['data'])  # basic approach

            if ('zero' not in scale or scale['zero'] == True) and max(channel['data']) < 0:
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


def _set_scale_type(channel, scale):
    """Scale Type needs to have the scale type and optional base and optional pow"""
    if 'type' in scale:
        if scale['type'] == 'log':
            if channel['axis'] == 'x':
                channel['ax'].set_xscale('log')
            else:  # y-axis
                channel['ax'].set_yscale('log')


def _set_tick_locator(channel, axis):
    """Tick Locator needs to have a lot of information"""
    if 'values' in axis:
        if channel['axis'] == 'x':
            channel['ax'].xaxis.set_major_locator(ticker.FixedLocator(axis.get('values')))
        else:  # y-axis
            channel['ax'].yaxis.set_major_locator(ticker.FixedLocator(axis.get('values')))
    else:
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
            chart_info = {'ax': ax, 'axis': channel,
                          'data': _locate_channel_data(chart, channel),
                          'dtype': _locate_channel_dtype(chart, channel)}
            scale_info = _locate_channel_scale(chart, channel)
            axis_info = _locate_channel_axis(chart, channel)
            _set_scale_type(chart_info, scale_info)
            _set_limits(chart_info, scale_info)
            _set_tick_locator(chart_info, axis_info)
