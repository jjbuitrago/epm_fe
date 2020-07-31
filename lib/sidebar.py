# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt

# Recall app
from app import app


####################################################################################
# Add the SideBar
####################################################################################

SideBar = html.Div(
    [

        html.Ul(
            [
                dcc.Location(id='current-url', refresh=False),
                html.Li(
                    [
                        dcc.Link(
                            [
                                html.I(
                                    className='fas fa-chart-area pr-2 md:pr-3 text-blue-600'),
                                html.Span(
                                    'Urabá', className='pb-1 md:pb-0 text-xs md:text-base text-white md:text-white block md:inline-block')
                            ], href='#uraba-section', className='block py-3 md:py-3 pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-blue-600 cursor-pointer', id='uraba-button'
                        )
                    ], className='mr-3 flex-1'
                ), html.Li(
                    [
                        dcc.Link(
                            [
                                html.I(
                                    className='fas fa-check pr-2 text-blue-600'),
                                html.Span(
                                    'Mapa', className='pb-1 md:pb-0 text-xs md:text-base text-gray-600 md:text-gray-400 block md:inline-block')
                            ], href='#map-section', className='block py-3 md:py-3 pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-gray-800 hover:border-purple-500 cursor-pointer', id='map-button'
                        )
                    ], className='mr-3 flex-1'
                ), html.Li(
                    [
                        dcc.Link(
                            [
                                html.I(
                                    className='fa fa-map pr-2 text-blue-600'),
                                html.Span(
                                    'Antioquia', className='pb-1 md:pb-0 text-xs md:text-base text-gray-600 md:text-gray-400 block md:inline-block')
                            ], href='#services-section', className='block py-3 md:py-3 pl-0 md:pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-gray-800 hover:border-red-500 cursor-pointer', id='services-button'
                        )
                    ], className='mr-3 flex-1'
                ),

            ], className='list-reset flex md:flex-col py-0 md:py-3 px-1 md:px-2 md:text-left', id='sidebar-section'
        )

    ], className=" md:w-48 content-center md:content-start text-left justify-between"
)


@app.callback(
    [Output("uraba-section", "className"),
     Output("map-section", "className"),
     Output("services-section", "className"),
     Output("uraba-button", "className"),
     Output("map-button", "className"),
     Output("services-button", "className")],
    [Input('current-url', 'hash')],
)
def toggle_sections(pathname):
    resp = ['', 'hidden', 'hidden','block py-3 md:py-3 pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-blue-600 cursor-pointer','block py-3 md:py-3 pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-gray-800 hover:border-gray-500 cursor-pointer','block py-3 md:py-3 pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-gray-800 hover:border-gray-500 cursor-pointer']
    if '#' in pathname:
        resp = []
        for i in ['uraba', 'map', 'services']:
            if i in pathname:
                resp.append('')
            else:
                resp.append('hidden')

        for sec in ['uraba', 'map', 'services']:
            if sec in pathname:
                resp.append(
                    'block py-3 md:py-3 pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-blue-600 cursor-pointer')
            else:
                resp.append(
                    'block py-3 md:py-3 pl-1 align-middle text-white no-underline hover:text-white border-b-2 border-gray-800 hover:border-gray-500 cursor-pointer')
    return resp


#############################################################################
# Sidebar Layout
#############################################################################
sidebar = html.Div(
    SideBar, className='bg-gray-900 shadow-lg h-16 bottom-0 left:0 md:h-screen z-10 w-full md:w-48'
)
