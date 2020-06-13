import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import diverging, qualitative
from plotly.subplots import make_subplots

from data import *


def create_test_chart(state, chart_type, line_type):
    if state == 'India':
        df_state_test_fig = df_state_test.groupby('Updated On').sum().reset_index()
    else:
        df_state_test_fig = df_state_test[df_state_test['State'] == state].fillna(method='ffill').fillna(
            0).reset_index()
    df_state_test_fig['Daily Tested'] = df_state_test_fig['Total Tested'] - df_state_test_fig['Total Tested'].shift(1)
    df_state_test_fig['Daily Positive'] = df_state_test_fig['Positive'] - df_state_test_fig['Positive'].shift(1)
    df_state_test_fig['Daily Negative'] = df_state_test_fig['Negative'] - df_state_test_fig['Negative'].shift(1)
    df_state_test_fig['Daily Unconfirmed'] = df_state_test_fig['Unconfirmed'] - df_state_test_fig['Unconfirmed'].shift(1)
    df_state_test_fig['Tests Per Confirmed Case'] = df_state_test_fig['Total Tested'] / df_state_test_fig['Positive']

    if chart_type == 'Total':
        fig_test_chart = px.line(df_state_test_fig,
                                 x='Updated On',
                                 y=line_type,
                                 log_y=False,
                                 line_shape='spline',
                                 )
        fig_test_chart.update_traces(mode='lines')
    else:
        fig_test_chart = go.Figure(data=[
            go.Bar(name='Negative', x=df_state_test_fig['Updated On'].to_list(),
                   y=df_state_test_fig['Daily Negative'].to_list(), marker_color='green'),
            go.Bar(name='Unconfirmed', x=df_state_test_fig['Updated On'].to_list(),
                   y=df_state_test_fig['Daily Unconfirmed'].to_list(), marker_color='yellow'),
            go.Bar(name='Positive', x=df_state_test_fig['Updated On'].to_list(),
                   y=df_state_test_fig['Daily Positive'].to_list(), marker_color='red')
        ])
        fig_test_chart.update_layout(barmode='stack')

    fig_test_chart.update_layout(annotations=[dict(x=0.5, y=1.1, showarrow=False,
                                                   text='Test Count - ' + state,
                                                   xref="paper", yref="paper",
                                                   font=dict(size=15)), ]
                                 )

    return fig_test_chart


def get_growth_data(state):
    if state == 'India':
        state = 'Total'
    df_states_growth = df_states[(df_states['STATE'] == state) & (df_states['STATUS'] == 'Total Confirmed')]
    for i in range(0, df_states_growth.shape[0] - 6):
        df_states_growth.loc[df_states_growth.index[i + 6], '7 Day CDGR'] = np.round(
            (((df_states_growth.iloc[i + 6, 3] / df_states_growth.iloc[i, 3]) ** (1 / 6.0) - 1) * 100), 1)
    for i in range(0, df_states_growth.shape[0] - 2):
        df_states_growth.loc[df_states_growth.index[i + 2], '3 Day CDGR'] = np.round(
            (((df_states_growth.iloc[i + 2, 3] / df_states_growth.iloc[i, 3]) ** (1 / 2.0) - 1) * 100), 1)

    return df_states_growth


def create_doubling_rate_chart(state):
    df_states_growth = get_growth_data(state=state)
    df_states_growth['Doubling Rate in Days'] = 72.0 / df_states_growth['7 Day CDGR']
    fig_doubling_rate_chart = px.line(df_states_growth,
                                      x='DATE',
                                      y='Doubling Rate in Days',
                                      log_y=False,
                                      line_shape='spline',
                                      )
    fig_doubling_rate_chart.update_traces(mode='lines')
    fig_doubling_rate_chart.update_layout(annotations=[dict(x=0.5, y=1.1, showarrow=False,
                                                            text='Doubling Rate - ' + state,
                                                            xref="paper", yref="paper",
                                                            font=dict(size=15)), ]
                                          )

    return fig_doubling_rate_chart


def create_cdgr_chart(state):
    df_states_growth = get_growth_data(state=state).melt(id_vars=['DATE', 'STATE', 'STATUS', 'COUNT']).rename(
        columns={'variable': 'GROWTH', 'value': 'RATE'})
    df_states_growth['DATE'] = df_states_growth['DATE'].astype(str)

    fig_cdgr_chart = px.line(df_states_growth,
                             x='DATE',
                             y='RATE',
                             log_y=False,
                             line_shape='spline',
                             color='GROWTH',
                             # color_discrete_map=color_discrete_map_total
                             )
    fig_cdgr_chart.update_traces(mode='lines')
    fig_cdgr_chart.update_layout(legend=dict(orientation='h', title=dict(text='Growth Rate')),
                                 xaxis=dict(title=dict(text='')),
                                 yaxis=dict(title=dict(text='')),
                                 annotations=[
                                     dict(x=0.5, y=1.1, showarrow=False,
                                          text='Percentage Growth Rate - ' + state,
                                          xref="paper", yref="paper",
                                          font=dict(size=15)), ]
                                 )

    return fig_cdgr_chart


def create_gauge_graph_object(value, title, reference, max_value):
    return go.Indicator(
        value=value,
        mode="gauge+number+delta",
        title={'text': title, 'font': {'size': 12}},
        delta={'reference': reference, 'increasing': {'color': '#FF4136'}, 'decreasing': {'color': '#3D9970'}},
        gauge={'axis': {'range': [None, max_value]},
               'bar': {'color': qualitative.Plotly[0]},
               'steps': [
                   {'range': [0, max_value * 0.5], 'color': diverging.RdYlGn[8]},
                   {'range': [max_value * 0.5, max_value * 0.8], 'color': diverging.RdYlGn[4]},
                   {'range': [max_value * 0.8, max_value], 'color': diverging.RdYlGn[2]}]},
    )


def create_animated_gauge_chart(state):
    df_states_growth = get_growth_data(state=state)
    df_states_growth['DATE'] = df_states_growth['DATE'].astype(str)
    value7 = df_states_growth['7 Day CDGR'].iloc[-1]
    value3 = df_states_growth['3 Day CDGR'].iloc[-1]
    # title = df_states_growth['DATE'].iloc[-1]
    title7 = '7 Day CDGR'
    title3 = '3 Day CDGR'
    max_value7 = df_states_growth['7 Day CDGR'].max() * 1.2
    max_value3 = df_states_growth['3 Day CDGR'].max() * 1.2
    reference7 = df_states_growth['7 Day CDGR'].iloc[-2]
    reference3 = df_states_growth['3 Day CDGR'].iloc[-2]

    fig_gauge_chart = make_subplots(rows=1, cols=2, subplot_titles=('7 Day CDGR', '3 Day CDGR'),
                                    specs=[[{"type": "indicator"}, {"type": "indicator"}]])
    fig_gauge_chart.add_trace(
        create_gauge_graph_object(value=value7, title=title7, reference=reference7, max_value=max_value7), row=1, col=1)
    fig_gauge_chart.add_trace(
        create_gauge_graph_object(value=value3, title=title3, reference=reference3, max_value=max_value3), row=1, col=2)

    frames = []

    for i in range(0, df_states_growth.shape[0]):
        frame_value7 = df_states_growth['7 Day CDGR'].iloc[i]
        frame_value3 = df_states_growth['3 Day CDGR'].iloc[i]
        frame_title = df_states_growth['DATE'].iloc[i]
        if i > 0:
            frame_reference7 = df_states_growth['7 Day CDGR'].iloc[i - 1]
            frame_reference3 = df_states_growth['3 Day CDGR'].iloc[i - 1]
        else:
            frame_reference7 = df_states_growth['7 Day CDGR'].iloc[i]
            frame_reference3 = df_states_growth['7 Day CDGR'].iloc[i]

        frames.append(dict(name=i,
                           data=[create_gauge_graph_object(value=frame_value7,
                                                           title=title7,
                                                           reference=frame_reference7,
                                                           max_value=max_value7),
                                 create_gauge_graph_object(value=frame_value3,
                                                           title=title3,
                                                           reference=frame_reference3,
                                                           max_value=max_value3)
                                 ],
                           traces=[0, 1]))

    updatemenus = [dict(type='buttons',
                        buttons=[dict(label='Play',
                                      method='animate',
                                      args=[[f'{k}' for k in range(df_states_growth.shape[0])],
                                            dict(frame=dict(duration=500, redraw=False),
                                                 transition=dict(duration=0),
                                                 easing='linear',
                                                 fromcurrent=True,
                                                 mode='immediate'
                                                 )])],
                        direction='left',
                        pad=dict(r=0, t=0),
                        showactive=True, x=0.1, y=0, xanchor='right', yanchor='top')
                   ]

    sliders = [{'yanchor': 'top',
                'xanchor': 'left',
                'currentvalue': {'font': {'size': 12}, 'prefix': 'Date: ', 'visible': True, 'xanchor': 'right'},
                'transition': {'duration': 500.0, 'easing': 'linear'},
                # 'pad': {'b': 10, 't': 10},
                'len': 0.9, 'x': 0.1, 'y': 0,
                'steps': [{'args': [[k], {'frame': {'duration': 500.0, 'easing': 'linear', 'redraw': False},
                                          'transition': {'duration': 0, 'easing': 'linear'}}],
                           'label': df_states_growth['DATE'].iloc[k], 'method': 'animate'} for k in
                          range(df_states_growth.shape[0])
                          ]}]

    fig_gauge_chart.update(frames=frames),
    fig_gauge_chart.update_layout(updatemenus=updatemenus,
                                  sliders=sliders,
                                  annotations=[
                                      dict(x=0.5, y=1.1, showarrow=False,
                                           text='Percentage Growth Rate - ' + state,
                                           xref="paper", yref="paper",
                                           font=dict(size=15)), ]
                                  )

    fig_gauge_chart['layout']['sliders'][0].active = len(df_states_growth['DATE'].unique()) - 1
    return fig_gauge_chart


dropdown_options = [{'label': 'India', 'value': 'India'}]
dropdown_options.extend([{'label': i, 'value': i} for i in df_state_test.State.unique()])

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
                            html.Button("Home", id="home-button"),
                            href="home",
                        ),
                        html.A(
                            html.Button("Insights", id="insights-button",
                                        style={"background-color": "#119dff", "color": "#ffffff"}),
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
                dcc.Dropdown(id='state-dropdown',
                             options=dropdown_options,
                             value='India'
                             )
            ],
            id='dropdown',
            # className='row flex-display'
        ),
        html.Div(
            [
                html.Div(
                    [html.Div([dcc.RadioItems(id='total-daily-test',
                                              options=[{'label': i, 'value': i} for i in ['Total', 'Daily']],
                                              value='Total', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     html.Div([dcc.RadioItems(id='status-total-test',
                                              options=[{'label': i, 'value': i} for i in
                                                       ['Total Tested', 'Tests per million']],
                                              value='Total Tested', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     dcc.Graph(id='test-chart'),
                     ],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [
                        dcc.Graph(id='doubling-rate-chart'),
                    ],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id='cdgr-chart')],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [dcc.Graph(id='gauge-chart'),
                     # dcc.Graph(id='gauge-chart-7', figure=test())
                     ],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
