import pandas as pd
import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html
import psycopg2

# # # conn = psycopg2.connect(host="localhost", database='postgres',
# # #                         user="jjbuitragoj", password="postgres")
# # # cur = conn.cursor()
# # # cur.execute(
# # #     'SELECT RepairDate, Town, callid FROM epm.uraba where repairDate is not NULL')
# # # rows = cur.fetchall()

# # # uraba = pd.DataFrame(rows)
# # # uraba.columns = ['RepairDate', 'town', 'callid']
# # # uraba = uraba[1:]

# # # cur.execute('SELECT SUBESTACI1, G3E_FID FROM epm.conectores')
# # # rows = cur.fetchall()

# # # df = pd.DataFrame(rows)
# # # df.columns = df.loc[0, :]
# # # df = df[1:]

# # # df_subestaciones = df.groupby('SUBESTACI1')['G3E_FID'].count().reset_index()
# # # print(uraba)
# # # uraba['RepairDate'] = pd.datetime(uraba['RepairDate'], '%Y-%m-%d %H:%m:%s')
# # # # Data Frame Uraba
# # # town = 'Turbo'

# # # town_ts = uraba[uraba['town'] == town].groupby(pd.Grouper(
# # #     key='RepairDate', freq='W-MON')).count()['CallID'].reset_index()
# # # town_ts.columns = ['RepairData', 'Services']
# # # line_plot = px.line(town_ts, x='Services', y='RepairData',
# # #                     title='Life expectancy in Canada')


# # # fig = px.bar(df_subestaciones, x='SUBESTACI1', y='G3E_FID')


# def grafica(ix):
#     return dcc.Graph(figure=fig, id='subestaciones_' + str(ix))

#page = html.Div(grafica)

# df = pd.read_excel('report_uraba.xlsx', encoding='utf-8')


# towns = [{'label': str(x), 'value': str(x).replace(' ', '_').lower()} for x in list(df['town'].unique())]
towns = [{'label': 'Carepa', 'value': 'carepa'}, {'label': 'Turbo', 'value': 'turbo'}, {'label': 'Necoclí', 'value': 'necoclí'}, {'label': 'San pedro de urabá', 'value': 'san_pedro_de_urabá'}, {'label': 'nan', 'value': 'nan'}, {'label': 'Nueva Colonia', 'value': 'nueva_colonia'}, {'label': 'Apartadó', 'value': 'apartadó'}, {'label': 'Arboletes', 'value': 'arboletes'}, {'label': 'Chigorodó', 'value': 'chigorodó'}, {'label': 'San juan de urabá', 'value': 'san_juan_de_urabá'}, {'label': 'La Atoyosa', 'value': 'la_atoyosa'}, {'label': 'Currulao', 'value': 'currulao'}, {'label': 'Mutatá', 'value': 'mutatá'}, {'label': 'Riosucio', 'value': 'riosucio'}, {'label': 'Belen de Bajira', 'value': 'belen_de_bajira'}, {'label': 'San Pedro De Los Milagros', 'value': 'san_pedro_de_los_milagros'}, {'label': 'Anzá', 'value': 'anzá'}, {'label': 'Nechí', 'value': 'nechí'}, {'label': 'Medellín', 'value': 'medellín'}, {
    'label': 'San Vicente Ferrer', 'value': 'san_vicente_ferrer'}, {'label': 'La estrella', 'value': 'la_estrella'}, {'label': 'Murindó', 'value': 'murindó'}, {'label': 'Segovia', 'value': 'segovia'}, {'label': 'Caucasia', 'value': 'caucasia'}, {'label': 'San José De La Montaña', 'value': 'san_josé_de_la_montaña'}, {'label': 'Anorí', 'value': 'anorí'}, {'label': 'Carolina', 'value': 'carolina'}, {'label': 'Nariño', 'value': 'nariño'}, {'label': 'El Carmen De Viboral', 'value': 'el_carmen_de_viboral'}, {'label': 'Caramanta', 'value': 'caramanta'}, {'label': 'Cisneros', 'value': 'cisneros'}, {'label': 'Bello', 'value': 'bello'}, {'label': 'Olaya', 'value': 'olaya'}, {'label': 'San Luis', 'value': 'san_luis'}, {'label': 'Cañasgordas', 'value': 'cañasgordas'}, {'label': 'Caicedo', 'value': 'caicedo'}, {'label': 'Ciudad bolívar', 'value': 'ciudad_bolívar'}, {'label': 'San Jerónimo', 'value': 'san_jerónimo'}]


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


dropdown = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=towns,
        value='NYC'
    )
], className='text-xl text-black w-48')

content = html.Div(
    [
        html.Div([html.P('Uraba', className='mr-4'), dropdown],
                 className='flex bg-blue-800 p-2 shadow text-xl text-white'),
        html.Div([html.Div(card('Total Failures', 400, 'green')),
                  html.Div(card('Repairs Made', 300, 'orange')),
                  html.Div(card('Present Failures', 10, 'yellow')),
                  html.Div(card('Transformers', 800)),
                  html.Div(card('Insulators', 500, 'purple')),
                  html.Div(card('Average repair time', 90, 'red'))],
                 className='grid grid-flow-row grid-cols-3 grid-rows-2 gap-4 mt-2 mx-2'),
        html.Div([
            # html.Div(grafica(1), className='h-32 bg-red-400'),
            # html.Div(line_plot, className='h-32 bg-red-400')
        ],
            className='grid grid-flow-row grid-cols-2 grid-rows-1 gap-4 mt-2 mx-2')
    ], id='uraba-section'
)
