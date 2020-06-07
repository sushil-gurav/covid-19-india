import json
import requests
import pandas as pd
from pandas import json_normalize
from itertools import product
from controls import *

states_daily_json = json.loads(requests.get(covid19india_api_json['states_daily']).text)

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

state_district_wise_v2_json = json.loads(requests.get(covid19india_api_json['state_district_wise_v2']).text)

df_state_district = json_normalize(data=state_district_wise_v2_json,
                                   record_path='districtData',
                                   meta=['state', 'statecode'])
df_state_district = df_state_district.rename(
    columns={'district': 'District', 'notes': 'Notes', 'active': 'Active', 'confirmed': 'Confirmed',
             'deceased': 'Deceased', 'recovered': 'Recovered', 'delta.confirmed': 'Delta Confirmed',
             'delta.deceased': 'Delta Deceased', 'delta.recovered': 'Delta Recovered', 'state': 'State',
             'statecode': 'State Code'})

df_state_test = pd.read_csv(covid19india_api_csv['statewise_tested_numbers_data'])
df_state_test['Updated On'] = pd.to_datetime(df_state_test['Updated On'], infer_datetime_format=True)
df_state_test = df_state_test[df_state_test['Updated On'] != '2020-02-16']
df_state_test = df_state_test[
    ['Updated On', 'State', 'Total Tested', 'Positive', 'Negative', 'Unconfirmed', 'Tests per thousand',
     'Tests per million']]
df_state_test_mask = pd.DataFrame(list(product(df_state_test['Updated On'].unique(), df_state_test.State.unique())),
                                  columns=['Updated On', 'State'])
df_state_test_mask = pd.concat([df_state_test_mask, pd.DataFrame(
    columns=['Total Tested', 'Positive', 'Test positivity rate', 'Tests per thousand', 'Tests per million'])])
df_state_test_mask = df_state_test_mask.set_index(['Updated On', 'State'])
df_state_test = df_state_test.set_index(['Updated On', 'State'])
df_state_test = df_state_test_mask.combine_first(df_state_test).reset_index()
for state in df_state_test.State.unique():
    df_state_test[df_state_test['State'] == state] = df_state_test[df_state_test['State'] == state].fillna(
        method='ffill').replace(to_replace=0, method='ffill')
df_state_test = df_state_test.astype(
    {'Positive': 'float64', 'Test positivity rate': 'float64', 'Tests per million': 'float64',
     'Tests per thousand': 'float64', 'Total Tested': 'float64'})
