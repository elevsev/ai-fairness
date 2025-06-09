# from dash import html, dcc, Input, Output, State, dash_table
# import plotly.express as px
# import dash_bootstrap_components as dbc
# from data import sample_df, available_metrics

# layout = html.Div([
#     html.H2("Guardrail Results"),
#     dbc.Button("Toggle Results Table 📈", id="toggle-table", className="mb-2", color="info"),
#     dbc.Collapse(
#         dash_table.DataTable(
#             id="interactive-table",
#             data=sample_df.to_dict("records"),
#             columns=[{"name": i, "id": i} for i in sample_df.columns],
#             sort_action="native",
#             sort_mode="multi",
#             style_table={"overflowX": "auto"},
#             style_cell={"textAlign": "center"}
#         ),
#         id="collapse-table",
#         is_open=False
#     ),
#     html.Br(),
#     dcc.Dropdown(
#         id="bar-metric-selector",
#         options=[{"label": m, "value": m} for m in available_metrics],
#         placeholder="Select a metric to filter (leave empty for all)",
#         style={"width": "40%", "marginBottom": "1rem"}
#     ),
#     dbc.Button("Toggle Results Chart 📊", id="toggle-graph", className="mb-2", color="success"),
#     dbc.Collapse(
#         html.Div(id="results-graphs-container"),
#         id="collapse-graph",
#         is_open=True
#     ),
# ])

# def register_callbacks(app):
#     @app.callback(
#         Output("collapse-table", "is_open"),
#         Input("toggle-table", "n_clicks"),
#         State("collapse-table", "is_open")
#     )
#     def toggle_table(n, is_open):
#         return not is_open if n else is_open

#     @app.callback(
#         Output("collapse-graph", "is_open"),
#         Input("toggle-graph", "n_clicks"),
#         State("collapse-graph", "is_open")
#     )
#     def toggle_graph(n, is_open):
#         return not is_open if n else is_open

#     @app.callback(
#         Output("results-graphs-container", "children"),
#         Input("bar-metric-selector", "value")
#     )
#     def update_graphs(selected_metric):
#         metrics = [selected_metric] if selected_metric else available_metrics
#         graphs = []
#         for m in metrics:
#             fig = px.bar(
#                 sample_df,
#                 x="Gaurdrail",
#                 y=m,
#                 color="Method",
#                 barmode="group",
#                 title=f"{m} by Guardrail and Method"
#             )
#             graphs.append(
#                 dcc.Graph(
#                     figure=fig,
#                     id={"type": "results-bar-graph", "index": m},
#                     style={"marginBottom": "2rem"}
#                 )
#             )
#         return graphs

from dash import html, dcc, Input, Output, State, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from data import sample_df, available_metrics

layout = html.Div([
    html.H2("🌟 Leaderboard Results"),
    dbc.Button("Toggle Results Table 📈", id="toggle-table", className="mb-2", color="info"),
    dbc.Collapse(
        dash_table.DataTable(
            id="interactive-table",
            data=sample_df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in sample_df.columns],
            sort_action="native",
            sort_mode="multi",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center"}
        ),
        id="collapse-table",
        is_open=False
    ),
    html.Br(),
    dbc.Button("Toggle Results Chart 📊", id="toggle-graph", className="mb-2", color="success"),
    dbc.Collapse(
        dbc.Card(
            dbc.CardBody([
                dcc.Dropdown(
                    id="bar-metric-selector",
                    options=[{"label": m, "value": m} for m in available_metrics],
                    placeholder="Select a metric to filter (leave empty for all)",
                    style={"width": "40%", "marginBottom": "1rem"}
                ),
                html.Div(id="results-graphs-container")
            ])
        ),
        id="collapse-graph",
        is_open=False
    ),
])

def register_callbacks(app):
    @app.callback(
        Output("collapse-table", "is_open"),
        Input("toggle-table", "n_clicks"),
        State("collapse-table", "is_open")
    )
    def toggle_table(n, is_open):
        return not is_open if n else is_open

    @app.callback(
        Output("collapse-graph", "is_open"),
        Input("toggle-graph", "n_clicks"),
        State("collapse-graph", "is_open")
    )
    def toggle_graph(n, is_open):
        return not is_open if n else is_open

    @app.callback(
        Output("results-graphs-container", "children"),
        Input("bar-metric-selector", "value")
    )
    def update_graphs(selected_metric):
        metrics = [selected_metric] if selected_metric else available_metrics
        graphs = []
        for m in metrics:
            fig = px.bar(
                sample_df,
                x="Gaurdrail",
                y=m,
                color="Method",
                barmode="group",
                title=f"{m} by Guardrail and Method"
            )
            graphs.append(
                dcc.Graph(
                    figure=fig,
                    id={"type": "results-bar-graph", "index": m},
                    style={"marginBottom": "2rem"}
                )
            )
        return graphs