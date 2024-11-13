from dash import html

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


