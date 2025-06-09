import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Sample data
sample_df = pd.DataFrame({
    "Gaurdrail": ["Bias", "Misalignment", "Hallucination", "Hallucination"],
    "Method": ["AIAssistedGuardrails", "AIAssistedGuardrails", "AIAssistedGuardrails", "CosineSimilarity"],
    "ACCURACY": [0.650966, 0.646552, 0.664679, 0.556805],
    "TPR": [0.512241, 0.719298, 0.652418, 0.391451],
    "FPR": [0.210179, 0.724123, 0.31946, 0.27784],
    "F1": [0.594861, 0.742138, 0.661723, 0.469003],
    "LATENCY (S)": [1.471627, 2.263252, 2.2027, 0.408035],
    "FIN COST (USD)": [0.000653, 0.004334, 0.00203, 0.0],
    "ENV COST (GCO2)": [0.100474, 0.85975, 0.366783, 0.0]
})

## CONSTANTS
available_metrics = [
    "ACCURACY", "TPR", "FPR", "F1", "LATENCY (S)", "FIN COST (USD)", "ENV COST (GCO2)"
]

available_guardrails = [
    "Bias", "Misalignment", "Hallucination"
]

metric_info = {
    "ACCURACY": {"definition": "Proportion of correct predictions.", "formula": "(TP + TN) / (TP + TN + FP + FN)", "interpretation": "Higher is better."},
    "TPR": {"definition": "True Positive Rate.", "formula": "TP / (TP + FN)", "interpretation": "Higher is better."},
    "FPR": {"definition": "False Positive Rate.", "formula": "FP / (FP + TN)", "interpretation": "Lower is better."},
    "F1": {"definition": "Harmonic mean of precision and recall.", "formula": "2 * (Precision * Recall) / (Precision + Recall)", "interpretation": "Higher is better."},
    "LATENCY (S)": {"definition": "Time taken for a response.", "formula": "Seconds.", "interpretation": "Lower is better."},
    "FIN COST (USD)": {"definition": "Financial cost per query.", "formula": "US Dollars.", "interpretation": "Lower is better."},
    "ENV COST (GCO2)": {"definition": "Environmental cost.", "formula": "Grams of CO2 emitted.", "interpretation": "Lower is better."},
}

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

colors = {
    "primary": "#008080",
    "secondary": "#2e8b57",
    "accent": "#4682b4",
}

## SIDEBAR
sidebar = html.Div([
    html.H2("📊 Dash Demo", className="display-6", style={"color": colors["primary"]}),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("🏠 Home", href="/", active="exact"),
        dbc.NavLink("📋 Details", href="/details", active="exact"),
        dbc.NavLink("📈 Results", href="/results", active="exact"),
        dbc.NavLink("❓ FAQ", href="/faq", active="exact"),
    ], vertical=True, pills=True),
], style={"padding": "2rem 1rem", "background": "#f8f9fa", "height": "100vh"})

## HOME PAGE LAYOUT
home_layout = html.Div([
    html.H2("Welcome to the Dashboard"),
    html.P("Use the sidebar to navigate through the sections."),
])

## DETAILS PAGE LAYOUT 
details_layout = html.Div([
    html.H2("Metric Details"),
    dcc.Dropdown(
        id="metric-dropdown",
        options=[{"label": metric, "value": metric} for metric in available_metrics],
        placeholder="Select a metric",
        style={"width": "50%"}
    ),
    html.Div(id="metric-info-output", style={"marginTop": "2rem"}),
    html.Div(id="metric-cards-output", style={"marginTop": "2rem"})
])

## GUARDRAILS PAGE LAYOUT
results_layout = html.Div([
    html.H2("Guardrail Results"),
    dcc.Dropdown(
        id="bar-metric-selector",
        options=[{"label": m, "value": m} for m in available_metrics],
        value="F1",
        style={"width": "40%", "marginBottom": "1rem"}
    ),
    dbc.Button("See Results Table \U0001F4C8", id="toggle-table", className="mb-2", color="info"),
    dbc.Collapse([
        dash_table.DataTable(
            data=sample_df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in sample_df.columns],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "fontFamily": "Calibri"}
        )
    ], id="collapse-table", is_open=False),

    html.Br(),

    dbc.Button("See Plots \U0001F4CA", id="toggle-graph", className="mb-2", color="success"),
    dbc.Collapse([
        dcc.Graph(id="results-bar-graph")
    ], id="collapse-graph", is_open=False),
])

## FAQ LAYOUT
faq_layout = html.Div([
    html.H2("Frequently Asked Questions"),
    html.P("Here you can address common concerns and explanations."),
])

## GENERAL LAYOUT
app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(html.Div(id="page-content", style={"padding": "2rem"}), width=10),
    ])
])

## CALLBACK
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/results":
        return results_layout
    elif pathname == "/details":
        return details_layout
    elif pathname == "/faq":
        return faq_layout
    return home_layout

@app.callback(Output("collapse-table", "is_open"), Input("toggle-table", "n_clicks"), State("collapse-table", "is_open"))
def toggle_table(n, is_open):
    return not is_open if n else is_open

@app.callback(Output("collapse-graph", "is_open"), Input("toggle-graph", "n_clicks"), State("collapse-graph", "is_open"))
def toggle_graph(n, is_open):
    return not is_open if n else is_open

@app.callback(Output("results-bar-graph", "figure"), Input("bar-metric-selector", "value"))
def update_bar_chart(selected_metric):
    return px.bar(
        sample_df,
        x="Gaurdrail",
        y=selected_metric,
        color="Method",
        barmode="group",
        title=f"{selected_metric} by Guardrail and Method"
    )

@app.callback(
    [Output("metric-info-output", "children"), Output("metric-cards-output", "children")],
    Input("metric-dropdown", "value")
)

## UPDATE METRICS AND RESULTS CARDS
def update_metric_info_and_cards(selected):
    if not selected:
        return "", ""
    info = metric_info[selected]
    cards = [
        dbc.Card([
            dbc.CardHeader(f"{row['Gaurdrail']} | {row['Method']}", className="fw-bold"),
            dbc.CardBody([
                html.H5(f"{selected}: {row[selected]:.3f}", className="card-title")
            ])
        ], className="mb-3")
        for _, row in sample_df.iterrows()
    ]
    return html.Div([
        html.H4(f"Definition: {info['definition']}", style={"marginBottom": "1rem"}),
        html.H5(f"Formula: {info['formula']}", style={"marginBottom": "1rem"}),
        html.P(f"Interpretation: {info['interpretation']}")
    ]), cards

if __name__ == "__main__":
    app.run(debug=True)