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
    
# # Prediction callback
# @app.callback(
#     [Output("aqi-output", "children"), Output("aqi-badge", "children"), Output("aqi-badge", "color")],
#     [Input("predict-button", "n_clicks")],
#     [State("pm10", "value"), State("no2", "value"), State("so2", "value"), State("co", "value"), State("o3", "value")]
# )
# def update_prediction(n_clicks, pm10, no2, so2, co, o3):
#     if n_clicks > 0 and all([pm10, no2, so2, co, o3]):
#         # Predict AQI
#         aqi = predict_aqi(pm10, no2, so2, co, o3)
        
#         # Determine AQI level and color
#         if aqi <= 50:
#             level = "Good"
#             color = "success"
#         elif aqi <= 100:
#             level = "Moderate"
#             color = "warning"
#         elif aqi <= 150:
#             level = "Bad"
#             color = "danger"
#         else:
#             level = "Extreme"
#             color = "dark"
        
#         return f"{aqi}", level, color
#     return "", "", ""


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
