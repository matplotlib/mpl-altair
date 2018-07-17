import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import mplaltair._quantitative as convert
import pytest

df_basic = pd.DataFrame({
    "a": [1, 2, 3], "b": [1.2, 2.4, 3.8], "c": [7, 5, 3],
    "s": [50, 100, 200.0], "alpha": [.1, .5, .8], "shape": [1, 2, 3], "fill": [1, 2, 3]
})

# Charts for implemented channels
chart_all = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Color('c:Q'), alt.Size('s'), opacity=alt.value(.5)
)
chart_fill = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Fill('fill:Q')
)

df_count = pd.DataFrame({"a": [1, 1, 2, 3, 5], "b": [1.4, 1.4, 2.9, 3.18, 5.3]})
chart_x_count_y = alt.Chart(df_count).mark_point().encode(alt.X('a'), alt.Y('count()'))


def test_x_y_quantitative_success():
    chart = alt.Chart(df_basic).mark_point().encode(alt.X(field='a', type='quantitative'), alt.Y('b'))
    mapping = convert.convert_quantitative(chart)
    assert list(mapping['x']) == list(df_basic['a'].values), "x values did not match expected x values"
    assert list(mapping['y']) == list(df_basic['b'].values), "y values did not match expected y values"


@pytest.mark.xfail(raises=NotImplementedError, reason="It doesn't make sense to have x2 and y2 on scatter plots")
def test_x2_y2_quantitative_fail():
    chart = alt.Chart(df_basic).mark_point().encode(alt.X('a'), alt.Y('b'), alt.X2('c'), alt.Y2('alpha'))
    convert.convert_quantitative(chart)


def test_color_quantitative_success():
    chart = alt.Chart(df_basic).mark_point().encode(alt.Color('c:Q'))
    mapping = convert.convert_quantitative(chart)
    assert list(mapping['c']) == list(df_basic['c'].values)


def test_fill_quantitative_success():
    chart = alt.Chart(df_basic).mark_point().encode(alt.Fill('fill:Q'))
    mapping = convert.convert_quantitative(chart)
    assert list(mapping['c']) == list(df_basic['fill'].values)


def test_opacity_value_quantitative_success():
    chart = alt.Chart(df_basic).mark_point().encode(opacity=alt.value(.5))
    mapping = convert.convert_quantitative(chart)
    assert mapping['alpha'] == 0.5


@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
def test_opacity_array_quantitative_fail():
    chart = alt.Chart(df_basic).mark_point().encode(alt.Opacity('alpha'))
    convert.convert_quantitative(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
def test_shape_quantitative_fail():
    chart = alt.Chart(df_basic).mark_point().encode(alt.Shape('shape'))
    mapping = convert.convert_quantitative(chart)


def test_size_quantitative_success():
    chart = alt.Chart(df_basic).mark_point().encode(alt.Size('s'))
    mapping = convert.convert_quantitative(chart)


@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well supported in Altair")
def test_stroke_quantitative_fail():
    chart = alt.Chart(df_basic).mark_point().encode(alt.Stroke('fill'))
    convert.convert_quantitative(chart)


@pytest.mark.parametrize("chart", [chart_all, chart_fill])
def test_scatter_quantitative(chart):
    mapping = convert.convert_quantitative(chart)
    plt.scatter(**mapping)
    plt.show()


@pytest.mark.xfail(raises=NotImplementedError, reason="Aggregate functions are not supported yet")
def test_quantitative_x_count_y():
    chart = alt.Chart(df_count).mark_point().encode(alt.X('a'), alt.Y('count()'))
    mapping = convert.convert_quantitative(chart)
    assert list(mapping['x']) == list(df_count['a'].values)
    assert list(mapping['y']) == list(df_count.groupby(['a']).count().values)
