import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from ._data import _locate_channel_data, _locate_channel_dtype, _locate_channel_scale, _locate_channel_axis
from ._date import convert_to_mpl_date


def _set_limits(channel, scale):
    """Set the axis limits on the Matplotlib axis

    Parameters
    ----------
    scale : dict
        The mapping of the scale metadata and the scale data

    """

    _axis_kwargs = {
        'x': {'min': 'xmin', 'max': 'xmax'},
        'y': {'min': 'ymin', 'max': 'ymax'},
    }

    lims = {}

    if channel['dtype'] == 'quantitative':
        # determine limits
        if 'domain' in scale:  # domain takes precedence over zero in Altair
            if scale['domain'] == 'unaggregated':
                raise NotImplementedError
            else:
                lims[_axis_kwargs[channel['axis']].get('min')] = scale['domain'][0]
                lims[_axis_kwargs[channel['axis']].get('max')] = scale['domain'][1]
        elif 'type' in scale and scale['type'] != 'linear':
            lims = _set_scale_type(channel, scale)
        else:
            # Check that a positive minimum is zero if zero is True:
            if ('zero' not in scale or scale['zero'] == True) and min(channel['data']) > 0:
                lims[_axis_kwargs[channel['axis']].get('min')] = 0  # quantitative sets min to be 0 by default
            else:
                pass  # use default

            # Check that a negative maximum is zero if zero is True:
            if ('zero' not in scale or scale['zero'] == True) and max(channel['data']) < 0:
                lims[_axis_kwargs[channel['axis']].get('max')] = 0
            else:
                pass  # use default

    elif channel['dtype'] == 'temporal':
        if 'domain' in scale:
            """Work is currently being done in Altair to modify what datetypes are allowed for domain specification.
            When something more stable is released the following might be useful for setting the date:
            
            lims[_axis_kwargs[channel['axis']].get('min')] = convert_to_mpl_date(scale['domain'][0])
            lims[_axis_kwargs[channel['axis']].get('max')] = convert_to_mpl_date(scale['domain'][1])
            """
            raise NotImplementedError
        elif 'type' in scale:
            lims = _set_scale_type(channel, scale)
        else:
            pass  # use default
    else:
        raise NotImplementedError

    # set the limits
    if channel['axis'] == 'x':
        channel['ax'].set_xlim(**lims)
    else:
        channel['ax'].set_ylim(**lims)


def _set_scale_type(channel, scale):
    """If the scale is non-linear, change the scale and return appropriate axis limits."""
    lims = {}
    if scale['type'] == 'log':

        base = 10  # default base is 10 in altair
        if 'base' in scale:
            base = scale['base']

        if channel['axis'] == 'x':
            channel['ax'].set_xscale('log', basex=base)
            # lower limit: round down to nearest major tick (using log base change rule)
            lims['xmin'] = base**np.floor(np.log10(channel['data'].min())/np.log10(base))
        else:  # y-axis
            channel['ax'].set_yscale('log', basey=base)
            # lower limit: round down to nearest major tick (using log base change rule)
            lims['ymin'] = base**np.floor(np.log10(channel['data'].min())/np.log10(base))

    elif scale['type'] == 'pow' or scale['type'] == 'sqrt':
        """When Matplotlib gets a power scale, the following should work:
        
        exponent = 2
        if scale['type'] == 'sqrt':
            exponent = 0.5
        elif 'exponent' in scale:
            exponent = scale['exponent']

        if channel['axis'] == 'x':
            channel['ax'].set_xscale('power_scale', exponent=exponent)
        else:  # y-axis
            channel['ax'].set_yscale('power_scale', exponent=exponent)
        """
        raise NotImplementedError

    elif scale['type'] == 'time':
        raise NotImplementedError
    elif scale['type'] == 'utc':
        raise NotImplementedError
    elif scale['type'] == 'sequential':
        raise NotImplementedError
    else:
        raise NotImplementedError
    return lims


def _set_tick_locator(channel, axis):
    """Set the tick locator if it needs to vary from the default"""
    # Works for quantitative and temporal
    if 'values' in axis:
        if channel['axis'] == 'x':
            channel['ax'].xaxis.set_major_locator(ticker.FixedLocator(axis.get('values')))
        else:  # y-axis
            channel['ax'].yaxis.set_major_locator(ticker.FixedLocator(axis.get('values')))
    elif 'tickCount' in axis:
        if channel['axis'] == 'x':
            channel['ax'].xaxis.set_major_locator(ticker.MaxNLocator(steps=[2, 5, 10], nbins=axis.get('tickCount')+1,
                                                                     min_n_ticks=axis.get('tickCount')))
        else:  # y-axis
            channel['ax'].yaxis.set_major_locator(ticker.MaxNLocator(steps=[2, 5, 10], nbins=axis.get('tickCount')+1,
                                                                     min_n_ticks=axis.get('tickCount')))
    else:
        pass  # Use the auto locator (it has similar, if not the same settings as Altair)


def _set_tick_formatter(channel, axis):
    if channel['dtype'] == 'temporal':
        formatter = mdates.DateFormatter('%b %d, %Y')
        if channel['axis'] == 'x':
            channel['ax'].xaxis.set_major_formatter(formatter)
            for label in channel['ax'].get_xticklabels():
                # Rotate the labels on the x-axis so they don't run into each other.
                label.set_rotation(30)
                label.set_ha('right')
        else:  # y-axis
            channel['ax'].yaxis.set_major_formatter(formatter)
    else:
        pass  # Use the auto formatter for quantitative (it has similar, if not the same settings as Altair)


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
            if chart_info['dtype'] == 'temporal':
                chart_info['data'] = convert_to_mpl_date(chart_info['data'])

            scale_info = _locate_channel_scale(chart, channel)
            axis_info = _locate_channel_axis(chart, channel)

            _set_limits(chart_info, scale_info)
            _set_tick_locator(chart_info, axis_info)
            _set_tick_formatter(chart_info, axis_info)
