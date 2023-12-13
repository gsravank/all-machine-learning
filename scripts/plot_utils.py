"""
Module for utility functions to help visualize data

"And God said, Let there be light: and there was light."
"""

import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


pyo.init_notebook_mode()


def get_plotly_yaxes(given_yaxes, start_num=0):
    """List of Y-Axis classes for a plot

    Args:
        given_yaxes (list): List of class names for y-axes
        start_num (int): Starting number for Y-axes

    Return:
        list: List of y-axis names for plotly
    """
    unique_vals = list(set(given_yaxes))
    plotly_yaxes = ['y{}'.format(unique_vals.index(val) + 1 + start_num)
                    for val in given_yaxes]

    return plotly_yaxes


def plotly_plot(xs, ys, names, modes=[], yaxes=[], line_styles=[], texts=[], line_shapes=[], height=700, 
                width=500, title='', return_fig=False, return_traces=False, autosize=True):
    """Plotly plot for any number of xs, ys

    Args:
        xs (list of list): List of list of X-axis values 
        ys (list of list): List of list of Y-axis values
        modes (list of str): List of modes for each plot (either 'lines' or 'lines+marker' or 'markers')
        yaxes (list): List of yaxis types (discrete classes)
        line_styles (list): List of line styles (solid or dash or dot or dashdot)
        line_shapes (list): List of shapes (hv, vh, hh, vv)
        texts (list of list): List of texts to be associated with each point
        height (int): Height of plot
        width (int): Width of plot
        title (str): Title of plot
        return_fig (bool): Return plotly figure object or not
        return_traces (bool): Return list of traces instead of plotting
        autosize (bool): Autosize width of plot

    Example:
        yaxes = [0, 0, 1, 1, 2] will mean that 
        first two plots are on the same y-axis, 
        the next two are on the next y-axis and (different from the first 2 plots)
        the last one is the last y-axis

        [0, 0, 1, 1, 2] equivalent to ['y1', 'y1', 'y2', 'y2', 'y3'] equivalent to ['cat', 'cat', 'dog', 'dog', 'snake']

    """
    # Check for errors
    if len(xs) != len(ys):
        print("Faulty input. Size mismatch between xs and ys")
        return

    if len(modes) != 0 and len(modes) != len(xs):
        print("Faulty input. Size mismatch between xs (or ys) and modes")
        return

    if len(yaxes) != 0 and len(yaxes) != len(xs):
        print("Faulty input. Size mismatch between xs (or ys) and yaxes")
        return

    if len(line_styles) != 0 and len(line_styles) != len(xs):
        print("Faulty input. Size mismatch between xs (or ys) and line_styles")
        return

    if len(texts) != 0 and len(texts) != len(xs):
        print("Faulty input. Size mismatch between xs (or ys) and texts")
        return

    if len(line_shapes) != 0 and len(line_shapes) != len(xs):
        print("Faulty input. Size mismatch between xs (or ys) and line_shapes")
        return

    # Get y-axes
    if len(yaxes) == 0:
        yaxes = ['y1' for _ in xs]
    else:
        yaxes = get_plotly_yaxes(yaxes)
            
    # Get modes
    if len(modes) == 0:
        modes = ['lines' for x in range(len(xs))]

    # Get line-styles
    if len(line_styles) == 0:
        line_styles = ['solid' for _ in range(len(xs))]

    # Get texts
    if len(texts) == 0:
        texts = [[] for _ in range(len(xs))]

    # Get line-shapes
    if len(line_shapes) == 0:
        line_shapes = ['linear' for _ in range(len(xs))]
    
    traces = list()
    for x, y, name, mode, yax, line_style, txt, line_shape in zip(xs, ys, names, modes, yaxes, line_styles, texts, line_shapes):
        if yax != 'y1':
            traces.append(go.Scatter(x=x, y=y, mode=mode, name=name, yaxis=yax, line={
                          'dash': line_style}, text=txt, line_shape=line_shape))
        else:
            traces.append(go.Scatter(x=x, y=y, mode=mode, name=name, line={
                          'dash': line_style}, text=txt, line_shape=line_shape))

    if return_traces:
        return traces
   
    if autosize: 
        fig = go.Figure(data=traces, layout=go.Layout(height=height))
    else:
        fig = go.Figure(data=traces, layout=go.Layout(height=height, width=width))

    # Update layout to plot multiple yaxes on the same plot
    num_unique_yaxes = len(set([trace.yaxis for trace in traces]))
    if num_unique_yaxes >= 2:
        fig.update_layout(yaxis2=dict(
            anchor="free", overlaying="y", side="left", position=0.02))
    if num_unique_yaxes >= 3:
        fig.update_layout(yaxis3=dict(
            anchor="free", overlaying="y", side="right", position=1.0))
    if num_unique_yaxes >= 4:
        fig.update_layout(yaxis4=dict(
            anchor="free", overlaying="y", side="right", position=0.98))
    if num_unique_yaxes >= 5:
        fig.update_layout(yaxis5=dict(
            anchor="free", overlaying="y", side="right", position=0.96))
    if num_unique_yaxes >= 6:
        fig.update_layout(yaxis6=dict(
            anchor="free", overlaying="y", side="right", position=0.94))
    if num_unique_yaxes >= 7:
        fig.update_layout(yaxis7=dict(
            anchor="free", overlaying="y", side="right", position=0.92))
    if num_unique_yaxes >= 8:
        fig.update_layout(yaxis8=dict(
            anchor="free", overlaying="y", side="right", position=0.90))
    if num_unique_yaxes >= 9:
        fig.update_layout(yaxis9=dict(
            anchor="free", overlaying="y", side="right", position=0.88))
    if num_unique_yaxes >= 10:
        fig.update_layout(yaxis10=dict(
            anchor="free", overlaying="y", side="right", position=0.86))
    if num_unique_yaxes >= 11:
        fig.update_layout(yaxis11=dict(
            anchor="free", overlaying="y", side="right", position=0.84))
    if num_unique_yaxes >= 12:
        print("Max supported unique Y-axes is 11")
        return

    # Add title
    if len(title):
        fig.update_layout(title=title)

    if not return_fig:
        pyo.iplot(fig)

    if return_fig:
        return fig
    else:
        return


def plotly_columns(df, columns, names=None, date=None, stime=None, etime=None, modes=[], yaxes=[], line_styles=[], texts=[], 
                   line_shapes=[], height=700, width=500, title='', return_fig=False, return_traces=False, autosize=True):
    """
    Plot given column of dataframe

    Args:
        df (pd.DataFrame): Dataframe
        columns (list): Names of columns
        names (list): Names to use for display
        date (str): Date in YYYYMMDD format
        stime (str): Time in hhmmssffffff format
        etime (str): Time in hhmmssffffff format
        modes (list of str): List of modes for each plot (either 'lines' or 'lines+marker' or 'markers')
        yaxes (list): List of yaxis types (discrete classes)
        line_styles (list): List of line styles (solid or dash or dot or dashdot)
        texts (list of list): List of texts to be associated with each point
        line_shapes (list): List of shapes (hv, vh, hh, vv)
        height (int): Height of plot
        width (int): Width of plot
        title (str): Title of plot
        return_fig (bool): Return plotly figure object or not
        return_traces (bool): Return list of traces instead of plotting
        autosize (bool): Autosize width of plot
    """
    if date is not None and stime is not None and etime is not None:
        tmp_df = time_slice(df, date, stime, etime)
    else:
        tmp_df = df
    
    xs = [tmp_df.index for _ in columns]
    ys = [tmp_df[col] for col in columns]
    if names is None:
        names = columns
        
    return plotly_plot(xs, ys, names, modes, yaxes, line_styles, texts, line_shapes, height, width, title, return_fig, return_traces, autosize)


def plotly_traces(traces, height=700, width=500, autosize=True, yaxes=[], title="", return_fig=False):
    """Plot given Plotly trace objects collected from other plotly plot functions
    
    Args:
        traces (list): List of go.Scatter objects
        height (int): Height of plot
        title (str): Title to be used for plot
        return_fig (bool): Flag to return final figure object
    """
    if len(yaxes) != 0 and len(yaxes) != len(traces):
        print("Faulty input. Size mismatch between xs (or ys) and modes")
        return

    if len(yaxes):
        yaxes = get_plotly_yaxes(yaxes)
        tmp_traces = list()
        for yax, trace in zip(yaxes, traces):
            trace.yaxis = yax
            tmp_traces.append(trace)
        traces = tmp_traces

    if autosize: 
        fig = go.Figure(data=traces, layout=go.Layout(height=height))
    else:
        fig = go.Figure(data=traces, layout=go.Layout(height=height, width=width))

    # Update layout to plot multiple yaxes on the same plot
    num_unique_yaxes = len(set([trace.yaxis for trace in traces]))
    if num_unique_yaxes >= 2:
        fig.update_layout(yaxis2=dict(
            anchor="free", overlaying="y", side="left", position=0.02))
    if num_unique_yaxes >= 3:
        fig.update_layout(yaxis3=dict(
            anchor="free", overlaying="y", side="right", position=1.0))
    if num_unique_yaxes >= 4:
        fig.update_layout(yaxis4=dict(
            anchor="free", overlaying="y", side="right", position=0.98))
    if num_unique_yaxes >= 5:
        fig.update_layout(yaxis5=dict(
            anchor="free", overlaying="y", side="right", position=0.96))
    if num_unique_yaxes >= 6:
        fig.update_layout(yaxis6=dict(
            anchor="free", overlaying="y", side="right", position=0.94))
    if num_unique_yaxes >= 7:
        fig.update_layout(yaxis7=dict(
            anchor="free", overlaying="y", side="right", position=0.92))
    if num_unique_yaxes >= 8:
        print("Max supported unique Y-axes is 8")
        return

    # Add title
    if len(title):
        fig.update_layout(title=title)

    if not return_fig:
        pyo.iplot(fig)

    if return_fig:
        return fig
    else:
        return



def plotly_subplots(lists_of_lists_of_traces, title="", height=700, width=1000, autosize=False, 
                    subplot_titles=[], return_fig=False, shared_yaxes=False, shared_xaxes=False):
    """
    Plot multiple subplots in a grid in one figure
    
    Args:
        lists_of_lists_of_traces (list): Should be of shape (m, n) for a grid of shape mxn
        title (str): Title of figure
        height (int): Height of figure
        width (int): Width of figure
        autosize (bool): Autosize figure to width of cell in a jupyter notebook or not
        subplot_titles (list): List of strings to be used as titles of individual plots in the figure
        return_fig (bool): Return the figure object or not
        shared_yaxes (bool): Make y-axis same for all subplots
        shared_xaxes (bool): Make x-axis same for all subplots
    
    Returns:
        None or go.Figure
    """
    num_rows = len(lists_of_lists_of_traces)
    num_cols = len(lists_of_lists_of_traces[0])
    
    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=subplot_titles, 
                        shared_yaxes=shared_yaxes, shared_xaxes=shared_xaxes)
    
    for rnum in range(num_rows):
        for cnum in range(num_cols):
            curr_traces = lists_of_lists_of_traces[rnum][cnum]
            for trace in curr_traces:
                fig.append_trace(trace, row=rnum+1, col=cnum+1)
                
    if autosize:
        _ = fig.update_layout(height=height, width=width, title_text=title)
    else:
        _ = fig.update_layout(height=height, title_text=title)
    
    if not return_fig:
        pyo.iplot(fig)
        return
    else:
        return fig

