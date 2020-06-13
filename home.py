import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from data import *


def create_count_indicator(state, status):
    today = df_states['DATE'][df_states.index[-1]]
    yesterday = df_states['DATE'][df_states.index[-2]]
    count_today = int(df_states[(df_states['DATE'] == today)
                                & (df_states['STATE'] == state)
                                & (df_states['STATUS'] == status)]['COUNT']
                      )
    count_yesterday = int(df_states[(df_states['DATE'] == yesterday)
                                    & (df_states['STATE'] == state)
                                    & (df_states['STATUS'] == status)]['COUNT']
                          )

    fig_count_indicator = go.Figure(go.Indicator(
        mode="number+delta",
        value=count_today,
        number={"valueformat": ",", 'font': {'size': 20}},
        delta={'reference': count_yesterday, "valueformat": ",", "position": "right"},
        # domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig_count_indicator.update_layout(autosize=False, width=150, height=50, margin=dict(l=0, r=0, b=0, t=0, pad=0),
                                      paper_bgcolor="#F9F9F9")

    return fig_count_indicator


def create_test_count_indicator(state, status):
    if state == 'Total':
        df_state_test_fig = df_state_test.groupby('Updated On').sum().reset_index()
    else:
        df_state_test_fig = df_state_test[df_state_test['State'] == state].fillna(method='ffill').fillna(
            0).reset_index()

    today = df_state_test_fig['Updated On'][df_state_test_fig.index[-1]]
    yesterday = df_state_test_fig['Updated On'][df_state_test_fig.index[-2]]
    count_today = int(df_state_test_fig[df_state_test_fig['Updated On'] == today][status])
    count_yesterday = int(df_state_test_fig[df_state_test_fig['Updated On'] == yesterday][status])

    fig_test_count_indicator = go.Figure(go.Indicator(
        mode="number+delta",
        value=count_today,
        number={"valueformat": ",", 'font': {'size': 16}},
        delta={'reference': count_yesterday, "valueformat": ",", "position": "right"},
        # domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig_test_count_indicator.update_layout(autosize=False, width=150, height=50, margin=dict(l=0, r=0, b=0, t=0, pad=0),
                                      paper_bgcolor="#F9F9F9")

    return fig_test_count_indicator


def load_map_json(map_name):
    with open('maps/geojson/' + map_dict[map_name]) as res:
        map_json = json.load(res)

    return map_json


def create_country_map(status):
    country_json = load_map_json(map_name='India')
    today = df_states['DATE'][df_states.index[-1]]
    count = str(int(
        df_states[(df_states['DATE'] == today) & (df_states['STATE'] == 'Total') & (df_states['STATUS'] == status)][
            'COUNT']))
    df_states_fig = df_states[(df_states['STATUS'] == status) & (df_states['STATE'] != 'Total')]
    fig_country_map = px.choropleth(df_states_fig,
                                    geojson=country_json,
                                    locations='STATE',
                                    color='COUNT',
                                    color_continuous_scale=color_continuous_scale_dict[status],
                                    range_color=(df_states_fig['COUNT'].min(), df_states_fig['COUNT'].max()),
                                    locationmode='geojson-id',  # scope="asia",
                                    labels={'STATE': 'State/UT', 'COUNT': status},
                                    featureidkey='properties.st_nm',
                                    animation_frame='DATE', animation_group='STATE'
                                    )
    fig_country_map.update_geos(fitbounds="locations", visible=False)
    fig_country_map.update_layout(transition={'duration': 100},
                                  margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                  sliders=dict(pad=dict(t=0, r=25, b=0, l=25)),
                                  coloraxis=dict(showscale=False),
                                  annotations=[dict(x=0.1, y=0.95, showarrow=False,
                                                    text='India<br>' + status.split()[1] + ': ' + count,
                                                    xref="paper", yref="paper",
                                                    font=dict(size=15, color=color_discrete_map_total[status]))]
                                  )

    fig_country_map.data[0].z = df_states_fig[df_states_fig['DATE'] == today]['COUNT'].to_numpy()
    fig_country_map.data[0].hovertemplate = 'Date=' + today + '<br>State/UT=%{location}<br>' + status + '=%{z}'
    fig_country_map['layout']['sliders'][0].active = len(df_states_fig['DATE'].unique()) - 1

    return fig_country_map


def create_country_chart(chart_type, bar_type):
    df_country_chart = df_states[df_states['STATE'] == 'Total'].reset_index()
    if chart_type == 'Total':
        df_country_chart = df_country_chart[df_country_chart['STATUS'].isin(total_list)]
        fig_country_chart = px.line(df_country_chart,
                                    x='DATE',
                                    y='COUNT',
                                    log_y=False,
                                    line_shape='spline',
                                    color='STATUS',
                                    color_discrete_map=color_discrete_map_total)
        fig_country_chart.update_traces(mode='lines')
    else:
        df_country_chart = df_country_chart[df_country_chart['STATUS'] == chart_type + ' ' + bar_type]
        fig_country_chart = px.bar(df_country_chart,
                                   x='DATE',
                                   y='COUNT',
                                   log_y=False,
                                   color='STATUS',
                                   color_discrete_map=color_discrete_map_daily)

    fig_country_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                    legend=dict(orientation='h', title=dict(text='')),
                                    xaxis=dict(title=dict(text='')),
                                    yaxis=dict(title=dict(text='')),
                                    annotations=[dict(x=0.1, y=0.95, showarrow=False,
                                                      text='India',
                                                      xref="paper", yref="paper",
                                                      font=dict(size=15))]
                                    )

    return fig_country_chart


def create_state_map(state, status):
    state_json = load_map_json(map_name=state)
    state_districts = [state_json['features'][i]['properties']['district'] for i in
                       range(0, len(state_json['features']))]
    df_state_district_fig = df_state_district[(df_state_district['State'] == state)]
    df_state_district_mask = pd.DataFrame(list(product(df_state_district_fig.State.unique(), state_districts)),
                                          columns=['State', 'District'])
    df_state_district_mask = pd.concat(
        [df_state_district_mask, pd.DataFrame(
            columns=['Active', 'Confirmed', 'Deceased', 'Recovered', 'Delta Active', 'Delta Confirmed',
                     'Delta Deceased', 'delta Recovered', 'State Code', 'Notes'])])
    df_state_district_fig = df_state_district_fig.set_index(['State', 'District'])
    df_state_district_mask = df_state_district_mask.set_index(['State', 'District'])

    df_state_district_fig = df_state_district_fig.combine_first(df_state_district_mask).reset_index()
    df_state_district_fig = df_state_district_fig.fillna(0)
    count = str(int(df_state_district.groupby('State').sum().loc[state, status]))

    fig_state_map = px.choropleth(df_state_district_fig,
                                  geojson=state_json,
                                  locations='District',
                                  color=status,
                                  color_continuous_scale=color_continuous_scale_dict['Total ' + status],
                                  range_color=(
                                      df_state_district_fig[status].min(),
                                      df_state_district_fig[status].max()),
                                  locationmode='geojson-id',  # scope="asia",
                                  labels={status: 'Total ' + status},
                                  featureidkey='properties.district',
                                  )
    fig_state_map.update_geos(fitbounds="locations", visible=False)
    fig_state_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis=dict(showscale=False),
        annotations=[dict(x=0.1, y=0.95, showarrow=False, text=state + '<br>' + status + ': ' + count, xref="paper",
                          yref="paper",
                          font=dict(size=15, color=color_discrete_map_total['Total ' + status]))]
    )

    return fig_state_map


def create_state_chart(state_name, chart_type, bar_type):
    df_state_chart = df_states[df_states['STATE'] == state_name].reset_index()
    if chart_type == 'Total':
        df_state_chart = df_state_chart[df_state_chart['STATUS'].isin(total_list)]
        fig_state_chart = px.line(df_state_chart,
                                  x='DATE',
                                  y='COUNT',
                                  log_y=False,
                                  line_shape='spline',
                                  color='STATUS',
                                  color_discrete_map=color_discrete_map_total)

        fig_state_chart.update_traces(mode='lines')
    else:
        df_state_chart = df_state_chart[df_state_chart['STATUS'] == chart_type + ' ' + bar_type]
        fig_state_chart = px.bar(df_state_chart,
                                 x='DATE',
                                 y='COUNT',
                                 log_y=False,
                                 color='STATUS',
                                 color_discrete_map=color_discrete_map_daily)

    fig_state_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                  legend=dict(orientation='h', title=dict(text='')),
                                  xaxis=dict(title=dict(text='')),
                                  yaxis=dict(title=dict(text='')),
                                  annotations=[
                                      dict(x=0.1, y=0.95, showarrow=False,
                                           text=state_name,
                                           xref="paper", yref="paper",
                                           font=dict(size=15)), ]
                                  )

    return fig_state_chart


layout = html.Div(
    [
        # dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.A(
                            html.Button("Home", id="home-button",
                                        style={"background-color": "#119dff", "color": "#ffffff"}),
                            href="home",
                        ),
                        html.A(
                            html.Button("Insights", id="insights-button"),
                            href="insights",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "COVID-19 Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "India", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://github.com/sushil-gurav/covid-19-india",
                            target="_blank"
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div([html.H6('India', id='country', style={"margin-top": "0px", "margin-bottom": "0px"})],
                         className="pretty_container two columns",
                         ),
                html.Div([html.H6('Active', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='active-indicator-country',
                                    figure=create_count_indicator(state='Total', status='Total Active'))],
                         className="pretty_container two columns",
                         style={"padding": 5,
                                "border": "solid",
                                "border-color": color_discrete_map_total['Total Active']}
                         ),
                html.Div([html.H6('Confirmed', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='confirmed-indicator-country',
                                    figure=create_count_indicator(state='Total', status='Total Confirmed'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Confirmed']}
                         ),
                html.Div([html.H6('Deceased', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='deceased-indicator-country',
                                    figure=create_count_indicator(state='Total', status='Total Deceased'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Deceased']}
                         ),
                html.Div([html.H6('Recovered', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='recovered-indicator-country',
                                    figure=create_count_indicator(state='Total', status='Total Recovered'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Recovered']}
                         ),
                html.Div([html.H6('Tests', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='tests-indicator-country',
                                    figure=create_test_count_indicator(state='Total', status='Total Tested'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Tested']}
                         ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div([html.Div(
                    [dcc.RadioItems(id='status-map-country', options=[{'label': i, 'value': 'Total ' + i} for i in
                                                                      ['Active', 'Confirmed', 'Deceased',
                                                                       'Recovered']],
                                    value='Total Active', labelStyle={'display': 'inline-block'})],
                    className="radio-group"),
                    dcc.Graph(id='map-country')],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.Div([dcc.RadioItems(id='total-daily-country',
                                              options=[{'label': i, 'value': i} for i in ['Total', 'Daily']],
                                              value='Total', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     html.Div([dcc.RadioItems(id='status-daily-country',
                                              options=[{'label': i, 'value': i} for i in
                                                       ['Confirmed', 'Deceased', 'Recovered']],
                                              value='Confirmed', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     dcc.Graph(id='chart-country')
                     ],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div([html.H6('Maharashtra', id='state', style={"margin-top": "0px", "margin-bottom": "0px"})],
                         className="pretty_container two columns",
                         ),
                html.Div([html.H6('Active', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='active-indicator-state',
                                    figure=create_count_indicator(state='Maharashtra', status='Total Active'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Active']}
                         ),
                html.Div([html.H6('Confirmed', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='confirmed-indicator-state',
                                    figure=create_count_indicator(state='Maharashtra', status='Total Confirmed'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Confirmed']}
                         ),
                html.Div([html.H6('Deceased', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='deceased-indicator-state',
                                    figure=create_count_indicator(state='Maharashtra', status='Total Deceased'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Deceased']}
                         ),
                html.Div([html.H6('Recovered', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='recovered-indicator-state',
                                    figure=create_count_indicator(state='Maharashtra', status='Total Recovered'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Recovered']}
                         ),
                html.Div([html.H6('Tests', style={"padding": 0,"margin-top": "0px", "margin-bottom": "0px"}),
                          dcc.Graph(id='tests-indicator-state',
                                    figure=create_test_count_indicator(state='Maharashtra', status='Total Tested'))],
                         className="pretty_container two columns",
                         style={"padding": 5, "border": "solid", "border-color": color_discrete_map_total['Total Tested']}
                         ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [html.Div([dcc.RadioItems(id='status-map-state', options=[{'label': i, 'value': i} for i in
                                                                              ['Active', 'Confirmed', 'Deceased',
                                                                               'Recovered']],
                                              value='Active', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     dcc.Graph(id='map-state')],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.Div([dcc.RadioItems(id='total-daily-state',
                                              options=[{'label': i, 'value': i} for i in ['Total', 'Daily']],
                                              value='Total', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     html.Div([dcc.RadioItems(id='status-daily-state',
                                              options=[{'label': i, 'value': i} for i in
                                                       ['Confirmed', 'Deceased', 'Recovered']],
                                              value='Confirmed', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     dcc.Graph(id='chart-state')],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
