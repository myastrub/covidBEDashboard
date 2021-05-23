import datasets as ds
from datasets import df_cases, vaccines, tests, hospital
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

indicators = ds.get_indicators_dataset(df_cases, hospital, tests, vaccines, today)
title_template = "<span style='font-size:0.6em;'>{}</span>"

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
    title = {
        'text': title_template.format(
            'Incident Rate (last 14 days)')
    }
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
    title={
        'text': title_template.format(
            'Cases Daily Average last 14 days)'
            )}
))

fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.HOSP_T],
    delta = {
        'reference': indicators[c.HOSP_T14], 
        'relative':True,
        'increasing': {
            'color': '#FF4136'
        },
        'decreasing': {
            'color':'#3D9970'
        }},
    domain={'row': 1, 'column': 0},
    title={
        'text': title_template.format(
            'Hospitalisations Daily Average (last 14 days)')
        }
))

fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.TESTS_T],
    number={'valueformat': '%'},
    delta = {
        'reference': indicators[c.TESTS_T14], 
        'relative':True,
        'increasing': {
            'color': '#FF4136'
        },
        'decreasing': {
            'color':'#3D9970'
        }},
    domain={'row': 1, 'column': 1},
    title={
        'text': title_template.format(
            'Positivity Rate (last 14 days)')
        }
))

fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.FD_VACCINE_T],
    delta = {
        'reference': indicators[c.FD_VACCINE_T14], 
        'relative':True},
    domain={'row': 2, 'column': 0},
    title={
        'text': title_template.format(
            'First Dose Vaccination')
        }
))

fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.FD_PERCENTAGE_T],
    delta = {
        'reference': indicators[c.FD_PERCENTAGE_T14], 
        'relative':True},
    number={'valueformat': '%'},
    domain={'row': 2, 'column': 1},
    title={
        'text': title_template.format(
            '18+ First Dose Coverage')
        }
))

fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.SD_VACCINE_T],
    delta = {
        'reference': indicators[c.SD_VACCINE_T14], 
        'relative':True},
    domain={'row': 3, 'column': 0},
    title={
        'text': title_template.format(
            'Fully Vaccinated')
        }
))

fig_indicators.add_trace(go.Indicator(
    mode='number+delta',
    value = indicators[c.SD_PERCENTAGE_T],
    delta = {
        'reference': indicators[c.SD_PERCENTAGE_T14], 
        'relative':True},
    number={'valueformat': '%'},
    domain={'row': 3, 'column': 1},
    title={
        'text': title_template.format(
            '18+ Fully Vaccinated Coverage')
        }
))

fig_indicators.update_layout(
    grid={'rows': 4, 'columns': 2, 'ygap': 0.4},
    margin={'l': 30, 'r': 30, 't': 80, 'b': 50},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font={'color': '#fff'}
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