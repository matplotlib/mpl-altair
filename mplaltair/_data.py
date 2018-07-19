from ._exceptions import ValidationError

def _locate_channel_dtype(chart, channel):
    """Locates dtype used for each channel
        Parameters
        ----------
        chart
            The Altair chart
        channel
            The Altair channel being examined

        Returns
        -------
        A string representing the data type from the Altair chart ('quantitative', 'ordinal', 'numeric', 'temporal')
        """

    channel_val = chart.to_dict()['encoding'][channel]
    if channel_val.get('type'):
        return channel_val.get('type')
    else:
        # TODO: find some way to deal with 'value' so that, opacity, for instance, can be plotted with a value defined
        if channel_val.get('value'):
            raise NotImplementedError
        raise NotImplementedError


def _locate_channel_data(chart, channel):
    """Locates data used for each channel

    Parameters
    ----------
    chart
        The Altair chart
    channel
        The Altair channel being examined

    Returns
    -------
    A numpy ndarray containing the data used for the channel

    Raises
    ------
    ValidationError
        Raised when the specification does not contain any data attribute

    """

    channel_val = chart.to_dict()['encoding'][channel]
    if channel_val.get('value'):
        return channel_val.get('value')
    elif channel_val.get('aggregate'):
        return _aggregate_channel()
    elif channel_val.get('timeUnit'):
        return _handle_timeUnit()
    else:  # field is required if the above are not present.
        return chart.data[channel_val.get('field')].values


def _aggregate_channel():
    raise NotImplementedError


def _handle_timeUnit():
    raise NotImplementedError