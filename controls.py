from plotly.colors import diverging, qualitative, sequential

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
covid19india_api_json = {
    'raw_data1': 'https://api.covid19india.org/raw_data1.json',
     'raw_data2': 'https://api.covid19india.org/raw_data2.json',
     'raw_data3': 'https://api.covid19india.org/raw_data3.json',
     'data': 'https://api.covid19india.org/data.json',
     'state_district_wise': 'https://api.covid19india.org/state_district_wise.json',
     'state_district_wise_v2': 'https://api.covid19india.org/v2/state_district_wise.json',
     'states_daily': 'https://api.covid19india.org/states_daily.json',
     'state_test_data': 'https://api.covid19india.org/state_test_data.json',
     'resources': 'https://api.covid19india.org/resources/resources.json',
     'zones': 'https://api.covid19india.org/zones.json',
}
covid19india_api_csv = {
    'raw_data1': 'https://api.covid19india.org/csv/latest/raw_data1.csv',
    'raw_data2': 'https://api.covid19india.org/csv/latest/raw_data2.csv',
    'raw_data3': 'https://api.covid19india.org/csv/latest/raw_data3.csv',
    'death_and_recovered1': 'https://api.covid19india.org/csv/latest/death_and_recovered1.csv',
    'death_and_recovered2': 'https://api.covid19india.org/csv/latest/death_and_recovered2.csv',
    'state_wise': 'https://api.covid19india.org/csv/latest/state_wise.csv',
    'case_time_series': 'https://api.covid19india.org/csv/latest/case_time_series.csv',
    'district_wise': 'https://api.covid19india.org/csv/latest/district_wise.csv',
    'state_wise_daily': 'https://api.covid19india.org/csv/latest/state_wise_daily.csv',
    'statewise_tested_numbers_data': 'https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv',
    'tested_numbers_icmr_data': 'https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv',
    'sources_list': 'https://api.covid19india.org/csv/latest/sources_list.csv',
    'raw_data': 'https://api.covid19india.org/csv/latest/raw_data.csv',
    'death_and_recovered': 'https://api.covid19india.org/csv/latest/death_and_recovered.csv',
    'travel_history': 'https://api.covid19india.org/csv/latest/travel_history.csv'
}
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
color_discrete_map_total = {'Total Active': '#2170B5', 'Total Confirmed': '#6A51A3',
                            'Total Deceased': '#CB181D', 'Total Recovered': '#238B46', 'Total Tested': sequential.solar[8]}
color_discrete_map_daily = {'Daily Active': '#2170B5', 'Daily Confirmed': '#6A51A3',
                            'Daily Deceased': '#CB181D', 'Daily Recovered': '#238B46'}
