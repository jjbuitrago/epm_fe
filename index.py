# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

# Recall app
from app import app

###########################################################
#
#           APP LAYOUT:
#
###########################################################

# LOAD THE DIFFERENT FILES
from lib import sidebar, navBar, content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


# PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(

    [
        html.Div(
            navBar.navBar, className="w-1 bg-gray-900 pt-2 md:pt-1 pb-1 px-1 mt-0 h-auto w-full z-20 top-0", id="nav-bar"
        ),
        html.Div(
            [
                html.Div(sidebar.sidebar, className='float-left w'),
                html.Div(content.content, className='w-100', id='content-section')], className='flex flow-row', id="document-body"
        )

    ], className=''
)


###############################################
#
#           APP INTERACTIVITY:
#
###############################################
if __name__ == "__main__":
    app.run_server(debug=True)
