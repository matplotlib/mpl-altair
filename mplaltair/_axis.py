import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from ._data import _convert_to_mpl_date


def _set_limits(channel, mark, ax):
    """Set the axis limits on the Matplotlib axis

    Parameters
    ----------
    channel : parse_chart.ChannelMetadata
        The channel data and metadata
    mark : str
        The chart's mark
    ax : matplotlib.axes
    """

    _axis_kwargs = {
        'x': {'min': 'left', 'max': 'right'},
        'y': {'min': 'bottom', 'max': 'top'},
    }

    lims = {}

    if channel.type == 'quantitative':
        # determine limits
        if 'domain' in channel.scale:  # domain takes precedence over zero in Altair
            if channel.scale['domain'] == 'unaggregated':
                raise NotImplementedError
            else:
                lims[_axis_kwargs[channel.name].get('min')] = channel.scale['domain'][0]
                lims[_axis_kwargs[channel.name].get('max')] = channel.scale['domain'][1]
        elif 'type' in channel.scale and channel.scale['type'] != 'linear':
            lims = _set_scale_type(channel, ax)
        else:
            # Include zero on the axis (or not).
            # In Altair, scale.zero defaults to False unless the data is unbinned quantitative.
            if mark == 'line' and channel.name == 'x':
                # Contrary to documentation, Altair defaults to scale.zero=False for the x-axis on line graphs.
                # Pass to skip.
                pass
            else:
                # Check that a positive minimum is zero if scale.zero is True:
                if ('zero' not in channel.scale or channel.scale['zero'] == True) and min(channel.data) > 0:
                    lims[_axis_kwargs[channel.name].get('min')] = 0  # quantitative sets min to be 0 by default

                # Check that a negative maximum is zero if scale.zero is True:
                if ('zero' not in channel.scale or channel.scale['zero'] == True) and max(channel.data) < 0:
                    lims[_axis_kwargs[channel.name].get('max')] = 0

    elif channel.type == 'temporal':
        # determine limits
        if 'domain' in channel.scale:
            domain = _convert_to_mpl_date(channel.scale['domain'])
            lims[_axis_kwargs[channel.name].get('min')] = domain[0]
            lims[_axis_kwargs[channel.name].get('max')] = domain[1]
        elif 'type' in channel.scale and channel.scale['type'] != 'time':
            lims = _set_scale_type(channel, channel.scale)

    else:
        raise NotImplementedError  # Ordinal and Nominal go here?

    # set the limits
    if channel.name == 'x':
        ax.set_xlim(**lims)
    else:
        ax.set_ylim(**lims)


def _set_scale_type(channel, ax):
    """If the scale is non-linear, change the scale and return appropriate axis limits.
    The 'linear' and 'time' scale types are not included here because quantitative defaults to 'linear'
    and temporal defaults to 'time'. The 'utc' and 'sequential' scales are currently not supported.

    Parameters
    ----------
    channel : parse_chart.ChannelMetadata
        The channel data and metadata
    ax : matplotlib.axes

    Returns
    -------
    lims : dict
        The axis limit mapped to the appropriate axis parameter for scales that change axis limit behavior
    """
    lims = {}
    if channel.scale['type'] == 'log':

        base = 10  # default base is 10 in altair
        if 'base' in channel.scale:
            base = channel.scale['base']

        if channel.name == 'x':
            ax.set_xscale('log', basex=base)
            # lower limit: round down to nearest major tick (using log base change rule)
            lims['left'] = base**np.floor(np.log10(channel.data.min())/np.log10(base))
        else:  # y-axis
            ax.set_yscale('log', basey=base)
            # lower limit: round down to nearest major tick (using log base change rule)
            lims['bottom'] = base**np.floor(np.log10(channel.data.min())/np.log10(base))

    elif channel.scale['type'] == 'pow' or channel.scale['type'] == 'sqrt':
        """The 'sqrt' scale is just the 'pow' scale with exponent = 0.5.
        When Matplotlib gets a power scale, the following should work:
        
        exponent = 2  # default exponent value for 'pow' scale
        if channel.scale['type'] == 'sqrt':
            exponent = 0.5
        elif 'exponent' in channel.scale:
            exponent = channel.scale['exponent']

        if channel.name == 'x':
            ax.set_xscale('power_scale', exponent=exponent)
        else:  # y-axis
            ax.set_yscale('power_scale', exponent=exponent)
        """
        raise NotImplementedError

    elif channel.scale['type'] == 'utc':
        raise NotImplementedError
    elif channel.scale['type'] == 'sequential':
        raise NotImplementedError("sequential scales used primarily for continuous colors")
    else:
        raise NotImplementedError
    return lims


def _set_tick_locator(channel, ax):
    """Set the tick locator if it needs to vary from the default locator

    Parameters
    ----------
    channel : parse_chart.ChannelMetadata
        The channel data and metadata
    ax : matplotlib.axes
        The mapping of the axis metadata and the scale data
    """
    current_axis = {'x': ax.xaxis, 'y': ax.yaxis}
    if 'values' in channel.axis:
        if channel.type == 'temporal':
            current_axis[channel.name].set_major_locator(ticker.FixedLocator(_convert_to_mpl_date(channel.axis.get('values'))))
        elif channel.type == 'quantitative':
            current_axis[channel.name].set_major_locator(ticker.FixedLocator(channel.axis.get('values')))
        else:
            raise NotImplementedError
    elif 'tickCount' in channel.axis:
        current_axis[channel.name].set_major_locator(
            ticker.MaxNLocator(steps=[2, 5, 10], nbins=channel.axis.get('tickCount')+1, min_n_ticks=channel.axis.get('tickCount'))
        )


def _set_tick_formatter(channel, ax):
    """Set the tick formatter.


    Parameters
    ----------
    channel : parse_chart.ChannelMetadata
        The channel data and metadata
    ax : matplotlib.axes
        The mapping of the axis metadata and the scale data

    Notes
    -----
    For quantitative formatting, Matplotlib does not support some format strings that Altair supports.
    Matplotlib only supports format strings as used by str.format().

    For formatting of temporal data, Matplotlib does not support some format strings that Altair supports (%L, %Q, %s).
    Matplotlib only supports datetime.strftime formatting for dates.
    """
    current_axis = {'x': ax.xaxis, 'y': ax.yaxis}
    format_str = channel.axis.get('format', '')

    if channel.type == 'temporal':
        if not format_str:
            format_str = '%b %d, %Y'

        current_axis[channel.name].set_major_formatter(mdates.DateFormatter(format_str))  # May fail silently

    elif channel.type == 'quantitative':
        if format_str:
            current_axis[channel.name].set_major_formatter(ticker.StrMethodFormatter('{x:' + format_str + '}'))

            # Verify that the format string is valid for Matplotlib and exit nicely if not.
            try:
                current_axis[channel.name].get_major_formatter().__call__(1)
            except ValueError:
                raise ValueError("Matplotlib only supports format strings as used by `str.format()`."
                                 "Some format strings that work in Altair may not work in Matplotlib."
                                 "Please use a different format string.")
    else:
        raise NotImplementedError  # Nominal and Ordinal go here


def _set_label_angle(channel, ax):
    """Set the label angle. TODO: handle axis.labelAngle from Altair

        Parameters
        ----------
        channel : parse_chart.ChannelMetadata
            The channel data and metadata
        ax : matplotlib.axes
            The mapping of the axis metadata and the scale data
        """
    if channel.type == 'temporal' and channel.name == 'x':
        for label in ax.get_xticklabels():
            # Rotate the labels on the x-axis so they don't run into each other.
            label.set_rotation(30)
            label.set_ha('right')

def _set_axis_title(channel, ax):
    '''Sets the axis label

    Currently, does not support aggregated, binned or timeUnit specified channels

    Parameters
    ----------
    channel: parse_chart.ChannelMetadata
        The channel data and metadata
    ax: maptlotlib.axes
        The matplotlib axis to be modified
    '''
    if channel.title:
        if channel.name == 'x':
            ax.set_xlabel(title)
        elif channel.name == 'y':
            ax.set_ylabel(title)
    elif channel.aggregate:
        raise NotImplementedError
    elif channel.bin:
        raise NotImplementedError
    elif channel.timeUnit:
        raise NotImplementedError

def _set_axis_label_visibility(channel, ax):
    '''Set the axis label visibility

    Parameters
    ----------
    channel: parse_chart.ChannelMetadata
        The channel data and metadata
    ax: maptlotlib.axes
        The matplotlib axis to be modified
    '''
    labels = channel.axis.get('labels', True)

    if channel.name == 'x':
        ax.tick_param(labelbottom=labels, labeltop=labels)
    elif channel.name == 'y':
        ax.tick_param(labelleft=labels, labelright=labels)

def convert_axis(ax, chart):
    """Convert elements of the altair chart to Matplotlib axis properties

    Parameters
    ----------
    ax
        The Matplotlib axis to be modified
    chart : parse_chart.ChartMetadata
        The chart data and metadata
    """

    for channel in [chart.encoding['x'], chart.encoding['y']]:
        _set_limits(channel, chart.mark, ax)
        _set_tick_locator(channel, ax)
        _set_tick_formatter(channel, ax)
        _set_label_angle(channel, ax)
        _set_axis_title(channel, ax)
        _set_axis_label_visibility(channel, ax)
