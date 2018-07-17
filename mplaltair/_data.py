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
    elif channel.get('field'):
        return data[channel.get('field')].values
    else:
        raise ValueError("Cannot find data for the channel")


def _aggregate_channel():
    raise NotImplementedError