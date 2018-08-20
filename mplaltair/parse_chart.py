from mplaltair._data import _convert_to_mpl_date, _normalize_data


class ChannelMetadata(object):
    """
    Stores relevant encoding channel information.

    Attributes
    ----------
    name : str
        The name of the encoding channel
    data : np.array
        The data linked to the channel (temporal data is converted)
    axis : dict
    bin : boolean, None
    field : str
    scale : dict
    sort
    stack
    timeUnit
    title
    type : str
    """
    def __init__(self, channel, alt_chart):
        chart_dict = alt_chart.to_dict()
        self.name = channel
        self.data = self._locate_channel_data(alt_chart)
        self.axis = chart_dict['encoding'][self.name].get('axis', {})
        self.bin = chart_dict['encoding'][self.name].get('bin', None)
        self.field = chart_dict['encoding'][self.name].get('field', None)
        self.scale = chart_dict['encoding'][self.name].get('scale', {})
        self.sort = chart_dict['encoding'][self.name].get('sort', None)
        self.stack = chart_dict['encoding'][self.name].get('stack', None)
        self.timeUnit = chart_dict['encoding'][self.name].get('aggregate', None)
        self.title = chart_dict['encoding'][self.name].get('title', None)
        self.type = self._locate_channel_dtype(alt_chart)

        if self.type == 'temporal':
            self.data = _convert_to_mpl_date(self.data)

    def _aggregate_channel(self):
        raise NotImplementedError

    def _handle_timeUnit(self):
        raise NotImplementedError

    def _locate_channel_data(self, alt_chart):
        """Locates data used for each channel

        Parameters
        ----------
        alt_chart : altair.Chart
            The Altair chart

        Returns
        -------
        A numpy ndarray containing the data used for the channel

        """

        channel_val = alt_chart.to_dict()['encoding'][self.name]
        if channel_val.get('value'):
            return channel_val.get('value')
        elif channel_val.get('aggregate'):
            return self._aggregate_channel()
        elif channel_val.get('timeUnit'):
            return self._handle_timeUnit()
        else:  # field is required if the above are not present.
            return alt_chart.data[channel_val.get('field')].values

    def _locate_channel_dtype(self, alt_chart):
        """Locates dtype used for each channel

        Parameters
        ----------
        alt_chart : altair.Chart
            The Altair chart

        Returns
        -------
        A string representing the data type from the Altair chart ('quantitative', 'ordinal', 'numeric', 'temporal')
        """

        channel_val = alt_chart.to_dict()['encoding'][self.name]
        if channel_val.get('type'):
            return channel_val.get('type')
        else:
            # TODO: find some way to deal with 'value' so that, opacity, for instance, can be plotted with a value defined
            if channel_val.get('value'):
                raise NotImplementedError
            raise NotImplementedError



class ChartMetadata(object):
    """
    Stores Altair chart information usefully. Use this class for initially converting the Altair chart.

    Attributes
    ----------
    data : pd.DataFrame
    mark : str
    encoding : dict of ChannelMetadata
    """

    def __init__(self, alt_chart):

        if not alt_chart.to_dict().get('encoding'):
            raise ValueError("Encoding is not provided with the chart specification")

        _normalize_data(alt_chart)
        self.data = alt_chart.data
        self.mark = alt_chart.mark

        self.encoding = {}
        for k, v in alt_chart.to_dict()['encoding'].items():
            self.encoding[k] = ChannelMetadata(k, alt_chart)