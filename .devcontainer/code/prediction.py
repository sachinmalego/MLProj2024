from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Define AQI Prediction Layout
prediction_layout = html.Div([
    html.H2("AQI Prediction"),
    
    dbc.Form([
        dbc.Row([
            dbc.Col(dbc.Input(type="number", id="pm10", placeholder="PM10"), width=4),
            dbc.Col(dbc.Input(type="number", id="no2", placeholder="NO2"), width=4),
            dbc.Col(dbc.Input(type="number", id="so2", placeholder="SO2"), width=4),
        ], className="mb-2"),
        
        dbc.Row([
            dbc.Col(dbc.Input(type="number", id="co", placeholder="CO"), width=4),
            dbc.Col(dbc.Input(type="number", id="o3", placeholder="O3"), width=4),
        ], className="mb-3"),
        
        dbc.Button("Predict", id="predict-button", color="primary", n_clicks=0),
    ]),

    html.Hr(),
    
    html.Div(id="result-section", children=[
        html.H4("Predicted AQI:", className="mt-3"),
        html.Div(id="aqi-output", style={"font-size": "2rem", "font-weight": "bold"}),
        dbc.Badge(id="aqi-badge", pill=True, style={"font-size": "1.2rem", "padding": "0.5rem 1rem"}),
    ], className="mt-4")
])

# Define AQI Prediction Logic (Stub function for demonstration)
def predict_aqi(pm10, no2, so2, co, o3):
    # Basic formula for demonstration purposes
    aqi = pm10 * 0.5 + no2 * 0.3 + so2 * 0.1 + co * 0.05 + o3 * 0.05
    return round(aqi)

# Callback for predicting AQI and updating badge based on AQI levels
@callback(
    [Output("aqi-output", "children"), Output("aqi-badge", "children"), Output("aqi-badge", "color")],
    [Input("predict-button", "n_clicks")],
    [State("pm10", "value"), State("no2", "value"), State("so2", "value"), State("co", "value"), State("o3", "value")]
)
def update_prediction(n_clicks, pm10, no2, so2, co, o3):
    if n_clicks > 0 and all([pm10, no2, so2, co, o3]):
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
        
        return f"{aqi}", level, color
    return "", "", ""
