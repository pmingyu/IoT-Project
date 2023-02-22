import dash
from dash.dependencies import Input, Output
from dash import dcc as dcc
from dash import html as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

datamart = pd.read_csv("../data/datamart.csv")
datamart.loc[(datamart.CLUSTER == 0), 'CLUSTER']='CLUSTER1'
datamart.loc[(datamart.CLUSTER == 1), 'CLUSTER']='CLUSTER2'
datamart.loc[(datamart.CLUSTER == 2), 'CLUSTER']='CLUSTER3'
datamart.loc[(datamart.CLUSTER == 3), 'CLUSTER']='CLUSTER4'
datamart.loc[(datamart.CLUSTER == 4), 'CLUSTER']='CLUSTER5'

shap_list = ['ME1_CYL_PCO_OUTLET_TEMP',
                       'ME1_TC2_LO_INLET_PRESS',
                       'ME1_LO_INLET_TEMP',
                       'ME1_TC1_RPM',
                       'ME1_TC1_LO_INLET_PRESS',
                       'ME1_JCW_INLET_TEMP',
                       'ME1_TC1_LO_OUTLET_TEMP',
                       'ME1_FOC',
                       'ME1_SHAFT_THRUST',
                       'ME1_POWER',
                       'ME1_FO_INLET_PRESS',
                       'ME1_SHAFT_TORQUE',
                       'ME1_TC2_LO_OUTLET_TEMP',
                       'ME1_THRUST_PAD_TEMP',
                       'ME1_RPM_SHAFT',
                       'ME1_SHAFT_POWER',
                       'ME1_JCW_INLET_PRESS',
                       'ME1_LOAD',
                       'ME1_SCAV_AIR_PRESS', 'SPEED_VG', 'ME1_RPM']

pil_image = Image.open('./cluster_img.001.jpeg')

app.layout = html.Div([
    html.Div([
        html.H1('IoT 2조', style={'backgroundColor':'#16103a', 'text-align': 'center', 'color':'white'} ),
        html.Iframe(id = 'folium', srcDoc=open('folium_v3.html', 'r').read(), width='80%', height='600', style={'margin-left':'160px'})
    ]),
    html.Div([
        html.Img(src=pil_image,width='80%', style={'margin-left':'163px', 'backgroundColor':'#16103a'} )
    ]),
    html.Div([
        dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': i, 'value': i} for i in shap_list],
        value='SPEED_VG', 
        style={'backgroundColor':'lightgray', 'color':'#16103a'}
    ),
    dcc.Graph(id='my-graph')
    ], style={'width': '100%', 'backgroundColor':'#16103a', 'color':'gray'}),
], style={'width': '100%', 'backgroundColor':'#16103a'})

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    line_fig = px.line(x=datamart.TIME_STAMP, y = datamart[selected_dropdown_value])
    line_fig.data[0].line.width = 1
    scatter_fig = px.scatter(data_frame=datamart, x=datamart.TIME_STAMP, y=datamart[selected_dropdown_value], 
                             color = 'CLUSTER',symbol='CLUSTER', opacity = 0.8,labels={"CLUSTER": "CLUSTER"})
    scatter_fig.update_traces(marker_size=5)
    fig3 = go.Figure(data=line_fig.data + scatter_fig.data)
    fig3.update_layout(paper_bgcolor="#16103a", font_color="white",)
    return fig3
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig)
# ])


if __name__ == '__main__':
    app.run_server(debug=True)
