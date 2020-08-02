import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import plotly.tools as tls
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

import psycopg2
from datetime import datetime as dt

from ..sections import useful_functions as ufs

import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf, acf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def func_proy(st, et, town, g_title, town_id, start_data_m, order_sm, seasonal_order_sm):

    conn = psycopg2.connect(host="localhost", database='postgres',
                            user="jjbuitragoj", password="postgres")
    cur = conn.cursor()
    query = '''
        SELECT date_trunc('week', repairdate::date) AS weekly,
        COUNT(tasknumber)
        FROM EPM.URABA
        where repairdate is not NULL
        and town ='{}'
        GROUP BY weekly
        ORDER BY weekly;
    '''.format(town)

    cur.execute(query)
    rows = cur.fetchall()

    uraba = pd.DataFrame(rows)[st:et]

    uraba.columns = ['RepairDate', 'count']

    uraba['RepairDate'] = uraba['RepairDate'].apply(
        lambda x: datetime.strptime(str(x).split(' ')[0], '%Y-%m-%d').date())
    uraba = uraba.set_index('RepairDate')

    mod = sm.tsa.statespace.SARIMAX(uraba,
                                    order=order_sm,
                                    seasonal_order=seasonal_order_sm,
                                    enforce_stationarity=True,
                                    enforce_invertibility=True)

    results = mod.fit()

    pred = results.get_prediction(start=pd.to_datetime(
        start_data_m), end=pd.to_datetime("2020-03-31"), dynamic=False)
    pred_summary = pred.summary_frame()

    turbo_df_proy = pd.DataFrame(
        pred_summary[['mean', 'mean_ci_lower', 'mean_ci_upper']]).reset_index()

    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Scatter(x=uraba.index.tolist(), y=uraba['count'].tolist()),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=turbo_df_proy['index'].tolist(),
                   y=turbo_df_proy['mean_ci_lower'].tolist(), mode='lines',
                   fillcolor='rgb(200, 200, 200)', line_color="rgb(200, 200, 200)"),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=turbo_df_proy['index'].tolist(),
                   y=turbo_df_proy['mean_ci_upper'].tolist(), mode='lines',
                   fillcolor='rgb(200, 200, 200)', fill='tonextx', line_color="rgb(200, 200, 200)"), row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=turbo_df_proy['index'].tolist(),
                   y=turbo_df_proy['mean'].tolist(), mode='lines', line_color="#444"),

        row=1, col=1
    )

    fig.update_layout(
        title_text=g_title)

    return dcc.Graph(figure=fig, id='line-plot-'+town_id, className='w-full')


content = html.Div(
    [
        func_proy(1, -1,
                  'Turbo', "Pronósticos de enero a junio de 2020 para Turbo", 'turbo', '2020-01-01', (0, 1, 1), (0, 1, 0, 26)),
        func_proy(1, -1,
                  'Necoclí', "Pronósticos de enero a junio de 2020 para Necoclí", 'necocli', '2020-01-12', (1, 1, 0), (0, 1, 0, 24)),
        func_proy(0, 52,
                  'Apartadó', "Pronósticos de enero a junio de 2020 para Apartadó", 'apartado', '2020-01-12', (1, 1, 0), (0, 1, 0, 24)),
        func_proy(0, 52,
                  'Carepa', "Pronósticos de enero a junio de 2020 para Carepa", 'carepa', '2020-01-06', (1, 1, 0), (0, 1, 0, 25)),
        func_proy(0, 52,
                  'San pedro de urabá', "Pronósticos de enero a junio de 2020 para San Pedro de Urabá", 'san-pedro', '2020-01-06', (0, 1, 1), (0, 1, 0, 26)),
        func_proy(0, 52,
                  'Chigorodó', "Pronósticos de enero a junio de 2020 para Chigorodó", 'chigorodo', '2020-01-12', (0, 1, 1), (0, 1, 0, 26)),

    ], className='flex flex-wrap w-full', id='map-section')
