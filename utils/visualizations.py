"""
Visualization utilities using Plotly for interactive charts
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import PRIMARY_COLOR, CHART_COLOR_SCHEME


def create_spend_trend_chart(spend_series, title="Spend Over Time"):
    """
    Create line chart for spend trends over time

    Args:
        spend_series: Series with spend by period (index should be period)
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if spend_series.empty:
        return go.Figure()

    # Convert period index to timestamp for plotting
    dates = spend_series.index.to_timestamp()
    values = spend_series.values

    fig = go.Figure()

    # Add line trace
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name='Spend',
        line=dict(color=PRIMARY_COLOR, width=3),
        marker=dict(size=8, color=PRIMARY_COLOR),
        hovertemplate='<b>%{x|%B %Y}</b><br>Spend: $%{y:,.0f}<extra></extra>'
    ))

    # Add trend line
    if len(dates) > 1:
        z = np.polyfit(range(len(dates)), values, 1)
        p = np.poly1d(z)
        trend_values = p(range(len(dates)))

        fig.add_trace(go.Scatter(
            x=dates,
            y=trend_values,
            mode='lines',
            name='Trend',
            line=dict(color='red', width=2, dash='dash'),
            hovertemplate='<b>Trend</b><br>$%{y:,.0f}<extra></extra>'
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Spend ($)",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        showlegend=True
    )

    fig.update_yaxes(tickformat='$,.0f')

    return fig


def create_category_pie_chart(category_spend, title="Spend by Category", hole=0.4):
    """
    Create pie/donut chart for category breakdown

    Args:
        category_spend: Series with spend by category
        title: Chart title
        hole: Size of hole for donut chart (0 = pie, 0.4 = donut)

    Returns:
        plotly.graph_objects.Figure
    """
    if category_spend.empty:
        return go.Figure()

    fig = go.Figure(data=[go.Pie(
        labels=category_spend.index,
        values=category_spend.values,
        hole=hole,
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Spend: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>',
        marker=dict(colors=px.colors.sequential.Blues_r)
    )])

    fig.update_layout(
        title=title,
        template='plotly_white',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )

    return fig


def create_supplier_bar_chart(supplier_spend, title="Top Suppliers by Spend", n=20, orientation='h'):
    """
    Create horizontal bar chart for top suppliers

    Args:
        supplier_spend: Series with spend by supplier
        title: Chart title
        n: Number of suppliers to show
        orientation: 'h' for horizontal, 'v' for vertical

    Returns:
        plotly.graph_objects.Figure
    """
    if supplier_spend.empty:
        return go.Figure()

    # Get top N
    top_n = supplier_spend.nlargest(n)

    if orientation == 'h':
        # Horizontal bar chart (reverse order for better readability)
        fig = go.Figure(data=[go.Bar(
            x=top_n.values,
            y=top_n.index,
            orientation='h',
            marker=dict(
                color=top_n.values,
                colorscale='Blues',
                showscale=False
            ),
            hovertemplate='<b>%{y}</b><br>Spend: $%{x:,.0f}<extra></extra>'
        )])

        fig.update_layout(
            title=title,
            xaxis_title="Spend ($)",
            yaxis_title="Supplier",
            yaxis={'categoryorder': 'total ascending'},
            height=max(400, n * 25),  # Dynamic height based on number of suppliers
            template='plotly_white'
        )

        fig.update_xaxes(tickformat='$,.0f')

    else:
        # Vertical bar chart
        fig = go.Figure(data=[go.Bar(
            x=top_n.index,
            y=top_n.values,
            marker=dict(
                color=top_n.values,
                colorscale='Blues',
                showscale=False
            ),
            hovertemplate='<b>%{x}</b><br>Spend: $%{y:,.0f}<extra></extra>'
        )])

        fig.update_layout(
            title=title,
            xaxis_title="Supplier",
            yaxis_title="Spend ($)",
            xaxis={'categoryorder': 'total descending'},
            height=400,
            template='plotly_white'
        )

        fig.update_yaxes(tickformat='$,.0f')
        fig.update_xaxes(tickangle=-45)

    return fig


def create_state_choropleth(state_spend, title="Spend by State"):
    """
    Create US choropleth map for spend by state

    Args:
        state_spend: Series with spend by state
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if state_spend.empty:
        return go.Figure()

    fig = go.Figure(data=go.Choropleth(
        locations=state_spend.index,
        z=state_spend.values,
        locationmode='USA-states',
        colorscale='Blues',
        colorbar_title="Spend ($)",
        hovertemplate='<b>%{location}</b><br>Spend: $%{z:,.0f}<extra></extra>',
        marker_line_color='white',
        marker_line_width=1
    ))

    fig.update_layout(
        title_text=title,
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        height=500,
        template='plotly_white'
    )

    return fig


def create_state_bar_chart(state_spend, title="Top States by Spend", n=10):
    """
    Create bar chart for top states

    Args:
        state_spend: Series with spend by state
        title: Chart title
        n: Number of states to show

    Returns:
        plotly.graph_objects.Figure
    """
    if state_spend.empty:
        return go.Figure()

    top_n = state_spend.nlargest(n)

    fig = go.Figure(data=[go.Bar(
        x=top_n.index,
        y=top_n.values,
        marker=dict(
            color=top_n.values,
            colorscale='Blues',
            showscale=False
        ),
        hovertemplate='<b>%{x}</b><br>Spend: $%{y:,.0f}<extra></extra>'
    )])

    fig.update_layout(
        title=title,
        xaxis_title="State",
        yaxis_title="Spend ($)",
        xaxis={'categoryorder': 'total descending'},
        height=400,
        template='plotly_white'
    )

    fig.update_yaxes(tickformat='$,.0f')

    return fig


def create_concentration_chart(top_n_spend, remaining_spend, n=20):
    """
    Create pie chart showing concentration of top N suppliers vs rest

    Args:
        top_n_spend: Total spend of top N suppliers
        remaining_spend: Total spend of remaining suppliers
        n: Number of top suppliers

    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure(data=[go.Pie(
        labels=[f'Top {n} Suppliers', 'Other Suppliers'],
        values=[top_n_spend, remaining_spend],
        hole=0.4,
        marker=dict(colors=[PRIMARY_COLOR, '#d0d0d0']),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Spend: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        title=f"Spend Concentration (Top {n} vs Others)",
        template='plotly_white',
        height=400,
        showlegend=True
    )

    return fig


def create_metric_comparison_bar(df_metrics, metric_name, title, top_n=10):
    """
    Create bar chart comparing a specific metric across categories

    Args:
        df_metrics: DataFrame with metrics
        metric_name: Column name of metric to plot
        title: Chart title
        top_n: Number of top items to show

    Returns:
        plotly.graph_objects.Figure
    """
    if df_metrics.empty or metric_name not in df_metrics.columns:
        return go.Figure()

    top_items = df_metrics.nlargest(top_n, metric_name)

    fig = go.Figure(data=[go.Bar(
        x=top_items.index,
        y=top_items[metric_name],
        marker=dict(
            color=top_items[metric_name],
            colorscale='Blues',
            showscale=False
        ),
        hovertemplate='<b>%{x}</b><br>' + metric_name + ': %{y:,.0f}<extra></extra>'
    )])

    fig.update_layout(
        title=title,
        xaxis_title="",
        yaxis_title=metric_name,
        xaxis={'categoryorder': 'total descending'},
        height=400,
        template='plotly_white'
    )

    fig.update_xaxes(tickangle=-45)

    return fig


def create_scatter_plot(df, x_col, y_col, size_col=None, color_col=None, title="Scatter Plot"):
    """
    Create scatter plot

    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        size_col: Column for marker size (optional)
        color_col: Column for marker color (optional)
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        hover_data=df.columns,
        title=title,
        template='plotly_white',
        height=500
    )

    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    return fig


def create_heatmap(data_matrix, x_labels, y_labels, title="Heatmap"):
    """
    Create heatmap

    Args:
        data_matrix: 2D array or DataFrame for heatmap
        x_labels: Labels for x-axis
        y_labels: Labels for y-axis
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=data_matrix,
        x=x_labels,
        y=y_labels,
        colorscale='Blues',
        hovertemplate='%{y}<br>%{x}<br>Value: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        template='plotly_white',
        height=500,
        xaxis={'side': 'bottom'},
        yaxis={'side': 'left'}
    )

    return fig


def create_multi_line_chart(df, x_col, y_cols, title="Multi-Line Chart"):
    """
    Create multi-line chart for comparing multiple series

    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_cols: List of columns for y-axis (multiple lines)
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure()

    colors = px.colors.qualitative.Plotly

    for idx, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[col],
            mode='lines+markers',
            name=col,
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=6)
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title="Value",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        showlegend=True
    )

    return fig


def create_stacked_bar_chart(df, x_col, y_cols, title="Stacked Bar Chart"):
    """
    Create stacked bar chart

    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_cols: List of columns to stack
        title: Chart title

    Returns:
        plotly.graph_objects.Figure
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure()

    for col in y_cols:
        fig.add_trace(go.Bar(
            name=col,
            x=df[x_col],
            y=df[col]
        ))

    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis_title=x_col,
        yaxis_title="Value",
        template='plotly_white',
        height=400,
        showlegend=True
    )

    return fig
