### Streamlit webpage

#Imports
from ctypes import alignment
from locale import currency
from string import hexdigits
from turtle import heading, right

import streamlit as st
from streamlit_lottie import st_lottie

import pandas as pd
import plotly.express as px
import json

#Page config
st.set_page_config(page_title = "Superstore | Dashboard", page_icon=":bar_chart:", layout = 'wide')

### --- Project X - Superstore Analysis and Dashboard --- ###
with st.container():
    st.subheader("Project X - Superstore Analysis and Dashboard")

#read and adapt dataframe
with st.container():
    df = pd.read_csv('C:\Portfolio & Projects\Streamlit Projects\streamlit_multipage\pages\data\superstore.csv',encoding='cp1252')
    states = json.load(open("Streamlit Projects\\streamlit_multipage\\pages\\data\\us_states_data.json",'r'))
    #change to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    #create a new column showing if it was proftable
    for i in df['Profit']:
        if i > 0:
            df['Profitable'] = df['Profit'] > 0
    #Region Dataset
    df_region = df.groupby(['Order Date','Region']).sum().reset_index()
    #Segment Dataset
    df_seg = df.groupby(['Order Date','Segment']).sum().reset_index()
    #Category Dataset
    df_cat = df.groupby(['Order Date','Category']).sum().reset_index()
    # CREATE MASKS
    #Region Masks
    region = df['Region'].unique().tolist()
    segment = df['Segment'].unique().tolist()
    category = df['Category'].unique().tolist()
    profit = df['Profit'].unique().tolist()

# --- SIDEBAR --- #
with st.container():
    st.sidebar.title('Options')  
    #Form Slider
    with st.container():    #Profit Selection
        profit_selection = st.sidebar.slider('Profit',
                                        min_value = min(profit),
                                        max_value = max(profit),
                                        value = (min(profit),max(profit)))
    region_selection = st.sidebar.multiselect("Region", region, default = region)
    segment_selection = st.sidebar.multiselect("Segment", segment, default = segment)
    category_selection = st.sidebar.multiselect("Category", category, default = category)
    with st.container():        #calendar
        date_start = st.sidebar.date_input('From', value = df['Order Date'].min(), 
                    min_value = df['Order Date'].min(), max_value=df['Order Date'].max())
        date_end = st.sidebar.date_input('To', value = df['Order Date'].max(), 
                    min_value= df ['Order Date'].min(), max_value=df['Order Date'].max())
        #convert to datetime
        date_start = pd.to_datetime(date_start)
        date_end = pd.to_datetime(date_end)

# --- RESULT DATAFRAME --- #
with st.container():
    mask = (df['Order Date'].between(date_start,date_end)) & (df['Profit'].between(*profit_selection)) & (df['Region'].isin(region_selection)) & (df['Segment'].isin(segment_selection)) & (df['Category'].isin(category_selection))
    #number of entities in results
    n_results = df[mask].shape[0]
    #df for dashboard
    df_dash = df[mask]

# --- UPPER VALUES --- #
with st.container():
    st.write("---")
    column1, column2, column3, column4 = st.columns(4)
    with column1:   
        st.metric('Quantity',  df_dash['Quantity'].sum(), round(df_dash['Quantity'].mean(), 0))  
    with column2:   
        st.metric('Profit', '${:,.2f}'.format(df_dash['Profit'].sum()),
                '${:,.2f}'.format(df_dash['Profit'].mean()))
    with column3:   
        st.metric('Sales', '${:,.2f}'.format(df_dash['Sales'].sum()),
                '${:,.2f}'.format(df_dash['Sales'].mean()))
    with column4:   
        st.metric('Profitable',"{:,.2%}".format(df_dash['Profitable'].mean()))

# --- MID VALUES --- #
with st.container():
    st.markdown(f'*Number of Results: {n_results}*')
    #Select map type
    choro_select = st.selectbox("",['Profit','Sales','Quantity'])
    column1, column2 = st.columns([2,1])
    with column1:
        #create a state id map
        state_id_map = {}
        for feature in states['features']:
            feature['id'] = feature['properties']['STATE']
            state_id_map[feature['properties']['NAME']] = feature['id']
        df_state = df_dash.groupby('State').sum().reset_index()
        #apply mapping to df
        df_state['state_id'] = df_state['State'].apply(lambda x: state_id_map[x])
        #create map fig
        choro_map = px.choropleth(df_state, locations = 'state_id', title = "Choropleth Map",
                            geojson = states, color = choro_select, 
                            scope = 'usa', hover_name = 'State',
                        color_continuous_scale = px.colors.diverging.PuOr,
                        color_continuous_midpoint = 0, width=950, height=500)
        st.plotly_chart(choro_map)
    with column2:
        #piechart
        pie_profitable = px.pie(df_dash, values = df_dash['Row ID'], title = "Profit Ratio",
                        names = 'Profitable', width = 400, height = 500,
                        color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(pie_profitable)

# --- LOW VALUES --- #
with st.container():
    st.write('---')
    column1, column2 = st.columns([2,1])
    with column1:      #LINE VALUES
        #REGION PLOT
        st.write('Region Historical Data')
        df_region = df_dash.groupby(['Order Date','Region']).sum().reset_index()
        linechart_region = px.line(df_region, x='Order Date', y="Profit",
                                color = 'Region', width = 950, height = 250,
                                color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(linechart_region)
        #SEGMENT PLOT
        st.write('Segment Historical Data')
        df_seg = df_dash.groupby(['Order Date','Segment']).sum().reset_index()
        linechart_seg = px.line(df_seg, x='Order Date', y="Profit",
                                color = 'Segment', width = 950, height = 250,
                                color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(linechart_seg)
        #CATEGORY PLOT
        st.write('Category Historical Data')
        df_cat = df_dash.groupby(['Order Date','Category']).sum().reset_index()
        linechart_cat = px.line(df_cat, x='Order Date', y="Profit",
                                color = 'Category', width = 950, height = 250,
                                color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(linechart_cat)
    with column2:      #PIE VALUES
        st.write('Profit by Region')
        pie_region = px.pie(df_dash, values = "Profit",
                        names = 'Region', width = 400, height = 250,
                        color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(pie_region)
        st.write('Profit by Segment')
        pie_segment = px.pie(df_dash, values = "Profit", 
                        names = "Segment", width = 400, height = 250,
                        color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(pie_segment)
        st.write('Profit by Category')
        pie_category = px.pie(df_dash, values = "Profit", 
                names = "Category", width = 400, height = 250,
                color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(pie_category)