import altair as alt
import pandas as pd
import mplaltair._convert as convert
import pytest

df_temporal = pd.DataFrame({
    "years": pd.date_range('01/01/2015', periods=5, freq='Y'), "months": pd.date_range('1/1/2015', periods=5, freq='M'),
    "days": pd.date_range('1/1/2015', periods=5, freq='D'), "hrs": pd.date_range('1/1/2015', periods=5, freq='H'),
    "combination": pd.to_datetime(['1/1/2015', '1/1/2015 10:00:00', '1/2/2015 00:00', '1/4/2016 10:00', '5/1/2016']),
    "quantitative": [1.1, 2.1, 3.1, 4.1, 5.1]
})


def test_data_field():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X(field='combination', type='temporal'))
    for channel in chart.to_dict()['encoding']:
        data = convert._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
    assert list(data) == list(df_temporal['combination'].values)


def test_data_shorthand():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X('combination'))
    for channel in chart.to_dict()['encoding']:
        data = convert._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
    assert list(data) == list(df_temporal['combination'].values)


@pytest.mark.xfail(raises=NotImplementedError)
def test_data_timeUnit_shorthand():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X('month(combination):T'))
    for channel in chart.to_dict()['encoding']:
        data = convert._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)


@pytest.mark.xfail(raises=NotImplementedError)
def test_data_timeUnit_field():
    chart = alt.Chart(df_temporal).mark_point().encode(alt.X(field='combination', type='temporal', timeUnit='month'))
    for channel in chart.to_dict()['encoding']:
        data = convert._locate_channel_data(chart.to_dict()['encoding'][channel], chart.data)
