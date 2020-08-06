import pandas as pd
import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

import psycopg2

from ..sections import useful_functions as ufs


conn = psycopg2.connect(host="postgres.czuldxhimlqj.us-east-2.rds.amazonaws.com", database='postgres',
                        user="postgres", password="postgres")
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


def grafica_hora(town):
    if town == 'Todos' or town is None:
        cur.execute('''select  date_part('hour', repairdate) as hour, count(*) from EPM.uraba
        where repairdate is not NULL
        group by  hour''')
    else:
        cur.execute('''select  date_part('hour', repairdate) as hour, count(*) from EPM.uraba
        where repairdate is not NULL
        and town ='{}'
        group by  hour'''.format(town))

    rows = cur.fetchall()

    df_subestaciones = pd.DataFrame(rows)

    df_subestaciones.columns = ['Hora', 'Reparaciones']

    fig = px.bar(df_subestaciones, x='Hora', y='Reparaciones',
                 title='Reparaciones por hora')
    return dcc.Graph(figure=fig, id='reparaciones-hora')


cur.execute('''WITH TAB AS (SELECT DISTINCT TOWN, COUNT(*) AS CNT FROM EPM.URABA
            WHERE TOWN IS NOT NULL
            and REPAIRDATE IS NOT NULL
            GROUP BY TOWN)
            SELECT * FROM TAB WHERE CNT >500;''')
rows = cur.fetchall()
distinct_towns = pd.DataFrame(rows)

towns = []

towns = list(map(ufs.norm_str, list(distinct_towns.loc[:, 0])))
towns.insert(0, {'label': 'Todos', 'value': 'Todos'})


def card(title, child, color='blue', icon='fas fa-server'):
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.I(className='{} fa-2x fa-inverse'.format(icon))],
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
], className='text-xl text-black w-48 pr-3')


@app.callback(
    [Output("card-total", "children"),
        Output("card-realizada", "children"),
        Output("card-norealizada", "children"),
        Output("repairs-ts", "children"),
        Output("repairs-hour", "children")],
    [Input('demo-dropdown', 'value')],
)
def toggle_sections(input):

    if input == 'Todos' or input is None:
        cur.execute(
            "SELECT COUNT(*) FROM EPM.URABA WHERE STATUS='Realizada'")
        realizada = cur.fetchone()[0]
        cur.execute(
            "SELECT COUNT(*) FROM EPM.URABA WHERE STATUS='No Realizada'")
        no_realizada = cur.fetchone()[0]
    else:
        cur.execute(
            "SELECT COUNT(*) FROM EPM.URABA WHERE TOWN='{}' AND STATUS='Realizada'".format(input))
        realizada = cur.fetchone()[0]
        cur.execute(
            "SELECT COUNT(*) FROM EPM.URABA WHERE TOWN='{}' AND STATUS='No Realizada'".format(input))
        no_realizada = cur.fetchone()[0]

    if input == 'Todos' or input is None:
        query = '''
            SELECT date_trunc('week', repairdate::date) AS weekly,
            COUNT(tasknumber)
            FROM EPM.URABA
            where repairdate is not NULL
            GROUP BY weekly
            ORDER BY weekly;
        '''
    else:
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

    return [card('Fallas Totales', realizada+no_realizada, 'green', 'fa fa-wrench'),
            card('Realizada', realizada, 'orange', 'fa fa-thumbs-up'),
            card('No Realizada', no_realizada, 'yellow', 'fa fa-thumbs-down'),
            line_graph,
            grafica_hora(input)]


content = html.Div(
    [
        html.Div([html.P('Urabá', className='mb-0 font-semibold pr-3'), dropdown],
                 className='flex justify-between items-center bg-blue-800 p-2 shadow text-xl text-white'),
        html.Div([html.Div(id='card-total', className='w-1/3'),
                  html.Div(id='card-realizada', className='w-1/3'),
                  html.Div(id='card-norealizada', className='w-1/3'),
                  #   html.Div(card('Transformers', 800)),
                  #   html.Div(card('Insulators', 500, 'purple')),
                  #   html.Div(card('Average repair time', 90, 'red'))
                  ],
                 className='flex flex-wrap mt-2 mx-2'),
        html.Div([
            html.Div(className='w-full', id='repairs-hour'),
            html.Div(className='w-full', id='repairs-ts')
        ],
            className='w-full grid grid-cols-2 gap-4 mt-2 mx-2')
    ], id='uraba-section'
)
