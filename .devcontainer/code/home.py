from dash import html, dcc
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

# Set the map style to "open-street-map"
fig.update_layout(mapbox_style="open-street-map")

# Remove margins around the map
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

home_layout = html.Div([
    # First row div
    html.Div(
            style={
                'display': 'flex',  # Flexbox for the inner container
                'flexDirection': 'row',  # Horizontal layout
                'justifyContent': 'space-between',  # Space between items
                'height': '33vh',  # One-third of the viewport height
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
                    },
                    children=[
                        dcc.Dropdown(
                            ['NYC', 'MTL', 'SF'], 
                            'NYC', 
                            id='station-dropdown', 
                            placeholder="Select a station", 
                            clearable=False,
                            style={'width': '50%'}
                        ),
                        
                        html.Div(
                            id='station-aqi',
                            style={'width': '100%', 'height': '100%', 'margin-top': '10px'},
                            children=[
                                html.H5("Samut Prakan Air Quality Index (AQI)"), # station name
                                html.P("Real-time PM2.5, PM10 air pollution level."),
                                
                                html.Div(
                                    style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                    children=[
                                        dbc.Badge("Good", id="aqi-badge", pill=True, style={"font-size": "1.2rem", "padding": "0.5rem 1rem"}, color="success"), # AQI indicator
                                        html.H1("15"), # AQI value real time
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
                # Second Flexbox section (Right)
                html.Div(
                    style={
                        'flex': '1',  # Take up equal space
                        'backgroundColor': '#e0e0e0',  # Slightly darker gray background
                        'padding': '20px',  # Padding inside the section
                        'display': 'flex',
                        'flexDirection': 'column',
                        'boxSizing': 'border-box',  # Include padding in height calculation
                        'overflow': 'hidden',
                        # 'justifyContent': 'center',
                        # 'alignItems': 'center'
                    },
                    children=[
                        html.H5("Air Quality Map"),
                        # html.P("Content for the second section."),
                        dcc.Graph(figure=fig,
                                  style={
                'flex': '1',        # Allow it to take up remaining space
                'height': '100%',   # Adjust to container height
                'width': '100%',    # Fit within the container width
            }
                                  )
                    ]
                )
            ]
        ),

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
                    'justifyContent': 'center',
                    'alignItems': 'center'
                },
                children=[
                    html.H2("Section 1"),
                    html.P("Content for the first section.")
                ]
            ),
            
            # Second Flexbox section (Right)
            html.Div(
                style={
                    'flex': '1',  # Take up equal space
                    'backgroundColor': '#e0e0e0',  # Slightly darker gray background
                    'padding': '20px',  # Padding inside the section
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center'
                },
                children=[
                    html.H2("Section 2"),
                    html.P("Content for the second section.")
                ]
            )
        ]
    ),

    # third row div
    html.Div(
        style={
            'display': 'flex',  # Flexbox for the inner container
            'flexDirection': 'row',  # Horizontal layout
            'height': '40vh', 
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
                    'justifyContent': 'center',
                    'alignItems': 'center'
                },
                children=[
                    html.H2("Section 1"),
                    html.P("Content for the first section.")
                ]
            ),
            
            # Second Flexbox section (Right)
            html.Div(
                style={
                    'flex': '1',  # Take up equal space
                    'backgroundColor': '#e0e0e0',  # Slightly darker gray background
                    'padding': '20px',  # Padding inside the section
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center'
                },
                children=[
                    html.H2("Section 2"),
                    html.P("Content for the second section.")
                ]
            )
        ]
    ),
])


