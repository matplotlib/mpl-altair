def _locate_channel_dtype(channel, data):
    """Locates data used for each channel
        Parameters
        ----------
        channel
            The encoding channel from the Altair chart
        data : Pandas DataFrame
            Data from the Altair chart
        Returns
        -------
        A string representing the data type from the Altair chart ('quantitative', 'ordinal', 'numeric', 'temporal')
        """
    if channel.get('type'):
        return channel.get('type')
    else:
        # TODO: find some way to deal with 'value' so that, opacity, for instance, can be plotted with a value defined
        if channel.get('value'):
            raise NotImplementedError
        raise NotImplementedError


def _locate_channel_data(channel, data):
    """Locates data used for each channel
    Parameters
    ----------
    channel
        The encoding channel from the Altair chart
    data : Pandas DataFrame
        Data from the Altair chart
    Returns
    -------
    A numpy ndarray containing the data used for the channel
    """

    if channel.get('value'):  # from the value version of the channel
        return channel.get('value')
    elif channel.get('aggregate'):
        return _aggregate_channel()
    elif channel.get('timeUnit'):
        return _handle_timeUnit()
    elif channel.get('field'):
        return data[channel.get('field')].values
    else:
        raise ValueError("Cannot find data for the channel")


def _aggregate_channel():
    raise NotImplementedError


def _handle_timeUnit():
    raise NotImplementedError