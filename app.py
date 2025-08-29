import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
def load_data():
    data = pd.read_csv("output/output.csv")
    data["date"] = pd.to_datetime(data["date"])
    data["sales"] = data["sales"].astype(float)
    return data

data = load_data()

# Encode region numerically for 3D axis
data["region_code"] = data["region"].astype("category").cat.codes

# 3D scatter plot 
fig = px.scatter_3d(
    data,
    x="date",
    y="region_code",
    z="sales",
    color="region",
    size="sales",
    hover_data=["region", "date", "sales"],
    title=" Pink Morsel Sales Visualisation",
    template="plotly_white"  
)

fig.update_traces(marker=dict(symbol="circle", line=dict(width=0)))
fig.update_layout(
    scene=dict(
        xaxis_title="Date",
        yaxis_title="Region",
        zaxis_title="Sales",
        bgcolor="white"  
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    title_font=dict(size=22, color="#F08080"), 
    font=dict(color="black")
)

# Dash 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Soul Foods Sales Dashboard - Pink Morsel", 
                        className="text-center mb-4",
                        style={"color": "#3a4750", "fontWeight": "bold"}), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig, style={"height": "90vh"}), width=12)
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
