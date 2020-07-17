import pandas as pd
import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv('CON_PRI_OP.csv', sep=",", encoding="latin")
df_subestaciones = df.groupby('SUBESTACI1')['G3E_FID'].count().reset_index()

fig = px.bar(df_subestaciones, x='SUBESTACI1', y='G3E_FID')

grafica = dcc.Graph(figure=fig, id='subestaciones')

page = html.Div(grafica)


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
        className="bg-{}-100 border-b-4 border-{}-500 rounded-lg shadow-lg p-3".format(color, color))


content = html.Div(
    [
        html.Div('Recon', className='bg-blue-800 p-2 shadow text-xl text-white'),
        html.Div([html.Div(card('Total Failures', 400, 'green')),
                  html.Div(card('Repairs Made', 300, 'orange')),
                  html.Div(card('Present Failures', 10, 'yellow')),
                  html.Div(card('Transformers', 800)),
                  html.Div(card('Insulators', 500, 'purple')),
                  html.Div(card('Average repair time', 90, 'red'))],
                 className='grid grid-flow-row grid-cols-3 grid-rows-2 gap-4 mt-2 mx-2'),
        html.Div([
            html.Div(grafica, className='h-32 bg-red-400'),
        ],
            className='grid grid-flow-row grid-cols-2 grid-rows-1 gap-4 mt-2 mx-2')
    ], id='reconec-section'
)
