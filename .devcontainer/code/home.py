from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Map months to their names
month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

# final traffic data
df_traffic = pd.read_csv("pivot_df.csv")

df_long_traffic = df_traffic.melt(
    id_vars=["location", "year", "month"], # Columns to keep
    value_vars=["1", "2", "3", "4", "5"],  # Columns to unpivot
    var_name="traffic_congestion",         # New column for traffic congestion types
    value_name="count"                     # New column for the counts
)
df_long_traffic["month_name"] = df_long_traffic["month"].map(month_names)

df_aqi = pd.read_csv("modified_aqi_data.csv")

df_aqi['year'] = pd.to_datetime(df_aqi['date'], format='%d/%m/%Y').dt.year
df_aqi['month'] = pd.to_datetime(df_aqi['date'], format='%d/%m/%Y').dt.month

home_layout = html.Div([
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
                options = [
                    {"label": "BU Rangsit Campus", "value": "Bangkok University Rangsit Campus, Pathum Thani"},
                    {"label": "NHA Bangplee", "value": "National Housing Authority Bangplee, Samut Prakan"},
                    {"label": "Ratburana Post Office", "value": "Ratburana Post Office, Bangkok"},
                    {"label": "The Bhubing Palace", "value": "The Bhubing Palace Doi Buak Ha"},
                    {"label": "Thonburi Power Station", "value": "Thonburi Power Sub-Station, Bangkok"},
                    {"label": "Bansomdej Rajabhat Univ", "value": "bansomdejchaopraya-rajabhat university, bangkok"},
                    {"label": "Chula Hospital", "value": "chulalongkorn-hospital, bangkok"},
                    {"label": "City Hall, Samut Prakan", "value": "city-hall, samut prakan"},
                    {"label": "EGAT Nonthaburi", "value": "egat, nonthaburi"},
                    {"label": "Highway District", "value": "highway-district, samut sakhon"},
                    {"label": "Nonsi Witthaya School", "value": "nonsi-witthaya school, bangkok"},
                    {"label": "Prabadang Rehab Center", "value": "prabadang-rehabiltation center, samut prakan"},
                    {"label": "Provincial Admin Office", "value": "provincial-administrative organization, samut sakhon"},
                    {"label": "Public Relations Dept", "value": "public-relations department, bangkok"},
                    {"label": "South Bangkok Power", "value": "south-bangkok power plant, samut prakan"},
                    {"label": "Sukhothai Open Univ", "value": "sukhothai-thammathirat open university, nonthaburi"}
                ],
                value="Bangkok University Rangsit Campus, Pathum Thani",
                clearable=False,
            ),
        ]),
        html.Div(style={'width': '230px'}, children=[
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(year), "value": year} for year in range(2014, 2024)],
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
])


@callback(
    Output("bar-graph", "figure"),
    [Input("station-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_graph(selected_station, selected_year):
    # Filter the data based on user selection
    filtered_df = df_long_traffic[
        (df_long_traffic["location"] == selected_station) & 
        (df_long_traffic["year"] == selected_year)
    ]
    
    # Create the bar graph
    fig = px.bar(
        filtered_df,
        x="month_name",
        y="count",
        color="traffic_congestion",
        title=f"Monthly Traffic Jams for {selected_station} in {selected_year}",
        labels={"month_name": "Month", "count": "Traffic Jams"},
        category_orders={"month_name": list(month_names.values())},
        barmode="stack",
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
    air_filtered_df = df_aqi[
        (df_aqi["location"] == selected_location) &
        (df_aqi["year"] == selected_year)
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