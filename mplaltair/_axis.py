import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from ._data import _locate_channel_data, _locate_channel_dtype, _locate_channel_scale, _locate_channel_axis, _convert_to_mpl_date


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

            # Check that a negative maximum is zero if zero is True:
            if ('zero' not in scale or scale['zero'] == True) and max(channel['data']) < 0:
                lims[_axis_kwargs[channel['axis']].get('max')] = 0

    elif channel['dtype'] == 'temporal':
        # determine limits
        if 'domain' in scale:
            domain = _convert_to_mpl_date(scale['domain'])
            lims[_axis_kwargs[channel['axis']].get('min')] = domain[0]
            lims[_axis_kwargs[channel['axis']].get('max')] = domain[1]
        elif 'type' in scale and scale['type'] != 'time':
            lims = _set_scale_type(channel, scale)

    else:
        raise NotImplementedError  # Ordinal and Nominal go here?

    # set the limits
    if channel['axis'] == 'x':
        channel['ax'].set_xlim(**lims)
    else:
        channel['ax'].set_ylim(**lims)


def _set_scale_type(channel, scale):
    """If the scale is non-linear, change the scale and return appropriate axis limits.
    Note: The 'linear' and 'time' scale types are not included here because quantitative defaults to 'linear'
    and temporal defaults to 'time'. The 'utc' and 'sequential' are currently not supported.
    """
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
        """The 'sqrt' scale is just the 'pow' scale with exponent = 0.5.
        When Matplotlib gets a power scale, the following should work:
        
        exponent = 2  # default exponent value for 'pow' scale
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

    elif scale['type'] == 'utc':
        raise NotImplementedError
    elif scale['type'] == 'sequential':
        raise NotImplementedError("sequential scales used primarily for continuous colors")
    else:
        raise NotImplementedError
    return lims


def _set_tick_locator(channel, axis):
    """Set the tick locator if it needs to vary from the default"""
    # Works for quantitative and temporal
    # The auto locator has similar (if not the same) defaults as Altair
    current_axis = {'x': channel['ax'].xaxis, 'y': channel['ax'].yaxis}
    if 'values' in axis:
        if channel['dtype'] == 'temporal':
            current_axis[channel['axis']].set_major_locator(ticker.FixedLocator(_convert_to_mpl_date(axis.get('values'))))
        elif channel['dtype'] == 'quantitative':
            current_axis[channel['axis']].set_major_locator(ticker.FixedLocator(axis.get('values')))
        else:
            raise NotImplementedError
    elif 'tickCount' in axis:
        current_axis[channel['axis']].set_major_locator(
            ticker.MaxNLocator(steps=[2, 5, 10], nbins=axis.get('tickCount')+1, min_n_ticks=axis.get('tickCount'))
        )


def _set_tick_formatter(channel, axis):
    current_axis = {'x': channel['ax'].xaxis, 'y': channel['ax'].yaxis}
    format_str = ''

    if 'format' in axis:
        format_str = axis['format']

    if channel['dtype'] == 'temporal':
        if not format_str:
            format_str = '%b %d, %Y'

        current_axis[channel['axis']].set_major_formatter(mdates.DateFormatter(format_str))

        try:
            current_axis[channel['axis']].get_major_formatter().__call__(1)
        except ValueError:
            raise ValueError("Matplotlib only supports `strftime` formatting for dates."
                             "Currently, %L, %Q, and %s are allowed in Altair, but not allowed in Matplotlib."
                             "Please use a `strftime` compliant format string.")


        # TODO: move rotation to another function?
        if channel['axis'] == 'x':
            for label in channel['ax'].get_xticklabels():
                # Rotate the labels on the x-axis so they don't run into each other.
                label.set_rotation(30)
                label.set_ha('right')

    elif channel['dtype'] == 'quantitative':
        if format_str:
            current_axis[channel['axis']].set_major_formatter(ticker.StrMethodFormatter('{x:' + format_str + '}'))

            # Verify that the format string is valid for Matplotlib and exit nicely if not.
            try:
                current_axis[channel['axis']].get_major_formatter().__call__(1)
            except ValueError:
                raise ValueError("Matplotlib only supports format strings as used by `str.format()`."
                                 "Some format strings that work in Altair may not work in Matplotlib."
                                 "Please use a different format string.")
    else:
        raise NotImplementedError  # Nominal and Ordinal go here


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
                chart_info['data'] = _convert_to_mpl_date(chart_info['data'])

            scale_info = _locate_channel_scale(chart, channel)
            axis_info = _locate_channel_axis(chart, channel)

            _set_limits(chart_info, scale_info)
            _set_tick_locator(chart_info, axis_info)
            _set_tick_formatter(chart_info, axis_info)
