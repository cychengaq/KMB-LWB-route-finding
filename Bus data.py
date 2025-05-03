import streamlit as st
import pandas as pd

bus = pd.read_json('https://data.etabus.gov.hk/v1/transport/kmb/route/')
stop = pd.read_json('https://data.etabus.gov.hk/v1/transport/kmb/route-stop')

def stop_name(x):
    return pd.read_json(f"https://data.etabus.gov.hk/v1/transport/kmb/stop/{x}").iloc[2,3]

st.markdown('### KMB/ LWB Route finding system')
st.markdown('***Developed by Isaac CHENG***')
'---'
x = st.text_input("Please enter KMB/ LWB route number, e.g. 80K/ 91M.")

bd = bus.data
for route in bd:
    if route['route'] == x:
        if route['service_type']=='1':
            st.write(f"Bound = {route['bound']}, Service type = {route['service_type']} --> {route['route']}: {route['orig_tc']} -> {route['dest_tc']}")
        elif route['service_type']!='1':
            st.write(f"Bound = {route['bound']}, Service type = {route['service_type']} --> {route['route']}: {route['orig_tc']} -> {route['dest_tc']} [特別班次]")

'---'
st.caption('Select your desired bound and type according to the information displayed after you input the route number.')

with st.form('input'):
    bound = st.radio('Please select the bound.',['O','I'])
    type = str(st.slider('Please select the service type. (1-7)',min_value=0, max_value=7))
    st.form_submit_button("Confirm")
'---'
details = [stops for stops in stop.data if stops['route']==x and stops['bound']==bound and stops['service_type']==type]
if details == []:
    st.error('Please ensure the bound/ direction is available!')
stop_code = [detail['stop'] for detail in details]
count = 1
for code in stop_code:
    st.write(f"{count}. {stop_name(code)}")
    count += 1