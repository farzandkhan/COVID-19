import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px


# title of the webpage
st.title('COVID-19 India Dashboard')

# add side bar of the webpage
st.sidebar.title('Data Visualizer')
st.sidebar.markdown('Use the options in the sidebar to create 🖱️ custom Charts 📊 and Graphs 📉')
st.markdown('This is a webapp to Visualize 📈 COVID-19 🦠 pandemic situation in India 🌏 ')


@st.cache(persist=True)
def load_state_data():
    state_data = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    state_data['Death Rate (%)'] = round(state_data['Deaths']/state_data['Confirmed'], 4)*100
    return state_data
state_data = load_state_data()

st.button('Re-Run')
if st.button == True:
    st.write('Refreshing Data')
    state_data = load_state_data()
def homepage():
    import datetime
    now = datetime.datetime.now()
    value = []
    key = ['Number of Days since 1st Infection 🗓️', 'Total Number of Confirmed Cases 🤒',
          'Total Number of Recovered 😊', 'Total Number of Deaths 💀', 'Total Number of Active Cases ➕', 'Death Rate (%) ⚰️']
    start = 'Jan 31 2020'; start = pd.to_datetime(start); start = start.dayofyear
    today = pd.to_datetime(now).dayofyear
    value.append(today-start)
    value.append(state_data[(state_data['State'] == 'Total')]['Confirmed'][0])
    value.append(state_data[(state_data['State'] == 'Total')]['Recovered'][0])
    value.append(state_data[(state_data['State'] == 'Total')]['Deaths'][0])
    value.append(state_data[(state_data['State'] == 'Total')]['Active'][0])
    value.append(round(value[3]/value[1], 4)*100)
    return pd.DataFrame({'Text': key, 'Number': value})
homepage = homepage()
st.write(homepage)


# show main table with top 10 infected countries
# add subheader for the side bar
st.sidebar.subheader('Choose the type of Graph you want')

# # add dropdown
select = st.sidebar.selectbox('Visualization type', ['Death Rate %', 'Top 10 Infected States'], key='1')
if not st.sidebar.checkbox('Hide Graphs', True):
    if select == 'Death Rate %':
        st.markdown('### Bar Chart depicting Death Rate (%) of Indian states')
        state_data['Death Rate (%)'] = round(state_data['Deaths']/state_data['Confirmed'], 4)*100
        death_perc = state_data[['State', 'Death Rate (%)']].sort_values(by='Death Rate (%)', ascending=False)[:29]
        fig = px.bar(death_perc, x='State', y='Death Rate (%)', height=600, width=800)
        st.plotly_chart(fig)
    elif select == 'Top 10 Infected States':
        st.markdown('### Table depicting 10 States with maximum number of Confirmed Cases')
        top10 = state_data[['State', 'Confirmed', 'Recovered', 'Deaths', 'Active', 'Death Rate (%)']][1:11]
        st.write(top10)



# input text box
st.sidebar.subheader('State Data comparision')
state = st.sidebar.text_input('Enter upto five State codes seprated by comma')
state = state.split(', ')
state
if not st.sidebar.checkbox('Hide Table', False):
    #st.markdown(f'Showing data for {state}')
    st_len = len(state)
    if st_len > 5:
        st.write('Please enter no more than 5 State codes at once')
    elif st_len == 5:
        st.write(state_data[(state_data['State_code'] == state[0]) | (state_data['State_code'] == state[1]) | (state_data['State_code'] == state[2]) | (state_data['State_code'] == state[3]) | (state_data['State_code'] == state[4])][['State', 'Confirmed', 'Recovered', 'Deaths', 'Active']].reset_index(drop=True))
    elif st_len == 4:
        st.write(state_data[(state_data['State_code'] == state[0]) | (state_data['State_code'] == state[1]) | (state_data['State_code'] == state[2]) | (state_data['State_code'] == state[3])][['State', 'Confirmed', 'Recovered', 'Deaths', 'Active']].reset_index(drop=True))
    elif st_len == 3:
        st.write(state_data[(state_data['State_code'] == state[0]) | (state_data['State_code'] == state[1]) | (state_data['State_code'] == state[2])][['State', 'Confirmed', 'Recovered', 'Deaths', 'Active']].reset_index(drop=True))
    elif st_len == 2:
        st.write(state_data[(state_data['State_code'] == state[0]) | (state_data['State_code'] == state[1])][['State', 'Confirmed', 'Recovered', 'Deaths', 'Active']].reset_index(drop=True))
    elif st_len == 1:
        st.write(state_data[(state_data['State_code'] == state[0])][['State', 'Confirmed', 'Recovered', 'Deaths', 'Active']].reset_index(drop=True))
    elif st_len == 0:
        st.write('Please enter State code to enable Graph')
