import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from home import home_layout
from prediction import prediction_layout, predict_aqi

# suppress_callback_exceptions: allow for the ids to be added later.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "AQI Predictor"

# Define the navbar with two navigation items
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Prediction", href="/prediction")),
    ],
    brand="ML-Project-2024",
    color="primary",
    dark=True,
)

# Define the layout with a navbar and a container for page content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', className='p-4')
])

# Callback to update page content based on the URL path
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/prediction':
        return prediction_layout
    else:
        return home_layout

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port = 8050, debug=True)
