# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt

# Recall app
from app import app


####################################################################################
# Add Elements
####################################################################################

logo = html.Div(
    className='flex flex-1 md:w-1/3 justify-center md:justify-start text-white px-2'
)


searchBar = html.Div(
    [
        html.Span(
            [
                dcc.Input(
                    className='w-full bg-gray-800 text-sm text-white transition border border-transparent focus:outline-none focus:border-gray-700 rounded py-1 px-2 pl-10 appearance-none leading-normal',
                    placeholder='Search', type='search', id='search-bar1'
                ), html.Div(
                    [], className='absolute search-icon'
                )
            ], className='relative w-full'
        )
    ], className='flex flex-1 md:w-1/3 justify-center md:justify-start text-white px-2'
)

navLinks = html.Div(
    [
        html.Ul(
            [
                html.Li(
                    [
                        html.A(
                            'Dashboard', className='inline-block py-2 px-4 text-white no-underline')
                    ], className='flex-1 md:flex-none md:mr-3 cursor-pointer'
                ),
                html.Li(
                    [
                        html.A(
                            'Exit', href='#', className='inline-block text-gray-600 no-underline hover:text-gray-200 hover:no-underline py-2 px-4')
                    ], className='flex-1 md:flex-none md:mr-3'
                )
            ], className='list-reset flex justify-between flex-1 md:flex-none items-center mb-0'
        )
    ], className='flex w-full pt-2 content-center justify-between md:w-1/3 md:justify-end'
)


Nav = html.Nav(
    [
        html.Div([
            logo,
            searchBar,
            navLinks
        ], className='flex flex-wrap items-center')
    ], className=""
)

#############################################################################
# Sidebar Layout
#############################################################################
navBar = Nav
