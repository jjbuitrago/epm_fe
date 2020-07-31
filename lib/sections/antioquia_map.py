'''
paulguzcas
'''
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import psycopg2


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd
import geopandas as gpd

from app import app
from . import useful_functions as usf
# import useful_functions as usf

# Recall app
# from app import app
###########################################################
#
#           Reading Loading info:
#
###########################################################

'''
Function to create dummi variables equal to 0 for the 
municipios that do not exist in the df
'''
def complete_mpio_geo(df):
    map_date = shape_MPIO.merge(df,
                             how='left',
                             on='MPIO_CCNCT').fillna(0)
    return map_date

'''
Function to retrieve queries from DB 
in a pd.DataFrame() with variable names in the columns
'''
def fetch_query_df(conn,query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    cols = [i[0] for i in cur.description]
    return pd.DataFrame(rows,columns = cols)

'''
Function to retur a map figure of Antiquia Municipios with variables
min_date: mínimum Repair date of the incidents to show
max_date: maximum Repair date of the incidents to show
priority_range: value of the priorities of the incidents to be shown
'''
def paint_map_antioquia(min_date,max_date,priority_range,town_value):

    #If priority range is more than 0 take into account the query filter
    #if not return empty string 
    if len(priority_range)>0:
        pri_range = ','.join(["'"+str(x)+"'" for x in priority_range]) #comma separated values for DB query
        query_priority = '''and priority in ({})'''.format(pri_range)
    else:
        query_priority = ''

    #Town query creation
    if (town_value == 'Todos') | (len(town_value) == 0):
        query_town = ''
    else:
        query_town = "and town = '{}'".format(town_value)

    query = '''select
                    town,
                    count(1) as cantidad
                from
                    epm.uraba u
                where
                    repairdate::date between to_timestamp('{}','YYYY-MM-DD') and to_timestamp('{}','YYYY-MM-DD')
                {} 
                {} 
                group by 
                    town;'''.format(min_date,max_date,query_priority,query_town)

    grp = fetch_query_df(conn,query)

    # Normalization of town names to join with information
    grp['town_join'] = grp['town'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper()
    #match to obtain keys to the geojson
    grp = grp.merge(shape_MPIO[['MPIO_CNMBR','MPIO_CCNCT']]
                    ,how = 'inner'
                    ,left_on = 'town_join'
                    ,right_on = 'MPIO_CNMBR').drop(columns=['MPIO_CNMBR'])


    #Create dummy variables
    map_data = complete_mpio_geo(grp)

    #Create map figure
    Map_Fig = px.choropleth(map_data, 
                        geojson=antioquia_mpio_json, 
                        color="cantidad",
                        locations="MPIO_CCNCT", 
                        featureidkey="properties.MPIO_CCNCT",
                        center={"lat": 6.2624, "lon": -75.7638},
                        projection="mercator",
                        color_continuous_scale=px.colors.sequential.BuGn

                    )
    
    #Cosmetic map manipulations
    Map_Fig.update_layout(title='Mapa Antioquia', paper_bgcolor="#F8F9F9")
    Map_Fig.update_geos(fitbounds="locations", visible=True)
    Map_Fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return Map_Fig


'''
Function to create the figure of parallel cagegories maps 

df: dataframe of the informateion to be plotted
'''
def paint_prll_categ(df):

    fig = px.parallel_categories(df, dimensions=["priority",'servicetype', 'servicegroup'],color='priority'
                        ,color_continuous_scale=px.colors.qualitative.Plotly)

    fig.update(layout_coloraxis_showscale=False)

    return fig


'''
Function to create parallel cagegories maps 

df: dataframe of the informateion to be plotted
'''
def paint_time_boxes(df):
    
    #Create dummy variables if the dataframe is empty
    if len(df)==0:
        df = pd.DataFrame({'duratiomin':[0],
        'priority':[0],
        'travel_to_onsite':[0],
        'open_to_completion':[0]})
    
    #creating boxplots
    duration = px.box(df,y='duratiomin',x='priority',color='priority',log_y=True)

    travel = px.box(df,y='travel_to_onsite',x='priority',color='priority',log_y=True)

    open_to_completion = px.box(df,y='open_to_completion',x='priority',color='priority',log_y=True)


    return duration,travel,open_to_completion

'''
    Function to group functions and painting actions 
    min_date: mínimum Repair date of the incidents to show
    max_date: maximum Repair date of the incidents to show
    priority_range: value of the priorities of the incidents to be shown
'''
def paint_descriptive_graphs(min_date,max_date,priority_range,town_value):
    
    #Create variable for priority range if exists create condition
    #if not return empty value to avoid crashing
    if len(priority_range)>0:
        pri_range = ','.join(["'"+str(x)+"'" for x in priority_range]) #comma separated values for DB query
        query_priority = '''and priority in ({})'''.format(pri_range)
    else:
        query_priority = ''

    #Town query creation
    if (town_value == 'Todos') | (len(town_value) == 0):
        query_town = ''
    else:
        query_town = "and town = '{}'".format(town_value)

    query = '''select
            callid
            ,priority
            ,Servicetype
            ,Servicegroup
            ,duratiomin
            ,EXTRACT(epoch from (to_timestamp(onsitedate,'YYYY-MM-DD HH24:mi') - to_timestamp(traveldate,'YYYY-MM-DD HH24:mi')) )/60 as travel_to_onsite
            ,EXTRACT(epoch from (to_timestamp(completiondate,'YYYY-MM-DD HH24:mi') - to_timestamp(opendate,'YYYY-MM-DD HH24:mi')) )/60 as open_to_completion

        from
            epm.uraba
        where
            repairdate::date
            between 
                to_timestamp('{}','YYYY-MM-DD') 
            and to_timestamp('{}','YYYY-MM-DD')
            {} 
            {} 
        ;'''.format(min_date,max_date,query_priority,query_town)


    #Queried information transformations
    epm_filtered = fetch_query_df(conn,query)
    epm_filtered['priority'] = epm_filtered['priority'].astype(int)
    epm_filtered['duratiomin'] = epm_filtered['duratiomin'].astype(int)


    #Function calls
    prll_categ = paint_prll_categ(epm_filtered)

    duration_box,travel_box,open2completion_box = paint_time_boxes(epm_filtered)
    
    return prll_categ,duration_box,travel_box,open2completion_box


# Server conection 
conn = psycopg2.connect(host="localhost", database='postgres',
                        user="jjbuitragoj", password="postgres")


#Gather Dates

query = '''SELECT MIN(repairdate::date) as min FROM epm.uraba
            WHERE repairdate::date <= now();'''
min_date = fetch_query_df(conn,query)['min'].values[0]

query = '''SELECT MAX(repairdate::date) as max FROM epm.uraba 
            WHERE repairdate::date <= now();'''
max_date = fetch_query_df(conn,query)['max'].values[0]

#Gather Shapes for mapfigures

query = '''SELECT file from epm.geo_shapes WHERE nombre = 'MUNICIPIOS' '''
antioquia_mpio_json = json.loads(fetch_query_df(conn,query)['file'].values[0])

rows = []

# create Shape_MPIO variable, wich helso to associate map keys to queried data
for i in np.arange(0,len(antioquia_mpio_json['features'])):
    
    rows.append(pd.DataFrame.from_dict(antioquia_mpio_json['features'][i]['properties'],orient='index').T[['MPIO_CNMBR','MPIO_CCNCT']])
    
shape_MPIO = pd.concat(rows).reset_index().drop(columns='index')

#i really dont know why i did this.
selected_min_date = min_date
selected_max_date = max_date

# Gather priority - Initialization
priority_range = np.arange(1,10)
dict_priority = [{'label' : y, 'value':x} for x,y in zip(priority_range,priority_range)]

priority_dropdown = dcc.Dropdown(
                        id = 'piority_dropdown',
                        options=dict_priority,
                        value=priority_range,
                        multi=True
                    )  
#Dropdown Towns
query = '''select town from epm.uraba u where town is not null group by town'''
towns = fetch_query_df(conn,query)['town'].values

dict_towns = [{'label' : y, 'value':x} for x,y in zip(towns,towns)]
dict_towns.append({'label':'Todos','value':'Todos'})

town_dropdown = html.Div([
    dcc.Dropdown(
        id='town_dropdown',
        options=dict_towns,
        value=dict_towns[-1]['value']

    )
    ], className='text-xl text-black w-48 pr-3')

#Create Map

Map_Fig = paint_map_antioquia(min_date,max_date,priority_range,dict_towns[-1]['value'])

#create datepicker
date_picker=dcc.DatePickerRange(
                id='date_picker',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=min_date,
                end_date=max_date,
                initial_visible_month=selected_max_date
            )




#Create descriptive figures
prll_categ,duration_box,travel_box,open2completion_box = paint_descriptive_graphs(min_date,max_date,priority_range,dict_towns[-1]['value'])



##############################
# Map Layout
##############################
map = html.Div([
    dcc.Graph(figure=Map_Fig, id='ant_map')
    ,html.Div([date_picker])
    ,html.Div([priority_dropdown])
    ,html.Div([town_dropdown])
    ,dcc.Graph(figure=prll_categ, id='prll_categ')
    ,html.Div([
            dcc.Graph(figure=duration_box, id='duration_box')
            ,dcc.Graph(figure=travel_box, id='travel_box')
            ,dcc.Graph(figure=open2completion_box, id='open_to_completion_box')
            ])
    ],
    className="ds4a-body")



##############################
# Callbacks
##############################
@app.callback(
    [Output("ant_map", "figure"),
    Output("prll_categ","figure"),
    Output("duration_box","figure"),
    Output("travel_box","figure"),
    Output("open_to_completion_box","figure")
    ],
    [
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
        Input("piority_dropdown", "value"),
        Input("town_dropdown","value")
    ],
)
def update_figs_date(start_date,end_date,value_p,value_t):
    global selected_min_date,selected_max_date

    sel_priorities=value_p
    town_value = value_t
    
    selected_min_date = start_date
    selected_max_date = end_date
    
    Map_Fig = paint_map_antioquia(start_date,end_date,sel_priorities,town_value)


    prll_categ,duration_box,travel_box,open2completion_box = paint_descriptive_graphs(start_date,end_date,sel_priorities,town_value)

    return [Map_Fig,prll_categ,duration_box,travel_box,open2completion_box]


