import dash
from dash.dependencies import Input, Output, State, ClientsideFunction

import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from .sections import con_pri


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd

##############################
# Map Layout
##############################
content = html.Div([con_pri.content,
                    html.Div(["This is the content of aislade"],
                             className='h-5 bg-blue-300 w-full hidden', id='aislade-section'),
                    html.Div(["This is the content of cuchill"],
                             className='h-5 bg-green-300 w-full hidden', id='cuchill-section')],
                   className='absolute top-auto ml-48', id='main-content')
