import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("../../data/processed/air/air_quality.csv")

# Preprocess the data
# Ensure the date column is parsed correctly
df["date"] = pd.to_datetime(df["date"])
# Handle missing values if needed
df.fillna(0, inplace=True)

# Create the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Monthly Averages of Air Quality Features"),
    html.Label("Select Location:"),
    dcc.Dropdown(
        id="location-dropdown",
        options=[{"label": loc, "value": loc} for loc in df["location"].unique()],
        value=df["location"].unique()[0],
        clearable=False
    ),
    html.Label("Select Year:"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": str(year), "value": year} for year in df["year"].unique()],
        value=df["year"].unique()[0],
        clearable=False
    ),
    html.Label("Select Feature:"),
    dcc.Dropdown(
        id="feature-dropdown",
        options=[{"label": feature, "value": feature} for feature in ["pm25", "pm10", "o3", "no2", "so2", "co"]],
        value="pm25",
        clearable=False
    ),
    dcc.Graph(id="line-plot")
])

# Callback to update the graph
@app.callback(
    Output("line-plot", "figure"),
    [Input("location-dropdown", "value"),
     Input("year-dropdown", "value"),
     Input("feature-dropdown", "value")]
)
def update_line_plot(selected_location, selected_year, selected_feature):
    # Filter the data based on user selection
    filtered_df = df[
        (df["location"] == selected_location) &
        (df["year"] == selected_year)
    ]
    
    # Group by month and calculate the average for the selected feature
    monthly_avg = (
        filtered_df.groupby("month")[selected_feature]
        .mean()
        .reset_index()
        .sort_values("month")
    )
    
    # Map month numbers to names for better readability
    month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
                   7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
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

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
