from mplaltair._data import _convert_to_mpl_date, _normalize_data


class ChannelMetadata(object):
    def __init__(self, k, v, alt_chart, df):
        self.channel = k  # Not from Altair
        self.data = self._locate_channel_data(alt_chart)  # Not from Altair
        self.axis = alt_chart.to_dict()['encoding'][self.channel].get('axis', {})
        self.bin = alt_chart.to_dict()['encoding'][self.channel].get('bin', None)
        self.field = alt_chart.to_dict()['encoding'][self.channel].get('field', None)
        self.scale = alt_chart.to_dict()['encoding'][self.channel].get('scale', {})
        self.sort = alt_chart.to_dict()['encoding'][self.channel].get('sort', None)
        self.stack = alt_chart.to_dict()['encoding'][self.channel].get('stack', None)
        self.timeUnit = alt_chart.to_dict()['encoding'][self.channel].get('aggregate', None)
        self.title = alt_chart.to_dict()['encoding'][self.channel].get('title', None)
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
        alt_chart
            The Altair chart

        Returns
        -------
        A numpy ndarray containing the data used for the channel

        Raises
        ------
        ValidationError
            Raised when the specification does not contain any data attribute
        """
        channel_val = alt_chart.to_dict()['encoding'][self.channel]
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
        chart
            The Altair chart

        Returns
        -------
        A string representing the data type from the Altair chart ('quantitative', 'ordinal', 'numeric', 'temporal')
        """

        channel_val = alt_chart.to_dict()['encoding'][self.channel]
        if channel_val.get('type'):
            return channel_val.get('type')
        else:
            # TODO: find some way to deal with 'value' so that, opacity, for instance, can be plotted with a value defined
            if channel_val.get('value'):
                raise NotImplementedError
            raise NotImplementedError



class ChartMetadata(object):
    """
    data : pd.DataFrame
    mark : string?
    encoding : dict of Channels
    """

    def __init__(self, alt_chart):
        _normalize_data(alt_chart)
        self.data = alt_chart.data
        self.mark = alt_chart.mark
        self.encoding = {}
        ALTAIR_ENCODINGS = ['color', 'detail', 'fill', 'href', 'key', 'latitude', 'latitude2', 'longitude',
                            'longitude2',
                            'opacity', 'order', 'shape', 'size', 'stroke', 'text', 'tooltip', 'x', 'x2', 'y', 'y2']
        for k, v in alt_chart.to_dict()['encoding'].items():
            self.encoding[k] = ChannelMetadata(k, v, alt_chart, self.data)
        for i in ALTAIR_ENCODINGS:
            if i not in alt_chart.to_dict()['encoding'].keys():
                self.encoding[i] = None