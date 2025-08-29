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

app.layout = dbc.Container([
    dbc.Card([
        # Title Bar
        dbc.CardHeader(
            html.H2("Pink Morsel Visualizer",
                    className="text-center",
                    style={"fontWeight": "bold", "margin": "0"}),
            style={
                "backgroundColor": "#d3cce3",   # light purple/grey strip
                "borderTopLeftRadius": "15px",
                "borderTopRightRadius": "15px",
                "textAlign": "center"
            }
        ),

        dbc.CardBody([
            # Line Chart
            dbc.Row([
                dbc.Col(dcc.Graph(id="sales-graph", style={"height": "70vh"}), width=12)
            ]),

            # Radio buttons (center + bottom)
            dbc.Row([
                dbc.Col([
                    dcc.RadioItems(
                        id="region-filter",
                        options=[
                            {"label": "north", "value": "north"},
                            {"label": "east", "value": "east"},
                            {"label": "south", "value": "south"},
                            {"label": "west", "value": "west"},
                            {"label": "all", "value": "all"}
                        ],
                        value="all",
                        inline=True,
                        inputStyle={"margin-right": "6px", "margin-left": "10px"},
                        labelStyle={"margin-right": "15px", "fontSize": "16px"}
                    )
                ], width="auto", className="text-center")
            ], justify="center", className="mt-3")
        ])
    ],
    style={
        "backgroundColor": "white",       # plain background
        "border": "2px solid #ccc",       # simple grey border
        "borderRadius": "15px",           # rounded corners
        "padding": "10px",
        "boxShadow": "2px 4px 12px rgba(0,0,0,0.1)"
    })
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

