import altair as alt
import matplotlib.pyplot as plt
from mplaltair import convert
from vega_datasets import data

url = data.stocks.url
stocks = data.stocks()

def test_line():
    chart = alt.Chart(stocks).mark_line().encode(
        alt.X('date:T'),
        alt.Y('price:Q'),
        alt.Color('symbol:O')
    )
    # fig, ax = plt.subplots()
    # fig, ax = convert(chart)
    # plt.show()
    convert(chart)