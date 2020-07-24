import pandas as pd
import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

import psycopg2

from ..sections import useful_functions as ufs


conn = psycopg2.connect(host="localhost", database='postgres',
                        user="jjbuitragoj", password="postgres")
cur = conn.cursor()
query = '''
    SELECT date_trunc('week', repairdate::date) AS weekly,
       COUNT(tasknumber)
    FROM EPM.URABA
    where repairdate is not NULL
    and town ='Turbo'
    GROUP BY weekly
    ORDER BY weekly;
'''
cur.execute(query)
rows = cur.fetchall()

uraba = pd.DataFrame(rows)

uraba.columns = ['RepairDate', 'count']

# uraba = uraba[1:]

cur.execute('''select SUBESTACI1, count(SUBESTACI1)
from epm.conectores
group by 1
ORDER BY subestaci1
ASC;''')

rows = cur.fetchall()

df_subestaciones = pd.DataFrame(rows)

df_subestaciones.columns = ['Subestacion', 'Maquinas']

fig = px.bar(df_subestaciones, x='Subestacion', y='Maquinas')
grafica = dcc.Graph(figure=fig, id='subestaciones')

linePlot = px.line(uraba[1:-1], x='RepairDate', y='count',
                   title='Numbers of repairs by week')

line_graph = dcc.Graph(figure=linePlot, id='line-plot', className='w-full')


cur.execute('''SELECT DISTINCT TOWN FROM EPM.URABA
            WHERE TOWN IS NOT NULL
            ORDER BY TOWN
            ASC;''')
rows = cur.fetchall()
distinct_towns = pd.DataFrame(rows)

towns = []
towns = list(map(ufs.norm_str, list(distinct_towns.loc[:, 0])))


def card(title, child, color='blue'):
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.I(className='fas fa-server fa-2x fa-inverse')],
                    className='rounded-full p-4 bg-{}-600'.format(color))
            ], className='flex-shrink pr-4'),
            html.Div([
                html.H5(
                    title, className='font-bold uppercase text-gray-600 text-center whitespace-no-wrap'),
                html.H3(child, className='font-bold text-3x text-center')
            ], className='flex-1 text-right md:text-center')
        ], className="flex flex-row items-center")],
        className="bg-{}-100 border-b-4 border-{}-500 rounded-lg shadow-lg p-3 mx-3".format(color, color))


dropdown = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=towns,
        value=towns[0]['label']

    )
], className='text-xl text-black w-48')


@app.callback(
    [Output("card-total", "children"),
        Output("card-realizada", "children"),
        Output("card-norealizada", "children"),
        Output("repairs-ts", "children")],
    [Input('demo-dropdown', 'value')],
)
def toggle_sections(input):
    cur.execute(
        "SELECT COUNT(*) FROM EPM.URABA WHERE TOWN='{}' AND STATUS='Realizada'".format(input))
    realizada = cur.fetchone()[0]
    cur.execute(
        "SELECT COUNT(*) FROM EPM.URABA WHERE TOWN='{}' AND STATUS='No Realizada'".format(input))
    no_realizada = cur.fetchone()[0]

    query = '''
        SELECT date_trunc('week', repairdate::date) AS weekly,
        COUNT(tasknumber)
        FROM EPM.URABA
        where repairdate is not NULL
        and town ='{}'
        GROUP BY weekly
        ORDER BY weekly;
    '''.format(input)
    cur.execute(query)
    rows = cur.fetchall()

    uraba = pd.DataFrame(rows)

    uraba.columns = ['RepairDate', 'count']

    linePlot = px.line(uraba[1:-1], x='RepairDate', y='count',
                       title='Reparaciones por semana')

    line_graph = dcc.Graph(figure=linePlot, id='line-plot', className='w-full')

    return [card('Fallas Totales', realizada+no_realizada, 'green'),
            card('Realizada', realizada, 'orange'),
            card('No Realizada', no_realizada, 'yellow'),
            line_graph]


content = html.Div(
    [
        html.Div([html.P('Urabá', className='mr-4'), dropdown],
                 className='flex bg-blue-800 p-2 shadow text-xl text-white'),
        html.Div([html.Div(id='card-total', className='w-1/3'),
                  html.Div(id='card-realizada', className='w-1/3'),
                  html.Div(id='card-norealizada', className='w-1/3'),
                  #   html.Div(card('Transformers', 800)),
                  #   html.Div(card('Insulators', 500, 'purple')),
                  #   html.Div(card('Average repair time', 90, 'red'))
                  ],
                 className='flex flex-wrap mt-2 mx-2'),
        html.Div([
            html.Div(grafica, className='w-full'),
            html.Div(className='w-full', id='repairs-ts')
        ],
            className='w-full grid grid-cols-2 gap-4 mt-2 mx-2')
    ], id='uraba-section'
)
