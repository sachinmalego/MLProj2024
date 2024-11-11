import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from home import home_layout
from prediction import prediction_layout

# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Simple Navbar App"

# Define the navbar with two navigation items
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Prediction", href="/prediction")),
    ],
    brand="Dash Navbar App",
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
    app.run_server(debug=True)
