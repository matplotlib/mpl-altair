import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import mplaltair._convert as convert
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
# Charts for channels that aren't implemented yet
chart_x2_y2_fail = alt.Chart(df_basic).mark_point().encode(
    alt.X('a'), alt.Y('b'), alt.X2('c'), alt.Y2('alpha')
)
chart_opacity_fail = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Opacity('alpha')
)
chart_shape_fail = alt.Chart(df_basic).mark_point().encode(
    alt.X(field='a', type='quantitative'), alt.Y('b'), alt.Color('c:Q'), alt.Shape('shape')
)
chart_stroke_fail = alt.Chart(df_basic).mark_point().encode(
    alt.X('a'), alt.Y('b'), alt.Stroke('fill')
)

df_count = pd.DataFrame({"a": [1, 1, 2, 3, 5], "b": [1.4, 1.4, 2.9, 3.18, 5.3]})
chart_x_count_y = alt.Chart(df_count).mark_point().encode(alt.X('a'), alt.Y('count()'))


def test_quantitative_x_y():
    mapping = convert.convert_quantitative(chart_all)
    assert list(mapping['x']) == list(df_basic['a'].values), "x values did not match expected x values"
    assert list(mapping['y']) == list(df_basic['b'].values), "y values did not match expected y values"


@pytest.mark.xfail(raises=NotImplementedError, reason="It doesn't make sense to have x2 and y2 on scatter plots")
def test_quantitative_x2_y2():
    convert.convert_quantitative(chart_x2_y2_fail)


def test_quantitative_color():
    mapping = convert.convert_quantitative(chart_all)
    assert list(mapping['c']) == list(df_basic['c'].values)


def test_quantitative_fill():
    mapping = convert.convert_quantitative(chart_fill)
    assert list(mapping['c']) == list(df_basic['fill'].values)


def test_quantitative_opacity_value():
    mapping = convert.convert_quantitative(chart_all)
    assert mapping['alpha'] == 0.5


@pytest.mark.xfail(raises=NotImplementedError, reason="The alpha argument in scatter() cannot take arrays")
def test_quantitative_opacity_array():
    convert.convert_quantitative(chart_opacity_fail)


@pytest.mark.xfail(raises=NotImplementedError, reason="The marker argument in scatter() cannot take arrays")
def test_quantitative_shape():
    mapping = convert.convert_quantitative(chart_shape_fail)
    assert list(mapping['marker']) == list(df_basic['shape'].values)


def test_quantitative_size():
    mapping = convert.convert_quantitative(chart_all)
    assert list(mapping['s']) == list(df_basic['s'].values)


@pytest.mark.xfail(raises=NotImplementedError, reason="Stroke is not well supported in Altair")
def test_quantitative_stroke():
    convert.convert_quantitative(chart_stroke_fail)


@pytest.mark.parametrize("chart", [chart_all, chart_fill])
def test_quantitative_scatter(chart):
    mapping = convert.convert_quantitative(chart)
    plt.scatter(**mapping)
    plt.show()


@pytest.mark.xfail(raises=NotImplementedError, reason="Aggregate functions are not supported yet")
def test_quantitative_x_count_y():
    mapping = convert.convert_quantitative(chart_x_count_y)
    assert list(mapping['x']) == list(df_count['a'].values)
    assert list(mapping['y']) == list(df_count.groupby(['a']).count().values)
