#Covid Streamlit Choropleth Map

import pandas as pd
import numpy as np
import json

import plotly.express as px
import plotly.graph_objects as go


import streamlit as st
import requests

# --- Page Config --- #
st.set_page_config(page_title = "Covid Map Brazil", page_icon=":test_tube:", layout = 'wide')

### --- Project XI - Covid Map --- ###
with st.container():
    st.subheader("Project XI - Covid Brazil Choropleth Map")
    st.write('---')

# --- DFs --- #
with st.container():    
    df_states = pd.read_csv('Streamlit Projects\project_covid\data\df_states.csv')
    json_states = json.load(open("Streamlit Projects\\project_covid\data\\brazil_geo.json"))
    #df pre processing
    df_states = df_states.rename(columns={'casosAcumulado':'Casos Acumulados',
                              'casosNovos':'Casos Novos',
                              'obitosAcumulado':'Óbitos Acumulados',
                              'obitosNovos':'Óbitos Novos'})
    df_states['data'] = pd.to_datetime(df_states['data'])
    df_region = df_states['regiao'].unique().tolist()

# --- LAYOUT --- #
with st.container():
    column1, column2 = st.columns([1,4])
    #Opções
    with column1:
        st.write('Tipo de Gráfico')
        choro_select = st.selectbox("",['Casos Novos','Óbitos Novos'])
        st.write('---')
        st.write('Regiões')    
        region_select = st.multiselect("",df_region, default = df_region)
        st.write('---')
        st.write('Data')

        #CALENDÁRIO
        with st.container():  
            date_start = st.date_input('De', value = df_states['data'].min(), 
                        min_value = df_states['data'].min(), max_value=df_states['data'].max())
            date_end = st.date_input('Até', value = df_states['data'].max(), 
                        min_value= df_states['data'].min(), max_value=df_states['data'].max())
            #convert to datetime
            date_start = pd.to_datetime(date_start)
            date_end = pd.to_datetime(date_end)
        st.write(f'Casos Acumulados:  {df_states["Casos Acumulados"][df_states["data"] == date_end].sum()}')
        st.write(f'Óbitos Acumulados:  {df_states["Óbitos Acumulados"][df_states["data"] == date_end].sum()}')

        # --- RESULT DATAFRAME --- #
        with st.container():
            mask = (df_states['data'].between(date_start,date_end)) & (df_states['regiao'].isin(region_select))
            #df for dashboard
            df_mask = df_states[mask]
            df_map_states = df_mask.groupby('estado').sum().reset_index()

    #Gráfico
    with column2:
        #create map fig
        choro_map = px.choropleth(df_map_states, locations = 'estado',
                            geojson = json_states, color = choro_select, 
                            scope = 'south america',
                            width=1400, height=800)
        st.plotly_chart(choro_map)

with st.container():
    column1, column2 = st.columns([4,1])
    with column1:
        #REGION PLOT
        st.write('Region Historical Data')
        df_newcases = df_mask.groupby(['data','regiao']).sum().reset_index()
        linechart_region = px.line(df_newcases, x='data', y="Casos Novos",
                                color = 'regiao', width = 950, height = 250,
                                color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(linechart_region)

st.write('Region Historical Data')
linechart_region = px.line(df_newcases, x='data', y="Óbitos Novos",
                        color = 'regiao',
                        width = 950, height = 250,
                        color_discrete_sequence=px.colors.qualitative.Antique)
st.plotly_chart(linechart_region)

    