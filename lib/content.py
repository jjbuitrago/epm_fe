import dash
from dash.dependencies import Input, Output, State, ClientsideFunction

import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from .sections import section_1, section_3


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd

##############################
# Map Layout
##############################
content = html.Div([section_1.content,
                    html.Div(["This is the content of aislade"],
                             className='h-5 bg-blue-300 w-full hidden', id='services-section'),
                    section_3.content
                    ],
                   className='container px-0', id='main-content')
