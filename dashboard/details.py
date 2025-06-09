from dash import html, dcc, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
from data import sample_df, guardrail_info


# # Layout definition
# layout = html.Div([
#     html.H2("Metric Details"),
#     html.H5("Select Guardrail:"),
#     html.Div(
#         id="guardrail-buttons",
#         children=[
#             dbc.Button(
#                 g,
#                 id={"type": "guardrail-button", "index": g},
#                 className="me-1",
#                 color="secondary"
#             ) for g in guardrail_info
#         ]
#     ),
#     html.Div(id="guardrail-description", className="mt-3"),

#     html.Hr(),
#     dcc.Dropdown(
#         id="method-select",
#         options=[],  # Populated based on selected guardrail
#         placeholder="Select a method",
#         style={"width": "50%"}
#     ),
#     html.Div(id="metric-cards-performance", className="mt-3"),
#     html.Div(id="metric-cards-operational"),

#     html.Hr(),
#     html.H5("Compare Methods"),
#     dcc.Dropdown(
#         id="compare-guardrail",
#         options=[{"label": g, "value": g} for g in guardrail_info],
#         placeholder="Select a Guardrail"
#     ),
#     dcc.Dropdown(
#         id="compare-methods",
#         options=[{"label": m, "value": m} for m in sample_df["Method"].unique()],
#         placeholder="Select methods to compare",
#         multi=True
#     ),
#     html.Div(id="comparison-output")
# ])

# # Callback registrations

# def register_callbacks(app):
#     # Highlight selected guardrail button and update method options
#     @app.callback(
#         Output("guardrail-buttons", "children"),
#         Output("method-select", "options"),
#         Output("guardrail-description", "children"),
#         Input({"type": "guardrail-button", "index": ALL}, "n_clicks")
#     )
#     def update_guardrail_selection(n_clicks_list):
#         triggered = ctx.triggered_id
#         # Default: no selection
#         selected = triggered.get("index") if triggered and isinstance(triggered, dict) else None

#         # Rebuild buttons with appropriate coloring
#         buttons = []
#         for g in guardrail_info:
#             color = "success" if g == selected else "secondary"
#             buttons.append(
#                 dbc.Button(
#                     g,
#                     id={"type": "guardrail-button", "index": g},
#                     className="me-1",
#                     color=color
#                 )
#             )

#         # Update method options based on selected guardrail
#         if selected:
#             methods = sample_df[sample_df["Gaurdrail"] == selected]["Method"].unique()
#             options = [{"label": m, "value": m} for m in methods]
#             description = html.Div(guardrail_info.get(selected, ""))
#         else:
#             options = []
#             description = html.Div()

#         return buttons, options, description

#     # Show performance and operational cards for selected method
#     @app.callback(
#         [Output("metric-cards-performance", "children"), Output("metric-cards-operational", "children")],
#         Input("method-select", "value")
#     )
#     def show_method_cards(method):
#         if not method:
#             return "", ""
#         subset = sample_df[sample_df["Method"] == method]
#         perf_metrics = ["ACCURACY", "TPR", "FPR", "F1"]
#         op_metrics = ["LATENCY (S)", "FIN COST (USD)", "ENV COST (GCO2)"]

#         def make_cards(metrics):
#             return dbc.Row([
#                 dbc.Col(
#                     dbc.Card([
#                         dbc.CardHeader(metric),
#                         dbc.CardBody([html.H5(f"{subset.iloc[0][metric]:.3f}", className="card-title")])
#                     ], className="mb-3")
#                 ) for metric in metrics
#             ])

#         return make_cards(perf_metrics), make_cards(op_metrics)

#     # Compare selected methods for a guardrail
#     @app.callback(
#         Output("comparison-output", "children"),
#         Input("compare-guardrail", "value"), Input("compare-methods", "value")
#     )
#     def compare_methods(guardrail, methods):
#         if not guardrail or not methods:
#             return html.Div()
#         subset = sample_df[(sample_df["Gaurdrail"] == guardrail) & (sample_df["Method"].isin(methods))]
#         return dbc.Table.from_dataframe(subset, striped=True, bordered=True, hover=True)


# Layout definition
layout = html.Div([
    html.H2("Metric Details", className="my-4"),
    html.H5("Select Guardrail Below", className="my-4"),
    html.Div(
        id="guardrail-buttons",
        children=[
            dbc.Button(
                g,
                id={"type": "guardrail-button", "index": g},
                className="me-1",
                color="secondary"
            ) for g in guardrail_info
        ]
    ),
    html.Div(id="guardrail-description", className="mt-3"),

    html.Hr(),
    dcc.Dropdown(
        id="method-select",
        options=[],  # Populated based on selected guardrail
        placeholder="Select a method",
        style={"width": "50%"}
    ),
    html.Div(id="metric-cards-performance", className="mt-3"),
    html.Div(id="metric-cards-operational"),

    html.Hr(),
    html.H5("Compare Methods",className="my-4"),
    dcc.Dropdown(
        id="compare-guardrail",
        options=[{"label": g, "value": g} for g in guardrail_info],
        placeholder="Select a Guardrail",
    ),
    dcc.Dropdown(
        id="compare-methods",
        options=[{"label": m, "value": m} for m in sample_df["Method"].unique()],
        placeholder="Select methods to compare",
        multi=True
    ),
    html.Div(id="comparison-output")
])

# Callback registrations

def register_callbacks(app):
    # Highlight selected guardrail button and update method options
    @app.callback(
        Output("guardrail-buttons", "children"),
        Output("method-select", "options"),
        Output("guardrail-description", "children"),
        Input({"type": "guardrail-button", "index": ALL}, "n_clicks")
    )
    def update_guardrail_selection(n_clicks_list):
        triggered = ctx.triggered_id
        # Default: no selection
        selected = triggered.get("index") if triggered and isinstance(triggered, dict) else None

        # Rebuild buttons with appropriate coloring
        buttons = []
        for g in guardrail_info:
            color = "success" if g == selected else "secondary"
            buttons.append(
                dbc.Button(
                    g,
                    id={"type": "guardrail-button", "index": g},
                    className="me-1",
                    color=color
                )
            )

        # Update method options based on selected guardrail
        if selected:
            methods = sample_df[sample_df["Gaurdrail"] == selected]["Method"].unique()
            options = [{"label": m, "value": m} for m in methods]
            description = html.Div(guardrail_info.get(selected, ""))
        else:
            options = []
            description = html.Div()

        return buttons, options, description

    # Show performance and operational cards for selected method
    @app.callback(
        [Output("metric-cards-performance", "children"), Output("metric-cards-operational", "children")],
        Input("method-select", "value")
    )
    def show_method_cards(method):
        if not method:
            return "", ""
        subset = sample_df[sample_df["Method"] == method]
        perf_metrics = ["ACCURACY", "TPR", "FPR", "F1"]
        op_metrics = ["LATENCY (S)", "FIN COST (USD)", "ENV COST (GCO2)"]

        def make_cards(metrics):
            return dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(metric),
                        dbc.CardBody([html.H5(f"{subset.iloc[0][metric]:.3f}", className="card-title")])
                    ], className="mb-3")
                ) for metric in metrics
            ])

        return make_cards(perf_metrics), make_cards(op_metrics)

    # Compare selected methods for a guardrail
    @app.callback(
        Output("comparison-output", "children"),
        Input("compare-guardrail", "value"), Input("compare-methods", "value")
    )
    def compare_methods(guardrail, methods):
        if not guardrail or not methods:
            return html.Div()
        subset = sample_df[(sample_df["Gaurdrail"] == guardrail) & (sample_df["Method"].isin(methods))]
        return dbc.Table.from_dataframe(subset, striped=True, bordered=True, hover=True)