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
from plotly.subplots import make_subplots


today = datetime.datetime(
    datetime.datetime.today().year,
    datetime.datetime.today().month,
    datetime.datetime.today().day,
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

server = app.server

# get indicators needed for the first plot
indicators = ds.get_indicators_dataset(cases, hospital, tests, vaccines, today)

# template text to be used for the title of each indicator
title_template = "<span style='font-size:0.8em;'>{}</span>"
graph_color = '#3498db'
figure_height = 225

# initiating figure and adding traces with each indicator
# from the received dataset
fig_indicators = go.Figure()
fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.INC_RATE_T],
        delta={
            "reference": indicators[c.INC_RATE_T14],
            "relative": True,
            "increasing": {"color": "#FF4136"},
            "decreasing": {"color": "#3D9970"},
        },
        domain={"row": 0, "column": 0},
        title={"text": title_template.format("Incident Rate (last 14 days)")},
    )
)

fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.CASES_T],
        delta={
            "reference": indicators[c.CASES_T14],
            "relative": True,
            "increasing": {"color": "#FF4136"},
            "decreasing": {"color": "#3D9970"},
        },
        domain={"row": 0, "column": 1},
        title={"text": title_template.format("Cases Daily Average last 14 days)")},
    )
)

fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.HOSP_T],
        delta={
            "reference": indicators[c.HOSP_T14],
            "relative": True,
            "increasing": {"color": "#FF4136"},
            "decreasing": {"color": "#3D9970"},
        },
        domain={"row": 1, "column": 0},
        title={
            "text": title_template.format(
                "Hospitalisations Daily Average (last 14 days)"
            )
        },
    )
)

fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.TESTS_T],
        number={"valueformat": "%"},
        delta={
            "reference": indicators[c.TESTS_T14],
            "relative": True,
            "increasing": {"color": "#FF4136"},
            "decreasing": {"color": "#3D9970"},
        },
        domain={"row": 1, "column": 1},
        title={"text": title_template.format("Positivity Rate (last 14 days)")},
    )
)

fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.FD_VACCINE_T],
        delta={"reference": indicators[c.FD_VACCINE_T14], "relative": True},
        domain={"row": 2, "column": 0},
        title={"text": title_template.format("First Dose Vaccination")},
    )
)

fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.FD_PERCENTAGE_T],
        delta={"reference": indicators[c.FD_PERCENTAGE_T14], "relative": True},
        number={"valueformat": "%"},
        domain={"row": 2, "column": 1},
        title={"text": title_template.format("18+ First Dose Coverage")},
    )
)

fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.SD_VACCINE_T],
        delta={"reference": indicators[c.SD_VACCINE_T14], "relative": True},
        domain={"row": 3, "column": 0},
        title={"text": title_template.format("Fully Vaccinated")},
    )
)

fig_indicators.add_trace(
    go.Indicator(
        mode="number+delta",
        value=indicators[c.SD_PERCENTAGE_T],
        delta={"reference": indicators[c.SD_PERCENTAGE_T14], "relative": True},
        number={"valueformat": "%"},
        domain={"row": 3, "column": 1},
        title={"text": title_template.format("18+ Fully Vaccinated Coverage")},
    )
)

fig_indicators.update_layout(
    grid={"rows": 4, "columns": 2, "ygap": 0.4},
    margin={"l": 30, "r": 30, "t": 50, "b": 40},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"color": "#fff"}
)


# create subplot for cases and hospitalisations graphs
fig_cases_hospital = make_subplots(
    rows=2, cols=1,
    subplot_titles=['Daily new cases', 'Daily hospitalisations'])

# retrieve data for subplots / plots
cases_graph_data = ds.get_cases_graph_data(cases)
hospital_graph_data = ds.get_hospital_graph_data(hospital)
positivity_graph_data = ds.get_positivity_rate_graph_data(tests)
vaccination_graph_data = ds.get_vaccination_graph_data(vaccines)

layout = go.Layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"color": "#fff"},
    showlegend=False,
    height=225,
    margin={
        't': 50,
        'b': 40
    },
    title={
        'x': 0.5
    }
)

fig_cases = go.Figure(layout=layout)
fig_hospital = go.Figure(layout=layout)

fig_cases.add_trace(
    go.Scatter(
        x=cases_graph_data[c.DATE],
        y=cases_graph_data[c.CASES_MA],
        name='Cases',
        line_shape='spline',
        line={'color': graph_color}
    )
)


fig_hospital.add_trace(
    go.Scatter(
        x=hospital_graph_data[c.DATE],
        y=hospital_graph_data[c.HOSP_MA],
        name='Hospitalisations',
        line_shape='spline',
        line={'color': graph_color}
    )
)


fig_cases.update_layout(
    title={'text': 'Daily new cases'}
)

fig_hospital.update_layout(
    title={'text': 'Daily hospitalisations'}
)

fig_vaccination = go.Figure(layout=layout)

fig_vaccination.add_trace(
    go.Scatter(
        x=vaccination_graph_data[c.DATE],
        y=vaccination_graph_data[c.FD_VACCINE_T],
        name='First dose'
    )
)

fig_vaccination.add_trace(
    go.Scatter(
        x=vaccination_graph_data[c.DATE],
        y=vaccination_graph_data[c.SD_VACCINE_T],
        name='Fully vaccinated'
    )
)

fig_vaccination.update_layout(
    title={
        'text':'Vaccination progress'
        }
)

fig_pos_rate = go.Figure(layout=layout)

fig_pos_rate.add_trace(
    go.Scatter(
        x=positivity_graph_data[c.DATE],
        y=positivity_graph_data[c.POS_RATE_MA],
        name='Positivity Rate'
    )
)

fig_pos_rate.update_layout(
    title={
        'text':'Positivity Rate'
        },
    yaxis={
        'tickformat': '%'
    }
)

app.layout = html.Div(
    children=[
        html.H1("COVID-19 Belgium Dashboard", style={
            'text-align': 'center',
            'margin': '20px'
        }),
        dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id="fig_indicators", figure=fig_indicators,
                            config={'displaylogo': False}
                        )
                    )
                ,xl=6, lg=6, md=12, xs=12),
                dbc.Col(children=[
                    dbc.Row(
                        dbc.Col(
                            html.Div(dcc.Graph(
                                id="fig_cases_hospital", figure=fig_cases,
                                config={'displaylogo': False}
                                )
                            )
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(dcc.Graph(
                                id="fig_hospital", figure=fig_hospital,
                                config={'displaylogo': False}
                                )
                            )
                        )
                    )
                ]
                ,xl=6, lg=6, md=12, xs=12)
            ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(
                        id='fig_vaccination', figure=fig_vaccination,
                        config={'displaylogo': False}
                    )
                )
                ,xl=6, lg=6, md=12, xs=12
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(
                        id='fig_positivity_rate', figure=fig_pos_rate,
                        config={'displaylogo': False}
                    )
                )
            ,xl=6, lg=6, md=12, xs=12
            )
        ], align="center")
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
