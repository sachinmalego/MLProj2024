from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Define AQI Prediction Layout with Cards
prediction_layout = html.Div(
    [
        html.H2("AQI Prediction", className="text-center mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Card for Pollutants and Air Quality Indicators
                        dbc.Card(
                            [
                                dbc.CardHeader("Pollutants and Air Quality Indicators"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="pm25", placeholder="PM2.5", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="pm10", placeholder="PM10", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width = 4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="co", placeholder="CO", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width = 4),
                                        ]),

                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="o3", placeholder="O3", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width=4),
                                            dbc.Col([dbc.Input(type="number", id="no2", placeholder="NO2", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width=4),
                                            dbc.Col([dbc.Input(type="number", id="so2", placeholder="SO2", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width=4),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Lagged Air Quality Data
                        dbc.Card(
                            [
                                dbc.CardHeader("Lagged Air Quality Data"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([dbc.Input(type="number", id="y_lag_1", placeholder="Y Lag 1", className="mb-2", style={"width": "100%"}),
                                            ], width = 4),
                                            dbc.Col([dbc.Input(type="number", id="y_lag_2", placeholder="Y Lag 2", className="mb-2", style={"width": "100%"}),
                                            ], width = 4),
                                            dbc.Col([dbc.Input(type="number", id="y_lag_3", placeholder="Y Lag 3", className="mb-2", style={"width": "100%"}),
                                            ], width = 4),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="y_lag_4", placeholder="Y Lag 4", className="mb-2", style={"width": "100%"}),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="y_lag_5", placeholder="Y Lag 5", className="mb-2", style={"width": "100%"}),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="y_lag_6", placeholder="Y Lag 6", className="mb-2", style={"width": "100%"}),
                                            ], width=4),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="y_lag_7", placeholder="Y Lag 7", className="mb-2", style={"width": "100%"}),
                                            ], width=4),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Temporal Information
                        dbc.Card(
                            [
                                dbc.CardHeader("Temporal Information"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="year", placeholder="Year", className="mb-2", style={"width": "100%"}, value = 2018, required = True, min = 2017, max = 2023),
                                            ], width = 6),
                                            dbc.Col([
                                                dbc.Input(type="number", id="month", placeholder="Month", className="mb-2", style={"width": "100%"}, value = 1, required = True, min = 1, max = 12),
                                            ], width = 6),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="day", placeholder="Day", className="mb-2", style={"width": "100%"}, value = 1, required = True, min = 1, max = 31),
                                            ], width=6),
                                            dbc.Col([
                                                dbc.Input(type="number", id="wom", placeholder="Week of Month", className="mb-2", style={"width": "100%"}, value = 1, required = True, min = 1, max = 5),
                                            ], width=6),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Location Information
                        dbc.Card(
                            [
                                dbc.CardHeader("Location Information"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="text", id="location", placeholder="Location", className="mb-2", style={"width": "100%"}),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="latitude", placeholder="Latitude", className="mb-2", style={"width": "100%"}),
                                            ], width = 4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="longitude", placeholder="Longitude", className="mb-2", style={"width": "100%"}),
                                            ], width = 4),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Traffic-Related Variables
                        dbc.Card(
                            [
                                dbc.CardHeader("Traffic-Related Variables"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="r_distance", placeholder="Road Distance", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width = 4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="distance_traffic", placeholder="Distance to Traffic Source", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width = 4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="r_count", placeholder="Road Count", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width = 4),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="volume", placeholder="Traffic Volume", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width = 4),
                                            dbc.Col([
                                                dbc.Input(type="number", id="r_vol", placeholder="Road Volume", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),
                                            ], width = 4),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Event-Based Data
                        dbc.Card(
                            [
                                dbc.CardHeader("Event-Based Data"),
                                dbc.CardBody([dbc.Input(type="number", id="event_count", placeholder="Event Count", className="mb-2", style={"width": "100%"}, value = 0, required = True, min = 0),]),
                            ],
                            className="mb-4",
                        ),
                        # Card for Weather Variables
                        dbc.Card(
                            [
                                dbc.CardHeader("Weather Variables"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="temp_avg", placeholder="Average Temperature", className="mb-2", style={"width": "100%"}),
                                            ], width=6),
                                            dbc.Col([
                                                dbc.Input(type="number", id="w_wind_speed", placeholder="Wind Speed", className="mb-2", style={"width": "100%"}),
                                            ], width=6),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Industrial and Energy Factors
                        dbc.Card(
                            [
                                dbc.CardHeader("Industrial and Energy Factors"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(type="number", id="energy_consumption", placeholder="Energy Consumption", className="mb-2", style={"width": "100%"}),
                                            ], width=6),
                                            dbc.Col([
                                                dbc.Input(type="number", id="industrial_prodution", placeholder="Industrial Production", className="mb-2", style={"width": "100%"}),
                                            ], width=6),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                    width=12,
                    style={"maxWidth": "900px", "margin": "auto"},
                ),
            ],
            justify="center",
        ),
        dbc.Row(
            dbc.Col(
                dbc.ButtonGroup(
                    [
                        dbc.Button("Predict", id="predict-button", color="primary", className="me-2"),
                        dbc.Button("Clear", id="clear-button", color="secondary"),
                    ],
                    className="d-flex justify-content-center mt-4",
                ),
                width=12,
                style={"maxWidth": "900px", "margin": "auto"},
            ),
            justify="center",
        ),

        # The Div that will hold the gauge figure
        html.Div(
            id="result-section",  # This div will be updated with the output
            children=[
                html.Div(
                    id="aqi-output",  # This will display the AQI number
                    className="text-center mt-4",
                ),
                html.Div(
                    id="aqi-badge",  # This will display the AQI level with color
                    className="text-center mt-2",
                ),
                html.Div(
                    dcc.Graph(id="aqi-gauge"),  # This will display the gauge plot
                    className="mt-4",
                ),
            ],
            style={"display": "none"},  # Initially hidden
        ),
    ]
)

# Define AQI Prediction Logic (Stub function for demonstration)
def predict_aqi(pm10, no2, so2, co, o3):
    # Basic formula for demonstration purposes
    aqi = pm10 * 0.5 + no2 * 0.3 + so2 * 0.1 + co * 0.05 + o3 * 0.05
    return round(aqi)

# Callback for predicting AQI, updating badge, updating gauge plot, and toggling visibility
@callback(
    [
        Output("aqi-output", "children"),
        Output("aqi-badge", "children"),
        Output("aqi-badge", "color"),
        Output("aqi-gauge", "figure"),
        Output("result-section", "style"),
        Output("pm10", "value"),
        Output("no2", "value"),
        Output("so2", "value"),
        Output("co", "value"),
        Output("o3", "value")
    ],
    [Input("predict-button", "n_clicks"), Input("clear-button", "n_clicks")],
    [State("pm10", "value"), State("no2", "value"), State("so2", "value"), State("co", "value"), State("o3", "value")]
)
def update_prediction(predict_clicks, clear_clicks, pm10, no2, so2, co, o3):
    # Treat None as 0 for predict_clicks and clear_clicks
    predict_clicks = predict_clicks or 0
    clear_clicks = clear_clicks or 0
    
    # Check if clear button was clicked
    if clear_clicks > 0:
        # Clear inputs and hide the prediction section
        return "", "", "", go.Figure(), {"display": "none"}, "", "", "", "", ""
    
    # Check if predict button was clicked and all inputs are filled
    if predict_clicks > 0:
        # If any of the fields are empty, prevent prediction
        if not all([pm10, no2, so2, co, o3]):
            return "", "", "", go.Figure(), {"display": "none"}, pm10, no2, so2, co, o3
        
        # Predict AQI
        aqi = predict_aqi(pm10, no2, so2, co, o3)
        
        # Determine AQI level and color
        if aqi <= 50:
            level = "Good"
            color = "success"
        elif aqi <= 100:
            level = "Moderate"
            color = "warning"
        elif aqi <= 150:
            level = "Bad"
            color = "danger"
        else:
            level = "Extreme"
            color = "dark"
        
        # Create the gauge plot
        gauge_figure = go.Figure(go.Indicator(
            mode="gauge+number",
            value=aqi,
            title={'text': "AQI Level"},
            gauge={
                'axis': {'range': [0, 200]},
                'steps': [
                    {'range': [0, 50], 'color': 'green'},
                    {'range': [51, 100], 'color': 'yellow'},
                    {'range': [101, 150], 'color': 'orange'},
                    {'range': [151, 200], 'color': 'red'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': aqi
                }
            }
        ))

        # Show the prediction section
        return f"{aqi}", level, color, gauge_figure, {"display": "block"}, pm10, no2, so2, co, o3
    
    # Default case when no button clicked or inputs are incomplete
    return "", "", "", go.Figure(), {"display": "none"}, pm10, no2, so2, co, o3


# pm25, co, pm10, y_lag_1, y_lag_2, y_lag_3, y_lag_4, year, y_lag_5, location, latitude, longitude, y_lag_6, month, y_lag_7, day
# r_distance, event_count, r_count, o3, wom, distance_traffic, volume, no2, r_vol, so2, energy_consumption, industrial_prodution, 
# w_wind_speed, temp_avg