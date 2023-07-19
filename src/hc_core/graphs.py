
import functools

import typing
import numpy
import pandas

import plotly.express
from plotly.express.colors import sample_colorscale

from . import rendering

# ---------------------------------------------------------------

RENDERING = {None: None}
HTML = "HTML"

def set_rendering(val):
    RENDERING[None] = val

def return_chart(fig):
    if RENDERING[None] == HTML:
        return rendering.render_as_html(fig)
    return fig

# ---------------------------------------------------------------

def df_color_scale(df, col, color_scale):
    colors = sample_colorscale(
        color_scale, 
        numpy.linspace(0, 1, len(df[col].unique()))
    )
    color_map = {
        k: v for k, v in zip(
            sorted(df[col].unique()),
            colors,
        )
    }
    return color_map

# ---------------------------------------------------------------

def df_chart(
    df,
    x="date",
    y="value",
    title=None,
    color: typing.Optional[str]=None,
    color_scale=None,
    width=750,
    height=400,
    f_plot = plotly.express.line,
    fig=None,
    **kws,
):

    if color is not None:
        kws["color"] = color

    if color_scale is not None:
        kws["color_discrete_map"] = df_color_scale(
            df,
            color,
            color_scale
        )

    chart = f_plot(
        data_frame=df,
        x=x,
        y=y,
        title=title,
        **kws,
    )
    if fig is None:
        fig = chart
    else:
        fig.add_trace(chart.data[0])
        
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
    )

    return return_chart(fig)

df_line_chart = functools.partial(
    df_chart,
    f_plot = plotly.express.line,
    render_mode="svg",
    #
)

df_bar_chart = functools.partial(
    df_chart,
    f_plot = plotly.express.bar,
    #
)

df_scatter_chart = functools.partial(
    df_chart,
    f_plot = plotly.express.scatter,
    render_mode="svg",
    #
)

# ---------------------------------------------------------------

def df_facet_chart(
    df,
    x="date",
    y="value",
    title=None,
    facet=None,
    facet_row=None,
    facet_col=None,
    color=None,
    color_scale=None,
    share_y=False,
    share_x=False,
    width=750,
    height=400,
    fig=None,
    f_plot = plotly.express.line,
    **kws,
):
    if facet_row is None and facet is not None:
        assert facet_col is None, facet_col
        facet_row = facet

    if color is not None:
        kws["color"] = color

    if color_scale is not None:
        kws["color_discrete_map"] = df_color_scale(
            df,
            color,
            color_scale
        )

    chart = f_plot(
        data_frame=df,
        x=x,
        y=y,
        facet_row=facet_row,
        facet_col=facet_col,
        title=title,
        **kws,
    )
    if fig is None:
        fig = chart
    else:
        fig.add_trace(chart.data[0])

    if not share_x:
        fig.update_xaxes(matches=None, showticklabels=True)
    if not share_y:
        fig.update_yaxes(matches=None, showticklabels=True)

    fig.update_layout(
        autosize=False,
        width=width,
        height=height * len(df[facet_row].unique()),
    )

    return return_chart(fig)

df_facet_line_chart = functools.partial(
    df_facet_chart,
    f_plot = plotly.express.line,
    render_mode="svg",
    #
)

df_facet_bar_chart = functools.partial(
    df_facet_chart,
    f_plot = plotly.express.bar,
    #
)

df_facet_scatter_chart = functools.partial(
    df_facet_chart,
    f_plot = plotly.express.scatter,
    render_mode="svg",
    #
)

# ---------------------------------------------------------------
