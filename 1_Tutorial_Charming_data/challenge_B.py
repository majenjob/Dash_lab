## CHALLENGE B ##

# Use plotly express to plot a Line chart
# X-axis should represent Year
# Y-axis should represent % of bee colonies
# Color should represent State
# Dropdown options should be list of things affecting bees

# ------------------------------------------------------------------------------

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Dash_Introduction/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
    html.H2("Challenge B", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_cause",
                 options=[
                     {"label": "Disease", "value": "Disease"},
                     {"label": "Pesticides", "value": "Pesticides"},
                     {"label": "Pesticides excluding Varroa", "value": "Pests_excl_Varroa"},
                     {"label": "Varroa mites", "value": "Varroa_mites"},
                     {"label": "Other", "value": "Other"},
                     {"label": "Unknown", "value": "Unknown"}],
                 multi=False,
                 value="Disease",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_line', figure={})

])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_line', component_property='figure')],
    [Input(component_id='slct_cause', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The cause affecting bees chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Affected by"] == option_slctd]
    # dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.line(
        data_frame=dff,
        x = 'Year',
        y = 'Pct of Colonies Impacted',
        color = 'State',
        template='plotly_dark'
    )

    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

    
# https://youtu.be/hSPmj7mK6ng 