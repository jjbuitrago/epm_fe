import pandas as pd
import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

import psycopg2
from datetime import datetime as dt

from ..sections import useful_functions as ufs

conn = psycopg2.connect(host="localhost", database='postgres',
                        user="jjbuitragoj", password="postgres")
cur = conn.cursor()

query = 'select max(repairdate), min(repairdate) from epm.uraba;'
cur.execute(query)
rows = cur.fetchall()

start = rows[0][1]
end = rows[0][0]

datePicker = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=start,
        max_date_allowed=end,
        start_date=start.date(),
        end_date=end.date()
    ),
    html.Div(id='output-container-date-picker-range')
], className='text-center mt-2')


@ app.callback(
    [Output("town-map", "children")],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')],
)
def toggle_sections(start_date, end_date):
    if start_date > end_date:
        end_date = start_date
    query = '''
    with coor as (select cast(latitude as FLOAT)/1000000 as lat,
       cast(longitude as FLOAT)/1000000 as long,
       town, repairdate, circuit
    from epm.uraba)
    select distinct lat, long, town, circuit from coor
    where
    repairdate >'{}' and repairdate<'{}';'''.format(start_date, end_date)

    cur.execute(query)
    rows = cur.fetchall()

    coordinates = pd.DataFrame(rows)

    coordinates.columns = ['lat', 'long', 'town', 'circuit']

    fig = px.scatter_mapbox(coordinates, lat="lat", lon="long", hover_name="town",
                            color_continuous_scale="circuit", zoom=8, height=700, width=490)

    fig.update_layout(mapbox_style="carto-positron",
                      margin={"r": 20, "t": 20, "l": 20, "b": 20})

    return [dcc.Graph(figure=fig)]


content = html.Div([html.Div([datePicker, html.Div(id='town-map')],
                             className='w-1/2 px-auto',
                             id='map-section'),
                    html.Div(className=' w-1/2')
                    ], className='flex flex-wrap w-full')
