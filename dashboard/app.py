"""
This script is the main runner script to pull in the various scripts together
"""
# app.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from styles import SIDEBAR_STYLE, CONTENT_STYLE, COLORS
import pages.home as home
import pages.details as details
import pages.results as results
import pages.faq as faq

# Application factory
def create_app():
    app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    server = app.server  # for gunicorn

    # Sidebar navigation
    sidebar = html.Div([
        html.H2("📊 Dash Demo", className="display-6", style={"color": COLORS['primary']}),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink("🏠 Home", href='/', active='exact'),
            dbc.NavLink("📋 Details", href='/details', active='exact'),
            dbc.NavLink("📈 Results", href='/results', active='exact'),
            dbc.NavLink("❓ FAQ", href='/faq', active='exact'),
        ], vertical=True, pills=True),
    ], style=SIDEBAR_STYLE)

    # App layout with router
    app.layout = html.Div([
        dcc.Location(id='url'),
        dbc.Row([
            dbc.Col(sidebar, width=2),
            dbc.Col(html.Div(id='page-content', style=CONTENT_STYLE), width=10),
        ])
    ])

    # Router callback
    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/details':
            return details.layout
        elif pathname == '/results':
            return results.layout
        elif pathname == '/faq':
            return faq.layout
        return home.layout

    # Register page callbacks
    details.register_callbacks(app)
    results.register_callbacks(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)