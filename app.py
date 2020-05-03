import json
from itertools import product

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash.dependencies import Input, Output
from pandas import json_normalize

pio.templates['plotly'].layout['paper_bgcolor'] = '#F9F9F9'
pio.templates['plotly'].layout['plot_bgcolor'] = '#F9F9F9'
pio.templates['plotly'].layout['geo'].bgcolor = '#F9F9F9'

map_dict = {'India': 'india.json', 'Andaman and Nicobar Islands': 'andamannicobarislands_district.json',
            'Andhra Pradesh': 'andhrapradesh_district.json', 'Arunachal Pradesh': 'arunachalpradesh_district.json',
            'Assam': 'assam_district.json', 'Bihar': 'bihar_district.json', 'Chandigarh': 'chandigarh_district.json',
            'Chhattisgarh': 'chhattisgarh_district.json', 'Dadra and Nagar Haveli': 'dadranagarhaveli_district.json',
            'Delhi': 'delhi_district.json', 'Goa': 'goa_district.json', 'Gujarat': 'gujarat_district.json',
            'Haryana': 'haryana_district.json', 'Himachal Pradesh': 'himachalpradesh_district.json',
            'Jammu and Kashmir': 'jammukashmir_district.json', 'Jharkhand': 'jharkhand_district.json',
            'Karnataka': 'karnataka_district.json', 'Kerala': 'kerala_district.json', 'Ladakh': 'ladakh_district.json',
            'Lakshadweep': 'lakshadweep_district.json', 'Madhya Pradesh': 'madhyapradesh_district.json',
            'Maharashtra': 'maharashtra_district.json', 'Manipur': 'manipur_district.json',
            'Meghalaya': 'meghalaya_district.json', 'Mizoram': 'mizoram_district.json',
            'Nagaland': 'nagaland_district.json', 'Odisha': 'odisha_district.json',
            'Puducherry': 'puducherry_district.json', 'Punjab': 'punjab_district.json',
            'Rajasthan': 'rajasthan_district.json', 'Sikkim': 'sikkim_district.json',
            'Tamil Nadu': 'tamilnadu_district.json', 'Telangana': 'telangana_district.json',
            'Tripura': 'tripura_district.json', 'Uttar Pradesh': 'uttarakhand_district.json',
            'Uttarakhand': 'uttarpradesh_district.json', 'West Bengal': 'westbengal_district.json'}
state_codes = {'TT': 'Total', 'MH': 'Maharashtra', 'DL': 'Delhi', 'TN': 'Tamil Nadu', 'RJ': 'Rajasthan',
               'MP': 'Madhya Pradesh', 'GJ': 'Gujarat', 'UP': 'Uttar Pradesh', 'TG': 'Telangana',
               'AP': 'Andhra Pradesh', 'KL': 'Kerala', 'KA': 'Karnataka', 'JK': 'Jammu and Kashmir',
               'WB': 'West Bengal', 'HR': 'Haryana', 'PB': 'Punjab', 'BR': 'Bihar', 'OR': 'Odisha', 'UT': 'Uttarakhand',
               'CT': 'Chhattisgarh', 'HP': 'Himachal Pradesh', 'AS': 'Assam', 'JH': 'Jharkhand', 'CH': 'Chandigarh',
               'LA': 'Ladakh', 'AN': 'Andaman and Nicobar Islands', 'ML': 'Meghalaya', 'GA': 'Goa', 'PY': 'Puducherry',
               'MN': 'Manipur', 'TR': 'Tripura', 'MZ': 'Mizoram', 'AR': 'Arunachal Pradesh', 'NL': 'Nagaland',
               'DN': 'Dadra and Nagar Haveli', 'DD': 'Daman and Diu', 'LD': 'Lakshadweep', 'SK': 'Sikkim'}

total_list = ['Total Active', 'Total Confirmed', 'Total Deceased', 'Total Recovered']
daily_list = ['Daily Confirmed', 'Daily Deceased', 'Daily Recovered']
color_continuous_scale_dict = {'Total Active': 'Blues', 'Total Confirmed': 'Purples',
                               'Total Deceased': 'Reds', 'Total Recovered': 'Greens', }
color_discrete_map = {'Total Active': '#59C3C3', 'Total Confirmed': '#C359AC', 'Total Deceased': '#F9ADA0', 'Total Recovered': '#849E68'}

with open('data/json/states_daily.json') as states_daily:
    states_daily_json = json.load(states_daily)
df_states = pd.DataFrame(states_daily_json['states_daily']).replace('', '0')
df_states.columns = map(str.upper, df_states.columns)
df_states = df_states.rename(columns=state_codes).melt(id_vars=['DATE', 'STATUS']).rename(
    columns={'variable': 'STATE', 'value': 'COUNT'})
df_states = df_states.astype({'DATE': 'str', 'STATUS': 'str', 'STATE': 'str', 'COUNT': 'int32'})
df_states = df_states.pivot_table(index=['DATE', 'STATE'], columns='STATUS', values='COUNT').reset_index()
df_states['DATE'] = pd.to_datetime(df_states['DATE'])
df_states = df_states.sort_values(by=['STATE', 'DATE'])
df_states.columns.name = None
df_states['Total Confirmed'] = df_states.groupby('STATE')['Confirmed'].transform(pd.Series.cumsum)
df_states['Total Deceased'] = df_states.groupby('STATE')['Deceased'].transform(pd.Series.cumsum)
df_states['Total Recovered'] = df_states.groupby('STATE')['Recovered'].transform(pd.Series.cumsum)
df_states['Total Active'] = df_states['Total Confirmed'] - df_states['Total Deceased'] - df_states['Total Recovered']
df_states = df_states.rename(
    columns={'Confirmed': 'Daily Confirmed', 'Deceased': 'Daily Deceased', 'Recovered': 'Daily Recovered'})
df_states = df_states.melt(id_vars=['DATE', 'STATE']).rename(columns={'variable': 'STATUS', 'value': 'COUNT'})
df_states['DATE'] = df_states['DATE'].astype(str)

with open('data/json/state_district_wise_v2.json') as state_district_wise_v2:
    state_district_wise_v2_json = json.load(state_district_wise_v2)
df_state_district = json_normalize(data=state_district_wise_v2_json, record_path='districtData',
                                   meta=['state', 'statecode'])
df_state_district = df_state_district.rename(
    columns={'district': 'District', 'notes': 'Notes', 'active': 'Active', 'confirmed': 'Confirmed',
             'deceased': 'Deceased', 'recovered': 'Recovered', 'delta.confirmed': 'Delta Confirmed',
             'delta.deceased': 'Delta Deceased', 'delta.recovered': 'Delta Recovered', 'state': 'State',
             'statecode': 'State Code'})


def load_map_json(map_name):
    with open('maps/geojson/' + map_dict[map_name]) as res:
        map_json = json.load(res)
    # print('Loaded the map of ' + map_name + '.')

    return map_json


def create_country_map(status):
    country_json = load_map_json(map_name='India')
    today = df_states['DATE'][df_states.index[-1]]
    count = str(int(df_states[(df_states['DATE'] == today) & (df_states['STATE'] == 'Total') & (df_states['STATUS'] == status)]['COUNT']))
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
                                  annotations=[
                                      dict(x=0.1, y=0.95, showarrow=False, text='India<br>' + status.split()[1] + ': ' + count,
                                           xref="paper", yref="paper",
                                           font=dict(size=15, color=color_discrete_map[status])), ]
                                  )

    # Set map data, hover text and slider to today.
    # today = df_states_fig['DATE'][df_states_fig.index[-1]]
    fig_country_map.data[0].z = df_states_fig[df_states_fig['DATE'] == today]['COUNT'].to_numpy()
    fig_country_map.data[0].hovertemplate = 'Date=' + today + '<br>State/UT=%{location}<br>' + status + '=%{z}'
    fig_country_map['layout']['sliders'][0].active = len(df_states_fig['DATE'].unique()) - 1
    # print(fig_country_map.data[0])

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
                                    color_discrete_map=color_discrete_map)
        fig_country_chart.update_traces(mode='markers+lines')
    else:
        df_country_chart = df_country_chart[df_country_chart['STATUS'] == chart_type + ' ' + bar_type]
        fig_country_chart = px.bar(df_country_chart,
                                   x='DATE',
                                   y='COUNT',
                                   log_y=False,
                                   )
    fig_country_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                    legend=dict(orientation='h', title=dict(text='')),
                                    xaxis=dict(title=dict(text='')),
                                    yaxis=dict(title=dict(text=''))
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
                                  # animation_frame='DATE'
                                  )
    fig_state_map.update_geos(fitbounds="locations", visible=False)
    fig_state_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis=dict(showscale=False),
        annotations=[dict(x=0.1, y=0.95, showarrow=False, text=state+'<br>'+status + ': '+ count, xref="paper", yref="paper",
                          font=dict(size=15, color=color_discrete_map['Total ' + status])), ]
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
                                  color_discrete_map={'Total Confirmed': '#59C3C3', 'Total Recovered': '#849E68',
                                                      'Total Deceased': '#F9ADA0', 'Total Active': '#C359AC'})
        fig_state_chart.update_traces(mode='markers+lines')
    else:
        df_state_chart = df_state_chart[df_state_chart['STATUS'] == chart_type + ' ' + bar_type]
        fig_state_chart = px.bar(df_state_chart,
                                 x='DATE',
                                 y='COUNT',
                                 log_y=False,
                                 )

    fig_state_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                  legend=dict(orientation='h', title=dict(text='')),
                                  xaxis=dict(title=dict(text='')),
                                  yaxis=dict(title=dict(text=''))
                                  )

    return fig_state_chart


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

app.layout = html.Div(
    [
        # dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
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
                            href="#",
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
                html.Div([html.Div(
                    [dcc.RadioItems(id='country-map-status', options=[{'label': i, 'value': 'Total ' + i} for i in
                                                                      ['Active', 'Confirmed', 'Deceased',
                                                                       'Recovered']],
                                    value='Total Active', labelStyle={'display': 'inline-block'})],
                    className="radio-group"),
                    dcc.Graph(id='map-country')],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.Div([dcc.RadioItems(id='country-total-daily',
                                              options=[{'label': i, 'value': i} for i in ['Total', 'Daily']],
                                              value='Total', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     html.Div([dcc.RadioItems(id='country-daily-status',
                                              options=[{'label': i, 'value': i} for i in
                                                       ['Confirmed', 'Deceased', 'Recovered']],
                                              value='Confirmed', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     dcc.Graph(id='chart-india')
                     ],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [html.Div([dcc.RadioItems(id='state-map-status', options=[{'label': i, 'value': i} for i in
                                                                              ['Active', 'Confirmed', 'Deceased',
                                                                               'Recovered']],
                                              value='Active', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     dcc.Graph(id='map-state')],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.Div([dcc.RadioItems(id='state-total-daily',
                                              options=[{'label': i, 'value': i} for i in ['Total', 'Daily']],
                                              value='Total', labelStyle={'display': 'inline-block'})],
                              className="radio-group"),
                     html.Div([dcc.RadioItems(id='state-daily-status',
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


@app.callback(
    Output(component_id='map-state', component_property='figure'),
    [Input(component_id='map-country', component_property='clickData'),
     Input(component_id='state-map-status', component_property='value')
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
     Input(component_id='state-total-daily', component_property='value'),
     Input(component_id='state-daily-status', component_property='value')]
)
def update_state_chart(clicked_state, state_total_daily, state_daily_status):
    if clicked_state is not None:
        return create_state_chart(state_name=clicked_state['points'][0]['location'], chart_type=state_total_daily,
                                  bar_type=state_daily_status)
    else:
        return create_state_chart(state_name='Maharashtra', chart_type=state_total_daily, bar_type=state_daily_status)


@app.callback(
    Output(component_id='map-country', component_property='figure'),
    [Input(component_id='country-map-status', component_property='value')]
)
def update_country_map(value):
    return create_country_map(status=value)


@app.callback(
    Output(component_id='country-daily-status', component_property='style'),
    [Input(component_id='country-total-daily', component_property='value')]
)
def update_country_chart_radio(value):
    if value == 'Daily':
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='state-daily-status', component_property='style'),
    [Input(component_id='state-total-daily', component_property='value')]
)
def update_state_chart_radio(value):
    if value == 'Daily':
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='chart-india', component_property='figure'),
    [Input(component_id='country-total-daily', component_property='value'),
     Input(component_id='country-daily-status', component_property='value')]
)
def update_country_chart(country_total_daily, country_daily_status):
    return create_country_chart(chart_type=country_total_daily, bar_type=country_daily_status)


if __name__ == '__main__':
    app.run_server()
