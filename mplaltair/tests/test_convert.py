import matplotlib
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import numpy as np
import mplaltair._convert as convert
import pytest

df_basic = pd.DataFrame({"a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, 3]})
chart_x = alt.Chart(df_basic).mark_point().encode(alt.X('a'))
chart_x_y = alt.Chart(df_basic).mark_point().encode(alt.X('a'), alt.Y('b'))
chart_color = alt.Chart(df_basic).mark_point().encode(alt.X('a'), alt.Y('b'), color=alt.Color('c:Q'))

df_count = pd.DataFrame({"a": [1, 1, 2, 3, 5], "b": [1.4, 1.4, 2.9, 3.18, 5.3]})
chart_x_count_y = alt.Chart(df_count).mark_point().encode(alt.X('a'), alt.Y('count()'))


def test_quantitative_x():
    mapping = convert.convert_quantitative(chart_x)
    assert np.array_equal(mapping['x'], df_basic['a'].values)


def test_quantitative_x_y():
    mapping = convert.convert_quantitative(chart_x_y)
    assert np.array_equal(mapping['x'], df_basic['a'].values)
    assert np.array_equal(mapping['y'], df_basic['b'].values)


def test_quantitative_color():
    mapping = convert.convert_quantitative(chart_color)
    assert np.array_equal(mapping['x'], df_basic['a'].values)
    assert np.array_equal(mapping['y'], df_basic['b'].values)
    assert np.array_equal(mapping['c'], df_basic['c'].values)


def test_quantitative_scatter():
    mapping = convert.convert_quantitative(chart_color)
    plt.scatter(**mapping)
    plt.show()


def test_quantitative_plot():
    mapping = convert.convert_quantitative(chart_x_y)
    args = [mapping.pop('x'), mapping.pop('y')]
    plt.plot(*args, **mapping)
    plt.show()


@pytest.mark.skip(reason="aggregate functions not implemented yet")
def test_quantitative_x_count_y():
    mapping = convert.convert_quantitative(chart_x_count_y)
    assert np.array_equal(mapping['x'], df_count['a'].values)
    assert np.array_equal(mapping['y'], df_count.groupby(['a']).count().values)
