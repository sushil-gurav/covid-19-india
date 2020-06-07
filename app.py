import dash
from dash.dependencies import Input, Output
import plotly.io as pio
from home import *
from insights import *
import home
import insights

pio.templates['plotly'].layout['paper_bgcolor'] = '#F9F9F9'
pio.templates['plotly'].layout['plot_bgcolor'] = '#F9F9F9'
pio.templates['plotly'].layout['geo'].bgcolor = '#F9F9F9'

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
# server.secret_key = os.environ.get('secret_key', 'secret')
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# App callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    elif pathname == '/insights':
        return insights.layout
    else:
        return home.layout


# Home Callbacks
@app.callback(
    Output(component_id='map-country', component_property='figure'),
    [Input(component_id='status-map-country', component_property='value')]
)
def update_country_map(value):
    return create_country_map(status=value)


@app.callback(
    Output(component_id='status-daily-country', component_property='style'),
    [Input(component_id='total-daily-country', component_property='value')]
)
def update_country_chart_radio(value):
    if value == 'Daily':
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='chart-country', component_property='figure'),
    [Input(component_id='total-daily-country', component_property='value'),
     Input(component_id='status-daily-country', component_property='value')]
)
def update_country_chart(country_total_daily, country_daily_status):
    return create_country_chart(chart_type=country_total_daily, bar_type=country_daily_status)


@app.callback(
    Output(component_id='state', component_property='children'),
    [Input(component_id='map-country', component_property='clickData')]
)
def update_state_name(clicked_state):
    if clicked_state is not None:
        return clicked_state['points'][0]['location']
    else:
        return 'Maharashtra'


@app.callback(
    Output(component_id='active-indicator-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData')]
)
def update_state_active_count(clicked_state):
    if clicked_state is not None:
        return create_count_indicator(clicked_state['points'][0]['location'], status='Total Active')
    else:
        return create_count_indicator(state='Maharashtra', status='Total Active')


@app.callback(
    Output(component_id='confirmed-indicator-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData')]
)
def update_state_confirmed_count(clicked_state):
    if clicked_state is not None:
        return create_count_indicator(clicked_state['points'][0]['location'], status='Total Confirmed')
    else:
        return create_count_indicator(state='Maharashtra', status='Total Confirmed')


@app.callback(
    Output(component_id='deceased-indicator-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData')]
)
def update_state_deceased_count(clicked_state):
    if clicked_state is not None:
        return create_count_indicator(clicked_state['points'][0]['location'], status='Total Deceased')
    else:
        return create_count_indicator(state='Maharashtra', status='Total Deceased')


@app.callback(
    Output(component_id='recovered-indicator-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData')]
)
def update_state_recovered_count(clicked_state):
    if clicked_state is not None:
        return create_count_indicator(clicked_state['points'][0]['location'], status='Total Recovered')
    else:
        return create_count_indicator(state='Maharashtra', status='Total Recovered')


@app.callback(
    Output(component_id='tests-indicator-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData')]
)
def update_state_tests_count(clicked_state):
    if clicked_state is not None:
        return create_test_count_indicator(clicked_state['points'][0]['location'], status='Total Tested')
    else:
        return create_test_count_indicator(state='Maharashtra', status='Total Tested')


@app.callback(
    Output(component_id='map-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData'),
     Input(component_id='status-map-state', component_property='value')
     ]
)
def update_state_map(clicked_state, status):
    if clicked_state is not None:
        return create_state_map(clicked_state['points'][0]['location'], status=status)
    else:
        return create_state_map(state='Maharashtra', status=status)


@app.callback(
    Output(component_id='chart-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData'),
     Input(component_id='total-daily-state', component_property='value'),
     Input(component_id='status-daily-state', component_property='value')]
)
def update_state_chart(clicked_state, state_total_daily, state_daily_status):
    if clicked_state is not None:
        return create_state_chart(state_name=clicked_state['points'][0]['location'], chart_type=state_total_daily,
                                  bar_type=state_daily_status)
    else:
        return create_state_chart(state_name='Maharashtra', chart_type=state_total_daily, bar_type=state_daily_status)


@app.callback(
    Output(component_id='status-daily-state', component_property='style'),
    [Input(component_id='total-daily-state', component_property='value')]
)
def update_state_chart_radio(value):
    if value == 'Daily':
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


# Insights callbacks
@app.callback(
    Output(component_id='status-total-test', component_property='style'),
    [Input(component_id='total-daily-test', component_property='value')]
)
def update_test_chart_radio(value):
    if value == 'Total':
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='test-chart', component_property='figure'),
    [Input(component_id='state-dropdown', component_property='value'),
     Input(component_id='total-daily-test', component_property='value'),
     Input(component_id='status-total-test', component_property='value')]
)
def update_test_chart(state, chart_type, line_type):
    return create_test_chart(state=state, chart_type=chart_type, line_type=line_type)


@app.callback(
    Output(component_id='doubling-rate-chart', component_property='figure'),
    [Input(component_id='state-dropdown', component_property='value')]
)
def update_doubling_rate_chart(state):
    return create_doubling_rate_chart(state=state)


@app.callback(
    Output(component_id='cdgr-chart', component_property='figure'),
    [Input(component_id='state-dropdown', component_property='value')]
)
def update_cdgr_chart(state):
    return create_cdgr_chart(state=state)


@app.callback(
    Output(component_id='gauge-chart', component_property='figure'),
    [Input(component_id='state-dropdown', component_property='value')]
)
def update_animated_gauge_chart(state):
    return create_animated_gauge_chart(state=state)


if __name__ == '__main__':
    app.run_server()
