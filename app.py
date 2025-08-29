import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
def load_data():
    data = pd.read_csv('output/output.csv')
    data['date'] = pd.to_datetime(data['date'])
    data['sales'] = data['sales'].astype(float)
    data['region'] = data['region'].astype(str)
    return data

data = load_data()
data = data.sort_values("date")  # ensure data sorted by date

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Sales Dashboard"
server = app.server

# Create line chart
fig = px.line(data, x="date", y="sales",
              title="Pink Morsel Sales Over Time",
              labels={"date": "Date", "sales": "Sales"})

# Add vertical marker for Jan 15, 2021 (price increase date)
price_increase_date = pd.Timestamp("2021-01-15")
fig.add_vline(x=price_increase_date, line_width=3, line_dash="dash", line_color='black')
fig.add_annotation(x=price_increase_date, y=data['sales'].max(),
                   text="Price Increase", showarrow=True, arrowhead=2)

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Pink Morsel Visualizer",
                        className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig, style={"height": "500px"})
        ], width=12)
    ])
], fluid=True)

# Run app
if __name__ == "__main__":
    app.run(debug=True)

