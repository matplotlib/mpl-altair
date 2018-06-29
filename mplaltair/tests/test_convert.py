import matplotlib
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import numpy as np
import mplaltair._convert as convert
import pytest

df_basic = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, 3],
    "s": [50, 100, 200.0], "alpha": [.1, .5, .8], "shape": [1, 2, 3]
})
chart_x_y = alt.Chart(df_basic).mark_point().encode(alt.X(field='a', type='quantitative'), alt.Y('b'))
chart_opacity = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), opacity=alt.value(.5)
)
chart_opacity_fail = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Opacity('alpha')
)
chart_shape = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Color('c:Q'), alt.Shape('shape')
)
chart_all = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Color('c:Q'), alt.Size('s')
)

df_count = pd.DataFrame({"a": [1, 1, 2, 3, 5], "b": [1.4, 1.4, 2.9, 3.18, 5.3]})
chart_x_count_y = alt.Chart(df_count).mark_point().encode(alt.X('a'), alt.Y('count()'))


def test_quantitative_x_y():
    mapping = convert.convert_quantitative(chart_x_y)
    assert list(mapping['x']) == list(df_basic['a'].values), "x values did not match expected x values"
    assert list(mapping['y']) == list(df_basic['b'].values), "y values did not match expected y values"


def test_quantitative_color():
    mapping = convert.convert_quantitative(chart_all)
    assert list(mapping['c']) == list(df_basic['c'].values)


def test_quantitative_opacity_value():
    mapping = convert.convert_quantitative(chart_opacity)
    assert mapping['alpha'] == 0.5


def test_quantitative_size():
    mapping = convert.convert_quantitative(chart_all)
    assert list(mapping['s']) == list(df_basic['s'].values)


@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
def test_quantitative_opacity_array():
    convert.convert_quantitative(chart_opacity_fail)


@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
def test_quantitative_shape():
    mapping = convert.convert_quantitative(chart_shape)
    assert list(mapping['marker']) == list(df_basic['shape'].values)


@pytest.mark.parametrize("chart", [chart_all, chart_opacity])
def test_quantitative_scatter(chart):
    mapping = convert.convert_quantitative(chart)
    plt.scatter(**mapping)
    plt.show()


@pytest.mark.xfail(raises=NotImplementedError, reason="WIP")
def test_quantitative_x_count_y():
    mapping = convert.convert_quantitative(chart_x_count_y)
    assert list(mapping['x']) == list(df_count['a'].values)
    assert list(mapping['y']) == list(df_count.groupby(['a']).count().values)
