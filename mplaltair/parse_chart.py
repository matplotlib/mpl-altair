from mplaltair._data import _locate_channel_data, _locate_channel_axis, _locate_channel_field, _locate_channel_scale,_locate_channel_dtype, _convert_to_mpl_date, _normalize_data


class ChannelMetadata(object):
    def __init__(self, k, v, alt_chart, df):
        self.channel = k  # Not from Altair
        self.data = _locate_channel_data(alt_chart, k)  # Not from Altair
        self.axis = _locate_channel_axis(alt_chart, k)
        self.bin = None
        self.field = _locate_channel_field(alt_chart, k)
        self.scale = _locate_channel_scale(alt_chart, k)
        self.sort = None
        self.stack = None
        self.timeUnit = None
        self.title = None
        self.type = _locate_channel_dtype(alt_chart, k)

        if self.type == 'temporal':
            self.data = _convert_to_mpl_date(self.data)


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