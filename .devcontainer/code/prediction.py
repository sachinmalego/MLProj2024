from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pickle

# import xgb model
model = pickle.load(open("Random Forest_classifier.pkl", "rb"))

#import scaler
scaler = pickle.load(open("scaler.pkl", "rb"))

# Define AQI Prediction Layout with Cards
prediction_layout = html.Div(
    [
        html.H2("AQI Prediction", className="text-center mb-4"),
        dbc.Row(
            [
                # Left Column: Form
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
                                                dbc.Label("PM2.5", html_for="pm25"),
                                                dbc.Input(type="number", id="pm25", placeholder="PM2.5", className="mb-2", style={"width": "100%"}, required=True, min=0),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Label("PM10", html_for="pm10"),
                                                dbc.Input(type="number", id="pm10", placeholder="PM10", className="mb-2", style={"width": "100%"}, required=True, min=0),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Label("CO", html_for="co"),
                                                dbc.Input(type="number", id="co", placeholder="CO", className="mb-2", style={"width": "100%"}, required=True, min=0),
                                            ], width=4),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("O3", html_for="o3"),
                                                dbc.Input(type="number", id="o3", placeholder="O3", className="mb-2", style={"width": "100%"}, required=True, min=0),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Label("NO2", html_for="no2"),
                                                dbc.Input(type="number", id="no2", placeholder="NO2", className="mb-2", style={"width": "100%"}, required=True, min=0),
                                            ], width=4),
                                            dbc.Col([
                                                dbc.Label("SO2", html_for="so2"),
                                                dbc.Input(type="number", id="so2", placeholder="SO2", className="mb-2", style={"width": "100%"}, required=True, min=0),
                                            ], width=4),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Temperature and Rainfall
                        dbc.Card(
                            [
                                dbc.CardHeader("Temperature and Rainfall"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Temperature", html_for="temperature"),
                                                dbc.Input(type="number", id="temperature", placeholder="In °C", className="mb-2", style={"width": "100%"}),
                                            ], width=6),
                                            dbc.Col([
                                                dbc.Label("Rainfall", html_for="rainfall"),
                                                dbc.Input(type="number", id="rainfall", placeholder="In mm", className="mb-2", style={"width": "100%"}),
                                            ], width=6),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Card for Traffic and Industry
                        dbc.Card(
                            [
                                dbc.CardHeader("Traffic And Industrial Data"),
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Traffic Type", html_for="traffic"),
                                                dbc.Select(
                                                    id="traffic",
                                                    options=[
                                                        {"label": 'Traffic Closure/Diversion', "value": 1},
                                                        {"label": 'Accident/Car Fire', "value": 2},
                                                        {"label": 'Traffic Jam', "value": 3},
                                                        {"label": 'Slow Traffic', "value": 4},
                                                        {"label": 'Heavy Traffic', "value": 5},
                                                    ],
                                                    value=1,
                                                    className="mb-2",
                                                    style={"width": "100%"},
                                                ),
                                            ], width=6),
                                            dbc.Col([
                                                dbc.Label("Industrial Production", html_for="industry"),
                                                dbc.Input(
                                                    type="number",
                                                    id="industry",
                                                    placeholder="Industry",
                                                    className="mb-2",
                                                    style={"width": "100%"},
                                                    required=True,
                                                    min=1,
                                                ),
                                            ], width=6),
                                        ]),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        dbc.ButtonGroup(
                            [
                                dbc.Button("Predict", id="predict-button", color="primary", className="me-2"),
                                # dbc.Button("Clear", id="clear-button", color="secondary"),
                            ],
                            className="d-flex justify-content-center mt-4",
                        ),
                    ],
                    width=6,  # Adjust column width as needed
                ),
                # Right Column: Result Section
                dbc.Col(
                    html.Div(
                        id="result-section",  # This div will be updated with the output
                        children=[
                            # html.Div(
                            #     id="aqi-output",  # This will display the AQI number
                            #     className="text-center mt-4",
                            # ),
                            # html.Div(
                            #     id="aqi-badge",  # This will display the AQI level with color
                            #     className="text-center mt-2",
                            # ),
                            html.Div(
                                dcc.Graph(id="aqi-gauge"),  # This will display the gauge plot
                                className="mt-4",
                            ),
                        ],
                        style={"display": "none"},  # Initially hidden
                    ),
                    width=6,  # Adjust column width as needed
                    style={"borderLeft": "1px solid #ddd", "paddingLeft": "15px"},
                ),
            ],
            className="g-4",  # Adjusts the gutter (spacing) between columns
        ),
    ]
)

def predict_aqi(pm25, pm10, no2, so2, co, o3, temperature, rainfall, traffic, industry):
    # Scale the input features
    features = scaler.transform([[pm25, pm10, o3, no2, so2, co, temperature, rainfall, industry]])
    
    # Predict AQI using the model
    aqi = model.predict(features)[0]

    print("upper aqi", model.predict(features))

    # aqi possible values: 0, 1, 2, 3, 4
    return round(aqi)

# Define the callback function
@callback(
    [
        Output("result-section", "style"),  # Show the result section
        Output("aqi-gauge", "figure"),  # Update the gauge chart
    ],
    [
        Input("predict-button", "n_clicks"),  # Trigger prediction only on button click
    ],
    [
        State("pm25", "value"),
        State("pm10", "value"),
        State("co", "value"),
        State("o3", "value"),
        State("no2", "value"),
        State("so2", "value"),
        State("temperature", "value"),
        State("rainfall", "value"),
        State("traffic", "value"),
        State("industry", "value"),
    ],
)
def update_aqi(n_clicks, pm25, pm10, co, o3, no2, so2, temperature, rainfall, traffic, industry):
    # Check if the predict button was clicked
    if n_clicks is None:
        return {"display": "none"}, {}

    # Ensure that all inputs are valid (i.e., not None or empty)
    try:
        pm25 = float(pm25)
        pm10 = float(pm10)
        no2 = float(no2)
        so2 = float(so2)
        co = float(co)
        o3 = float(o3)
        temperature = float(temperature)
        rainfall = float(rainfall)
        traffic = int(traffic)
        industry = int(industry)
    except ValueError:
        # Return empty result if inputs are invalid
        return {"display": "none"}, {}
    except TypeError:
        # Return empty result if inputs are invalid
        return {"display": "none"}, {}
    
    print("pm25", pm25)
    print("pm10", pm10)
    print("no2", no2)
    print("so2", so2)
    print("co", co)
    print("o3", o3)
    print("temperature", temperature)
    print("rainfall", rainfall)
    print("traffic", traffic)
    print("industry", industry)

    # Call the prediction function
    aqi = predict_aqi(pm25, pm10, no2, so2, co, o3, temperature, rainfall, traffic, industry)

    print("aqi", aqi)

    # Define custom tick labels
    tick_values = [0, 1, 2, 3, 4, 5]  # Normalized scale
    tick_texts = ["0", "25", "50", "100", "200", "200+"]  # Custom labels

    # Define AQI category based on value
    if aqi == 0:
        aqi_category = "Very Good"
    elif aqi == 1:
        aqi_category = "Good"
    elif aqi == 2:
        aqi_category = "Moderate"
    elif aqi == 3:
        aqi_category = "Beginning to have health effects"
    elif aqi == 4:
        aqi_category = "Impact on health"


    # Create the gauge chart for AQI
    fig = go.Figure(go.Indicator(
        mode="gauge", # "gauge+number+delta" if want to show number as well
        value=aqi,
        title={"text": "Air Quality Index (AQI)"},
        gauge={
            "axis": {
                "range": [None, 5],
                "tickvals": tick_values,
                "ticktext": tick_texts,
                "tickwidth": 1,
            },
            "bar": {"color": "black"},
            "steps": [
                {"range": [0, 1], "color": "blue"},
                {"range": [1, 2], "color": "green"},
                {"range": [2, 3], "color": "yellow"},
                {"range": [3, 4], "color": "orange"},
                {"range": [4, 5], "color": "red"},
            ],
        },
    ))

        # Add text annotation in the center
    fig.add_annotation(
        text=aqi_category,  # Display the AQI category
        x=0.5, y=0.2,  # Center position of the gauge
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=20, color="black")
    )

    # Return the updated result section and the gauge chart
    return {"display": "block"}, fig
