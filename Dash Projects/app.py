#Dash Test

#Imports
import pandas as pd
import plotly.express as px
import json

import dash
from dash import html, dcc
from dash.dependencies import Input,Output

# --- CREATE DATAFRAME --- #

#read and adapt dataframe
df = pd.read_csv('Dash Projects\data\superstore.csv',encoding='cp1252')
states = json.load(open("Dash Projects\\data\\us_states_data.json",'r'))
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
#create a state id map
state_id_map = {}
for feature in states['features']:
    feature['id'] = feature['properties']['STATE']
    state_id_map[feature['properties']['NAME']] = feature['id']
df_state = df.groupby('State').sum().reset_index()
df_state['state_id'] = df_state['State'].apply(lambda x: state_id_map[x])
# --- GENERATE TABLE --- #

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
)

# --- APP LAYOUT --- #
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Superstore | Dashboard", style={'text-align':'center'}),
    dcc.Dropdown(id='dropdown_choropleth',
                 searchable = False,
                 placeholder = 'Select Choropleth values',
                 multi = False,
                 options = ['Profit','Sales','Quantity'],
                 value = 'Profit'),
    html.Br(),
    dcc.Dropdown(id = 'dropdown_region',
                 options = [{'label': i , 'value': i} for i in df['Region'].unique()],
                 multi = False, 
                 searchable = True, 
                 clearable = True,
                 value= 'West'),
    html.Div(id = 'output_container', children = []),
    html.Br(),
    dcc.Graph(id= 'choro_map', figure = {})

])

# --- CALLBACKS --- # 

@app.callback(
    [Output(component_id='output_container', component_property = 'children'),
     Output(component_id='choro_map', component_property = 'figure')],
    [Input(component_id ='dropdown_region', component_property = 'value')]
)
def update_graph(chosen_regions):
    print(chosen_regions)
    print(type(chosen_regions))
    container = "Chosen Regions: {}".format(chosen_regions)
    dfc = df_state.copy()
    dfc = dfc[dfc['Region'] == chosen_regions]
    #plotly choromap
    fig = px.choropleth(dfc, locations = 'state_id', title = "Choropleth Map",
                        geojson = states, color = 'Profit', 
                        scope = 'usa', hover_name = 'State',
                        color_continuous_scale = px.colors.diverging.PuOr,
                        color_continuous_midpoint = 0)
    return container, [fig]

if __name__ == '__main__':
    app.run_server(debug=True)
