from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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
        
        dbc.Row([
            dbc.Col(dbc.Button("Predict", id="predict-button", color="primary", n_clicks=0), width=2),
            dbc.Col(dbc.Button("Clear", id="clear-button", color="secondary", n_clicks=0), width=2)
        ])
    ]),

    html.Hr(),

    # Prediction div, initially hidden
    html.Div(id="result-section", children=[
        html.H4("Predicted AQI:", className="mt-3"),
        html.Div(id="aqi-output", style={"font-size": "2rem", "font-weight": "bold"}),
        dbc.Badge(id="aqi-badge", pill=True, style={"font-size": "1.2rem", "padding": "0.5rem 1rem"}),
        dcc.Graph(id="aqi-gauge")
    ], className="mt-4", style={"display": "none"})  # Hide initially
])

# Define AQI Prediction Logic (Stub function for demonstration)
def predict_aqi(pm10, no2, so2, co, o3):
    # Basic formula for demonstration purposes
    aqi = pm10 * 0.5 + no2 * 0.3 + so2 * 0.1 + co * 0.05 + o3 * 0.05
    return round(aqi)

# Callback for predicting AQI, updating badge, updating gauge plot, and toggling visibility
@callback(
    [Output("aqi-output", "children"),
     Output("aqi-badge", "children"),
     Output("aqi-badge", "color"),
     Output("aqi-gauge", "figure"),
     Output("result-section", "style")],
    [Input("predict-button", "n_clicks"), Input("clear-button", "n_clicks")],
    [State("pm10", "value"), State("no2", "value"), State("so2", "value"), State("co", "value"), State("o3", "value")]
)
def update_prediction(predict_clicks, clear_clicks, pm10, no2, so2, co, o3):
    # Check if clear button was clicked
    if clear_clicks > 0:
        # Clear inputs and hide the prediction section
        return "", "", "", go.Figure(), {"display": "none"}
    
    # Check if predict button was clicked and all inputs are filled
    if predict_clicks > 0 and all([pm10, no2, so2, co, o3]):
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
        return f"{aqi}", level, color, gauge_figure, {"display": "block"}
    
    # Default case when no button clicked or inputs are incomplete
    return "", "", "", go.Figure(), {"display": "none"}
