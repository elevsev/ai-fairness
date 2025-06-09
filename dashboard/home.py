from dash import html
import dash_bootstrap_components as dbc

# layout = html.Div([
#     html.H1("🏡 Welcome to Guardo's Gauge"),
#     html.H1(" --  "),
#     html.H2("The RGAI Guardrail Evaluation Dashboard"),
#     html.P("""
#     This evaluation methodology is designed to assess guardrails in LLMs
#     Based on standardised benchmark data and operational metrics
#     Please see our SharePoint Page for more information""")
# ])

# Home page layout
# top_layout
# Home page layout
layout = dbc.Container([
    # Highlighted Welcome Section
    dbc.Card(
        dbc.CardBody([
            html.H1("👋 Welcome to Guardo's Gauge", className="my-4"),
            html.H4("The RGAI Guardrail Evaluation Dashboard", className="my-4"),
            # Welcome bullet points
            html.Ul([
                html.Li("This evaluation methodology is designed to assess guardrails in LLMs."),
                html.Li("Based on standardised benchmark data and operational metrics."),
                html.Li("Please see our SharePoint Page for more information."),
            ], className="my-4")
        ]),
        color="#A7E2D7",
        className="mb-5 border rounded-2"
    ),

    # Guardrail Definitions Section
    html.H2("Guardrail Definitions", className="my-4"),
    dbc.Table([
        html.Thead(html.Tr([html.Th("Guardrail"), html.Th("Description")])),
        html.Tbody([
            html.Tr([
                html.Td("⚖️ Bias"),
                html.Td("Measures level of bias in an LLM's output with respect to a set of protected groups.")
            ]),
            html.Tr([
                html.Td("😵‍💫 Hallucination"),
                html.Td("Measures the level of inaccuracy from an LLM's response relative to the prompt.")
            ]),
            html.Tr([
                html.Td("🔀 Misalignment"),
                html.Td("Measures the level of brand alignment with respect to LBG's tone of voice guidance.")
            ]),
        ])
    ], bordered=True, striped=True, responsive=True, className="mb-5"),

    # Methodology and Metrics Section
    html.H2("Methodology and Metrics Explained", className="my-4"),
    html.P(
        "We use a consistent set of metrics run against the same:",
        className="mb-3"
    ),
    html.Ul([
        html.Li("prompt(s)"),
        html.Li("benchmark data (open-source, LBG inner source, or synthetically created)"),
        html.Li("number of runs/calls"),
    ], className="mb-4"),
    dbc.Table([
        html.Thead(html.Tr([
            html.Th("Metric"), html.Th("Description"), html.Th("Range"), html.Th("Interpretation of Range")
        ])),
        html.Tbody([
            html.Tr([
                html.Td("Accuracy"),
                html.Td("Correctness of the guardrail in identifying intended outcomes."),
                html.Td("[0, 1]"), html.Td("Higher is better")
            ]),
            html.Tr([
                html.Td("TPR"),
                html.Td("Proportion of true positives."),
                html.Td("[0, 1]"), html.Td("Higher is better")
            ]),
            html.Tr([
                html.Td("FPR"),
                html.Td("Proportion of false positives."),
                html.Td("[0, 1]"), html.Td("Lower is better")
            ]),
            html.Tr([
                html.Td("F1 Score"),
                html.Td("Precision + recall combined."),
                html.Td("[0, 1]"), html.Td("Higher is better")
            ]),
            html.Tr([
                html.Td("Latency (s)"),
                html.Td("Time taken to produce output."),
                html.Td("Variable"), html.Td("Lower is better")
            ]),
            html.Tr([
                html.Td("Fin. Cost (USD)"),
                html.Td("Monetary cost per run."),
                html.Td("Variable"), html.Td("Lower is better")
            ]),
            html.Tr([
                html.Td("Env. Cost (GCO2)"),
                html.Td("Greenhouse gas emissions."),
                html.Td("Variable"), html.Td("Lower is better")
            ]),
        ])
    ], bordered=True, striped=True, responsive=True)
], fluid=True)