import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data
def load_data():
    data = pd.read_csv("output/output.csv")
    data["date"] = pd.to_datetime(data["date"])
    data["sales"] = data["sales"].astype(float)
    data["region"] = data["region"].astype(str)
    return data

data = load_data()

# Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Soul Foods Sales Dashboard"

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H1("Soul Foods Sales Dashboard",
                        className="text-center mb-4",
                        style={"color": "#3a4750", "fontWeight": "bold"}), width=12)
    ]),

    # Radio buttons
    dbc.Row([
        dbc.Col([
            html.Label("Select Region:", style={"fontWeight": "bold", "fontSize": "18px"}),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"}
                    ],
                    value="all",  # default
                    inline=True,
                    inputStyle={"margin-right": "8px", "margin-left": "12px"},
                    labelStyle={"margin-right": "20px", "fontSize": "16px"}
                )

        ], width=12)
    ]),

    # Line Chart
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-graph", style={"height": "80vh"}), width=12)
    ])
], fluid=True)


# Callback to update chart
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(region):
    # Filter data based on region
    if region == "all":
        filtered_data = data
    else:
        filtered_data = data[data["region"].str.lower() == region]

    # Create line chart
    fig = px.line(filtered_data, x="date", y="sales", color="region",
                  title="Pink Morsel Sales Over Time",
                  labels={"date": "Date", "sales": "Sales", "region": "Region"},
                  template="plotly_white")

    # Add vertical marker for Jan 15, 2021 (price increase date)
    price_increase_date = pd.Timestamp("2021-01-15")
    fig.add_vline(x=price_increase_date, line_width=2, line_dash="dash", line_color='black')
    fig.add_annotation(x=price_increase_date, y=filtered_data['sales'].max() if not filtered_data.empty else 0,
                       text="Price Increase", showarrow=True, arrowhead=2)

    fig.update_layout(
        title_font=dict(size=22, color="#F08080"),
        font=dict(size=14),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)

