### Streamlit webpage

#Imports
from doctest import DocFileSuite
from string import hexdigits
from turtle import heading, right

import streamlit as st
from streamlit_lottie import st_lottie
import requests
import plotly.express as px

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as pxrun
import plotly.io as pio
import json

import os
import sys

#Page config
st.set_page_config(page_title = "Renewable Energy", page_icon=":world_map:", layout = 'wide')

### --- Project X - Superstore Analysis and Dashboard --- ###
with st.container():
    st.subheader("Project XII - Renewable Energy in World")
    st.write('---')

# --- DATAFRAMES --- #
#Choose File
st.sidebar.title('Options')
df_file = st.sidebar.file_uploader('Choose a File','csv')
#df = pd.read_csv('Streamlit Projects\project_energy\data\share-electricity-wind.csv')
df = pd.read_csv(df_file)
year = df['Year'].unique().tolist()
countries_features = json.load(open("Streamlit Projects\\project_energy\\data\\world.json",'r'))
countries_geojson = json.load(open("Streamlit Projects\\project_energy\\data\\countries.geo.json",'r'))

#read and adapt dataframe
with st.container():
    #maps 
    cont_map = {}
    sub_map = {}

    for feature in countries_features['features']:
        feature['continent'] = feature['properties']['continent']
        feature['subregion'] = feature['properties']['subregion']
        cont_map[feature['properties']['adm0_a3_is']] = feature['continent']
        sub_map[feature['properties']['adm0_a3_is']] = feature['subregion']  

    #Drop Nulls
    df.dropna(inplace = True,subset='Code')
    #Drop World and USSR
    df = df[df['Code'] != 'OWID_WRL']
    df = df[df['Code'] != 'OWID_USS']
    #Replace French UMT
    df['Code'].replace('GUF','FRA',inplace = True)
    df['Code'].replace('GLP','FRA',inplace = True)
    df['Code'].replace('MTQ','FRA',inplace = True)
    df['Code'].replace('REU','FRA',inplace = True)
    #Replace Kosovo
    df['Code'].replace('OWID_KOS','SRB',inplace = True)
    #Make Columns
    df['Continent'] = df['Code'].apply(lambda x: cont_map[x])
    df['Subregion'] = df['Code'].apply(lambda x: sub_map[x])

# --- SIDEBAR --- #
with st.container():
    #Choose Column  
    choro_column = st.sidebar.selectbox('Choose Column',df.columns.tolist()[3:-2])
    #Form Slider
    with st.container():    #Year Selection
        year_selection = st.sidebar.slider('Years',
                                        min_value = min(year),
                                        max_value = max(year),
                                        value = (min(year),max(year)))
    split_option = st.sidebar.radio("Selections",['Continent','Subregion','Entity'])
    #region_selection = st.sidebar.multiselect("Region", region, default = region)
    split_selection = st.sidebar.multiselect(split_option, df[split_option].unique().tolist(), default = df[split_option].unique().tolist())
    #country_selection = st.sidebar.multiselect("Category", category, default = category)

mask = (df['Year'].between(*year_selection)) & (df[split_option].isin(split_selection))
df_dash = df[mask]

#UPPER VALUES
with st.container():
    column1, column2 = st.columns([2,1])
    with column1:
        #create map fig
        choro_map = px.choropleth(df_dash, locations = 'Code',
                                  geojson = countries_geojson, color = df_dash[choro_column], 
                                  scope = 'world', hover_name = 'Entity',
                                  color_discrete_sequence= px.colors.sequential.Plasma_r,
                                  width=950, height=500)
        st.plotly_chart(choro_map)
    with column2:
        #pie chart
        #Make a new df with concat 'others' value.
        with st.container():
                df_pie = df_dash.groupby('Entity').sum().reset_index().sort_values(choro_column, ascending = False)
                df1 = df_pie[df_pie['Entity'].isin(df_pie['Entity'].iloc[:10].to_list())]
                df2 = df_pie[df_pie['Entity'].isin(df_pie['Entity'].iloc[10:].to_list())]
                df2['Entity'] = 'Others'
                df2 = df2.groupby('Entity').sum().reset_index()
                df_pie = pd.concat([df1, df2])
        #pie Chart
        st.subheader('Total Production')
        pie_category = px.pie(df_pie, values = df_pie[choro_column], 
                names = "Entity", width = 500, height = 500,
                color_discrete_sequence=px.colors.qualitative.Antique)
        pie_category.update_traces(textposition='inside')
        pie_category.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        st.plotly_chart(pie_category)

with st.container():
    column1, column2 = st.columns([1,1])
    st.write('---')
    with column1:
        #top 5 histogram
        st.subheader('Production by Year')
        df_get_top5 = df_dash.groupby(['Entity','Year']).sum().reset_index().sort_values(['Year', choro_column], ascending=False)
        top5_mask = df_dash[df_dash['Entity'].isin(df_get_top5['Entity'].iloc[:5].to_list())]
        df_top5 = top5_mask.groupby(['Entity','Year']).sum().reset_index()
        line_top5 = px.line(df_top5, x='Year', y = df_top5[choro_column], 
                            color = 'Entity', height = 300,
                            color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(line_top5)
