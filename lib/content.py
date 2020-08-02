import dash
from dash.dependencies import Input, Output, State, ClientsideFunction

import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from .sections import section_1, section_3, antioquia_map


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd
import os

from app import app

bf_img = 'BEFORE REMOVING STOPWORDS.JPG'
af_img = 'AFTER REMOVING STOPWORDS-J.JPG'
non_sig_im = 'removing recurrent non-significant words.JPG'


def create_img(title, image):
    return html.Div(
        [html.P(title, className='text-center text-xl font-semibold my-3 text-blue-900'),
         html.Img(src=app.get_asset_url(image),
                  className='mx-auto', width='450')
         ], className='w-1/2'
    )


wordcloud = html.Div([create_img('Before removing words', bf_img),
                      create_img(
    'After removing words', af_img),
    create_img(
    'After removing recurrent non-significant words', non_sig_im)
], className='flex flex-wrap')

##############################
# Map Layout
##############################
content = html.Div([section_1.content,
                    html.Div(antioquia_map.map,
                             className='h-5 bg-blue-300 w-full hidden', id='services-section'),
                    html.Div(wordcloud,
                             className='h-5 bg-blue-300 w-full hidden', id='wordcloud-section'),
                    section_3.content
                    ],
                   className='overflow-x-hidden', id='main-content')
