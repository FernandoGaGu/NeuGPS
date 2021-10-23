# Module that includes the tools for the visualisation of results.
#
# Author: Fernando García Gutiérrez
# Email: fegarc05@ucm.es
#
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def pieChart(data: pd.DataFrame, labels_col: str, values_col: str, **kwargs):
    assert labels_col in data.columns
    assert values_col in data.columns

    fig = go.Figure(data=[go.Pie(labels=data[labels_col], values=data[values_col])])
    fig.update_layout(
        title=dict(
            text=kwargs.get('title', ''),
            y=0.95,
            x=0.5
        ),
        font=dict(
            size=kwargs.get('font_size', 25)
        ),
        template=kwargs.get('template', 'plotly_white'),
        width=1200,
        height=700,
    )

    fig.update_traces(marker=dict(colors=px.colors.qualitative.T10))
    fig.show()
