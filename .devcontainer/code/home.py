from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample data for a dummy map
data = {
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Latitude': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
    'Longitude': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Generate a dummy map using Plotly Express
fig = px.scatter_mapbox(
    df,
    lat='Latitude',
    lon='Longitude',
    hover_name='City',
    zoom=3,
    height=400
)

# Load the traffic data
df = pd.read_csv("../../data/processed/traffic/traffic_pivot.csv")

# Reshape the data to a long format for easier filtering
df_long = df.melt(
    id_vars=["station", "start_month"], 
    value_vars=[str(year) for year in range(2017, 2024)],
    var_name="year", 
    value_name="count"
)
df_long["year"] = df_long["year"].astype(int)

# Map months to their names
month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
df_long["month_name"] = df_long["start_month"].map(month_names)

# load the air quality data
df_air = pd.read_csv("../../data/processed/air/air_quality.csv")

# Ensure the date column is parsed correctly
df_air["date"] = pd.to_datetime(df_air["date"])
# Handle missing values if needed
df_air.fillna(0, inplace=True)

# Set the map style to "open-street-map"
fig.update_layout(mapbox_style="open-street-map")

# Remove margins around the map
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

home_layout = html.Div([
    # First row div
    # html.Div(
    #         style={
    #             'display': 'flex',  # Flexbox for the inner container
    #             'flexDirection': 'row',  # Horizontal layout
    #             'justifyContent': 'space-between',  # Space between items
    #             'height': '33vh',  # One-third of the viewport height
    #             'gap': '10px',     # Gap between the two sections
    #             'marginBottom': '10px'  # Margin at the bottom of the top section
    #         },
    #         children=[
    #             # First Flexbox section (Left)
    #             html.Div(
    #                 style={
    #                     'flex': '1',  # Take up equal space
    #                     'backgroundColor': '#f0f0f0',  # Light gray background
    #                     'padding': '20px',  # Padding inside the section
    #                     'display': 'flex',
    #                     'flexDirection': 'column',
    #                 },
    #                 children=[
    #                     dcc.Dropdown(
    #                         ['NYC', 'MTL', 'SF'], 
    #                         'NYC', 
    #                         id='station-dropdown', 
    #                         placeholder="Select a station", 
    #                         clearable=False,
    #                         style={'width': '50%'}
    #                     ),
                        
    #                     html.Div(
    #                         id='station-aqi',
    #                         style={'width': '100%', 'height': '100%', 'margin-top': '10px'},
    #                         children=[
    #                             html.H5("Samut Prakan Air Quality Index (AQI)"), # station name
    #                             html.P("Real-time PM2.5, PM10 air pollution level."),
                                
    #                             html.Div(
    #                                 style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
    #                                 children=[
    #                                     dbc.Badge("Good", id="aqi-badge", pill=True, style={"font-size": "1.2rem", "padding": "0.5rem 1rem"}, color="success"), # AQI indicator
    #                                     html.H1("15"), # AQI value real time
    #                                 ]
    #                             ),
    #                         ]
    #                     ),
    #                 ]
    #             ),
    #             # Second Flexbox section (Right)
    #             html.Div(
    #                 style={
    #                     'flex': '1',  # Take up equal space
    #                     'backgroundColor': '#e0e0e0',  # Slightly darker gray background
    #                     'padding': '20px',  # Padding inside the section
    #                     'display': 'flex',
    #                     'flexDirection': 'column',
    #                     'boxSizing': 'border-box',  # Include padding in height calculation
    #                     'overflow': 'hidden',
    #                     # 'justifyContent': 'center',
    #                     # 'alignItems': 'center'
    #                 },
    #                 children=[
    #                     html.H5("Air Quality Map"),
    #                     # html.P("Content for the second section."),
    #                     dcc.Graph(figure=fig,
    #                               style={
    #             'flex': '1',        # Allow it to take up remaining space
    #             'height': '100%',   # Adjust to container height
    #             'width': '100%',    # Fit within the container width
    #         }
    #                               )
    #                 ]
    #             )
    #         ]
    #     ),

    html.Div(style={
        'display': 'flex',
        'flexDirection': 'row',
        'marginBottom': '10px',
        'gap': '10px'
    }, children=[
        html.Div(style={'width': '230px'}, children=[
            html.Label("Select Station:"),
            dcc.Dropdown(
                id="station-dropdown",
                options=[{"label": station, "value": station} for station in df["station"].unique()],
                value=df["station"].unique()[0],
                clearable=False,
            ),
        ]),
        html.Div(style={'width': '230px'}, children=[
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(year), "value": year} for year in range(2017, 2024)],
                value=2017,
                clearable=False,
            ),
        ]),
    ]),

    # second row div
    html.Div(
        style={
            'display': 'flex',  # Flexbox for the inner container
            'flexDirection': 'row',  # Horizontal layout
            'height': '66vh', 
            'gap': '10px',     # Gap between the two sections
            'marginBottom': '10px'  # Margin at the bottom of the top section
        },
        children=[
            # First Flexbox section (Left)
            html.Div(
                style={
                    'flex': '1',  # Take up equal space
                    'backgroundColor': '#f0f0f0',  # Light gray background
                    'padding': '20px',  # Padding inside the section
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'space-between',
                    # 'alignItems': 'center'
                },
                children=[
                    html.H2("Historic Air Quality Graph"),
                    html.Div(style={
                        'display': 'flex',
                        'flexDirection': 'row',
                    }, children=[
                        html.Div(style={'width': '230px'}, children=[
                            html.Label("Select Feature:"),
                            dcc.Dropdown(
                                id="feature-dropdown",
                                options=[{"label": feature, "value": feature} for feature in ["pm25", "pm10", "o3", "no2", "so2", "co"]],
                                value="pm25",
                                clearable=False
                            ),
                        ]),
                    ]),
                    dcc.Graph(id="line-plot"),
                ]
            ),
            
            # Second Flexbox section (Right)
            html.Div(
                style={
                    'flex': '1',  # Take up equal space
                    'backgroundColor': '#e0e0e0',  # Slightly darker gray background
                    'padding': '20px',  # Padding inside the section
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    # 'alignItems': 'center',
                    'flexDirection': 'column',
                },
                children=[
                    html.H2("Traffic Density Graph"),
                    dcc.Graph(id="bar-graph")
                ]
            )
        ]
    ),

    # third row div
    # html.Div(
    #     style={
    #         'display': 'flex',  # Flexbox for the inner container
    #         'flexDirection': 'row',  # Horizontal layout
    #         'height': '40vh', 
    #         'gap': '10px', 
    #         'marginBottom': '10px',
    #     },
    #     children=[
    #         # First Flexbox section (Left)
    #         html.Div(
    #             style={
    #                 'flex': '1', 
    #                 'backgroundColor': '#7AB2D3', 
    #                 'padding': '20px', 
    #                 'display': 'flex',
    #                 'justifyContent': 'center',
    #                 'alignItems': 'center'
    #             },
    #             children=[
    #                 html.H2("Section 1"),
    #                 html.P("Content for the first section.")
    #             ]
    #         ),
            
    #         # Second Flexbox section (Right)
    #         html.Div(
    #             style={
    #                 'flex': '1',  # Take up equal space
    #                 'backgroundColor': '#7AB2D3',  # Slightly darker gray background
    #                 'padding': '20px',  # Padding inside the section
    #                 'display': 'flex',
    #                 'flexDirection': 'column',
    #             },
    #             children=[
    #                 html.H2("Air Quality Forecast", style={'textAlign': 'center'}),

    #                 html.Div(
    #                     style={'display': 'flex', 'flexDirection': 'row'},
    #                     children=[
    #                         # Forecast card 1
    #                         html.Div(
    #                             style={'display': 'flex',   
    #                                    'flexDirection': 'column', 
    #                                    'minHeight': '60px', 
    #                                    'minWidth': '80px', 
    #                                    'backgroundColor': '#f0f0f0', 
    #                                    'padding': '10px', 
    #                                    'margin': '5px',
    #                                    'border-radius': '5px'
    #                                    },
    #                             children=[
    #                                 html.P("Sun", style={'textAlign': 'center'}),
    #                                 html.H5("15", style={'textAlign': 'center'}),
    #                                 html.P("AQI", style={'textAlign': 'center'}),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ]
    #         )
    #     ]
    # ),
])


@callback(
    Output("bar-graph", "figure"),
    [Input("station-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_graph(selected_station, selected_year):
    # Filter the data based on user selection
    filtered_df = df_long[
        (df_long["station"] == selected_station) & 
        (df_long["year"] == selected_year)
    ]
    
    # Create the bar graph
    fig = px.bar(
        filtered_df,
        x="month_name",
        y="count",
        title=f"Monthly Traffic Jams for {selected_station} in {selected_year}",
        labels={"month_name": "Month", "count": "Traffic Jams"},
        category_orders={"month_name": list(month_names.values())}
    )
    return fig

@callback(
    Output("line-plot", "figure"),
    [Input("station-dropdown", "value"),
     Input("year-dropdown", "value"),
     Input("feature-dropdown", "value")]
)
def update_line_plot(selected_location, selected_year, selected_feature):
    # Filter the data based on user selection
    air_filtered_df = df_air[
        (df_air["location"] == selected_location) &
        (df_air["year"] == selected_year)
    ]
    
    # Group by month and calculate the average for the selected feature
    monthly_avg = (
        air_filtered_df.groupby("month")[selected_feature]
        .mean()
        .reset_index()
        .sort_values("month")
    )
    
    # Map month numbers to names for better readability
    monthly_avg["month_name"] = monthly_avg["month"].map(month_names)

    # Create the line plot
    fig = px.line(
        monthly_avg,
        x="month_name",
        y=selected_feature,
        title=f"Monthly Average of {selected_feature.upper()} for {selected_location} in {selected_year}",
        labels={"month_name": "Month", selected_feature: f"Avg {selected_feature.upper()}"},
        markers=True
    )
    fig.update_xaxes(categoryorder="array", categoryarray=list(month_names.values()))
    return fig