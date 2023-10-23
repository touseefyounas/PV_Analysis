{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOCcaQzYTFNzBPllB4Zwwyz",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/touseefyounas/PV_Analysis/blob/main/pv_dash_app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from dash import Dash,dcc,html\n",
        "from dash.dependencies import Input, Output\n",
        "import requests\n",
        "import pandas as pd\n",
        "import plotly.express as px\n",
        "import folium\n",
        "from folium.raster_layers import ImageOverlay\n",
        "import plotly.graph_objects as go\n",
        "import dash_bootstrap_components as dbc\n",
        "from dash_bootstrap_templates import load_figure_template"
      ],
      "metadata": {
        "id": "1AI1cIlXj6d4"
      },
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "app = Dash(__name__,external_stylesheets=[dbc.themes.LUX])\n",
        "\n",
        "app.layout = html.Div([\n",
        "    html.H1('Solar Energy Data Dashboard'),\n",
        "\n",
        "    # Input field for system_capacity\n",
        "    html.Label('Nameplate Capacity (kW):'),\n",
        "    dcc.Input(id='system_capacity',type='number', value=4, min=0.05, max=500000),\n",
        "    html.Br(),\n",
        "    html.Br(),\n",
        "\n",
        "    #Radio Item Selection for the type of module i.e. Standard, Premium, Think Film\n",
        "    html.Label('Module type:'),\n",
        "    dcc.RadioItems(id='module_type',\n",
        "        options=[{'label': 'Standard', 'value':0},\n",
        "         {'label': 'Premium', 'value':1},\n",
        "          {'label': 'Thin Film', 'value':2}],value=0),\n",
        "    html.Br(),\n",
        "    html.Br(),\n",
        "\n",
        "    #Input field for system losses\n",
        "    html.Label('System Losses(%):'),\n",
        "    dcc.Input(id='system_losses',type='number',value=5,min=-5,max=100),\n",
        "    html.Br(),\n",
        "    html.Br(),\n",
        "\n",
        "html.Div([\n",
        "    #Radio Item Selection for the array_type\n",
        "    html.Label('Array Type:'),\n",
        "    dcc.Dropdown(id='array_type',options=[{'label':'Fixed - Open Rack','value':0},\n",
        "     {'label':'Fixed - Roof Mounted','value':1},{'label':'1-Axis','value':2},\n",
        "       {'label':' 1-Axis Backtracking','value':3},{'label':'2-Axis','value':4}],value=1),\n",
        "    html.Br(),\n",
        "    html.Br(),],style={'width':'25%'}),\n",
        "\n",
        "    #Slider for selecting Tilt Angle\n",
        "html.Div([\n",
        "    html.Label('Tilt Angle (0 to 90):'),\n",
        "    dcc.Slider(id='tilt_angle', value=30, min=0, max=90, step=0.5,marks={0: '0°', 45: '45°', 90: '90°'}),\n",
        "    dcc.Input(id='tilt_angle_display', type='text', readOnly=True, style={'border': 'none'}),\n",
        "    html.Br(),html.Br(),],style={'width': '30%'}),\n",
        "\n",
        "    #Slider for selecting Azimuth Angle\n",
        "html.Div([\n",
        "    html.Label('Azimuth Angle (0 to 360):'),\n",
        "    dcc.Slider(id='azimuth_angle',value=180,min=0,max=360,step=1,marks={0: '0°', 90: '90°', 180: '180°', 270: '270°', 360: '360°'}),\n",
        "    dcc.Input(id='azimuth_angle_display', type='text', readOnly=True, style={'border': 'none'}),\n",
        "    html.Br(),html.Br(),],style={'width': '30%'}),\n",
        "\n",
        "    #RadioItems for input selection\n",
        "    dcc.RadioItems(id='input-selection',\n",
        "                   options=[{'label': 'Use Address', 'value': 'address'},\n",
        "                    {'label': 'Use Latitude & Longitude', 'value': 'lat_long'}],value='lat_long'),\n",
        "    html.Br(),\n",
        "    html.Br(),\n",
        "\n",
        "    # Div for the address input section\n",
        "html.Div([\n",
        "        html.Label('Enter Address:'),\n",
        "        dcc.Input(id='address-input', type='text'),\n",
        "        html.Br(),\n",
        "        html.Br(),\n",
        "    ], id='address-section'),\n",
        "\n",
        "    # Div for the lat/long input section\n",
        "html.Div([\n",
        "    html.Label('Enter Latitude:'),\n",
        "    dcc.Input(id='lat-input', type='number', value=33.670491),\n",
        "    html.Br(),\n",
        "    html.Br(),\n",
        "    html.Label('Enter Longitude:'),\n",
        "    dcc.Input(id='long-input', type='number', value=72.995602),\n",
        "    html.Br(),\n",
        "    html.Br(),\n",
        "    ], id='lat-long-section'),\n",
        "\n",
        "#Slider for Inverter Efficiency\n",
        "html.Div([\n",
        "    html.Label('Inverter Efficiency (90% to 99.5%):'),\n",
        "    dcc.Slider(id='inv_eff', value=96, min=90, max=99.5, step=0.5,marks={90: '90%', 99.5: '99.5%'}),\n",
        "    dcc.Input(id='inv_eff_display', type='text', readOnly=True, style={'border': 'none'}),\n",
        "    html.Br(),html.Br(),],style={'width': '25%'})\n",
        "])\n",
        "\n",
        "@app.callback(\n",
        "    Output('address-section', 'style'),\n",
        "    Output('lat-long-section', 'style'),\n",
        "    Input('input-selection', 'value')\n",
        ")\n",
        "def update_input_sections(selected_option):\n",
        "    address_style = {'display': 'block' if selected_option == 'address' else 'none'}\n",
        "    lat_long_style = {'display': 'block' if selected_option == 'lat_long' else 'none'}\n",
        "    return address_style, lat_long_style\n",
        "\n",
        "@app.callback(\n",
        "    Output('tilt_angle_display', 'value'),\n",
        "    Output('azimuth_angle_display', 'value'),\n",
        "    Output('inv_eff_display','value'),\n",
        "    Input('tilt_angle','value'),\n",
        "    Input('azimuth_angle','value'),\n",
        "    Input('inv_eff','value'))\n",
        "def update_slider_value_display(tilt_value, azimuth_value, inv_value):\n",
        "    return f'Tilt Angle: {tilt_value}°', f'Azimuth Angle: {azimuth_value}°',f'Inverter Efficiency:{inv_value}%'\n",
        "\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    app.run_server(debug=True)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 672
        },
        "id": "aSqD1X7EkQ8J",
        "outputId": "64b2e935-8759-4eb3-c452-2440c78cd203"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ],
            "application/javascript": [
              "(async (port, path, width, height, cache, element) => {\n",
              "    if (!google.colab.kernel.accessAllowed && !cache) {\n",
              "      return;\n",
              "    }\n",
              "    element.appendChild(document.createTextNode(''));\n",
              "    const url = await google.colab.kernel.proxyPort(port, {cache});\n",
              "    const iframe = document.createElement('iframe');\n",
              "    iframe.src = new URL(path, url).toString();\n",
              "    iframe.height = height;\n",
              "    iframe.width = width;\n",
              "    iframe.style.border = 0;\n",
              "    iframe.allow = [\n",
              "        'accelerometer',\n",
              "        'autoplay',\n",
              "        'camera',\n",
              "        'clipboard-read',\n",
              "        'clipboard-write',\n",
              "        'gyroscope',\n",
              "        'magnetometer',\n",
              "        'microphone',\n",
              "        'serial',\n",
              "        'usb',\n",
              "        'xr-spatial-tracking',\n",
              "    ].join('; ');\n",
              "    element.appendChild(iframe);\n",
              "  })(8050, \"/\", \"100%\", 650, false, window.element)"
            ]
          },
          "metadata": {}
        }
      ]
    }
  ]
}