import datasets as ds
from datasets import cases, vaccines, tests, hospital
import constants as c
import pandas as pd
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


today = datetime.datetime(
    datetime.datetime.today().year, 
    datetime.datetime.today().month,
    datetime.datetime.today().day)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

indicators = ds.get_indicators_dataset(cases, hospital, tests, vaccines, today)

fig_indicators = go.Figure()
fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.INC_RATE_T],
    delta = {
        'reference': indicators[c.INC_RATE_T14], 
        'relative':True,
        'increasing': {
            'color': '#FF4136'
        },
        'decreasing': {
            'color':'#3D9970'
        }},
    domain={'row': 0, 'column': 0},
    title = {'text': 'Incident Rate (last 14 days)'}
))

fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.CASES_T],
    delta = {
        'reference': indicators[c.CASES_T14], 
        'relative':True,
        'increasing': {
            'color': '#FF4136'
        },
        'decreasing': {
            'color':'#3D9970'
        }},
    domain={'row': 0, 'column': 1},
    title={'text': 'Last 14 days Daily Average'}
))

fig_indicators.update_layout(
    grid={'rows': 4, 'columns': 2}
)


app.layout = html.Div(children=[
    html.H1("Test app"),
    dbc.Row([
        dbc.Col(
            dbc.Row(
                dbc.Col(
                    html.Div(dcc.Graph(figure=fig_indicators))
                )
            )
        ),
        dbc.Col(
            dbc.Row(
                dbc.Col(
                    html.Div(dbc.Alert("1 Row, 2 Column, 1 subcolum"))
                )
            )
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)