import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('UMH'),
        ], className='logo'),
        html.Div([
            dcc.Link('Dashboard', href='#'),
            dcc.Link('Content', href='#'),
            dcc.Link('Analytics', href='#'),
            dcc.Link('Comments', href='#'),
            dcc.Link('Subtitles', href='#'),
            dcc.Link('Copyright', href='#'),
            dcc.Link('Earn', href='#'),
            dcc.Link('Customization', href='#'),
            dcc.Link('Logout', href='#'),
        ], className='menu-item'),
    ], className='sidebar'),
    html.Div([
        # content goes here
    ], className='main-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)