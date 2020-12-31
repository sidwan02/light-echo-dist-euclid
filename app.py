# import os

# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# code taken from 6_dash_UI_BLC_incid_and_dist.py

import math
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output
# import dash_auth

# BLC stands for Broad Line Cloud

# username and password pairs
# USERNAME_PASSWORD_PAIRS = [['light-echoes', 'AGNBLC']]

# create the application
app = dash.Dash()

# create the server
light_echo_dist_euclid = app.server

# create dash authorization
# auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

# create the app layout
app.layout = html.Div([

    html.Div([


        html.H3('r (Radial Position from the AGN):'),

        # r = input box of any positive number
        dcc.Input(
            id='r_input',
            placeholder='Enter a number',
            type='number',
            min=1e-100,
            value=2,
            style=dict(
                height='20px',
                marginTop='30px',
                marginLeft='20px',
                marginRight='20px'
            )
        ),


        html.H3('R (Radius of the BLC):'),

        # R = input box of any positive number
        dcc.Input(
            id='R_input',
            placeholder='Enter a number',
            type='number',
            min=1e-100,
            value=1,
            style=dict(
                height='20px',
                marginTop='30px',
                marginLeft='20px',
                marginRight='20px'
            )
        ),

        html.H3('θ (Azimuth Angle):'),

        html.Div([
            # theta = slider b/w 0 and (2 * pi)
            dcc.Slider(
                id='theta_slider',
                min=0,
                max=math.pi * 2,
                step=0.01,
                value=math.pi,
                marks={
                    0: '0',
                    math.pi / 2: 'π/2',
                    math.pi: 'π',
                    (3 / 2) * math.pi: '3π/2',
                    math.pi * 2: '2π'
                }
            ),

            html.Div(
                id='theta_actual',
                children='Theta value'
            ),
        ]),



        html.H3('φ (Polar Angle):'),

        html.Div([
            # phi = slider b/w 0 and pi
            dcc.Slider(
                id='phi_slider',
                min=0,
                max=math.pi,
                step=0.01,
                value=math.pi/2,
                marks={
                    0: '0',
                    math.pi / 4: 'π/4',
                    math.pi / 2: 'π/2',
                    (3 / 4) * math.pi: '3π/4',
                    math.pi: 'π'
                }
            ),

            html.Div(
                id='phi_actual',
                children='Theta value'
            ),
        ]),

        html.H3('Total no.of points:'),

        html.Div([
            dcc.Input(
                id='total_num_input',
                placeholder='Enter a number',
                type='number',
                min=1,
                value=1e5,
                style=dict(
                    height='20px',
                    marginTop='20px',
                    marginLeft='20px',
                    marginRight='20px'
                )
            ),

            html.Div(
                id='incident_num',
                children='No.of incident points',
                style=dict(marginTop='10px')
            ),
        ]),

        html.Div([
            html.Button(
                'Update',
                id='submit_btn',
                n_clicks=0,
                disabled=False,
                style=dict(
                    fontSize='16px',
                    fontWeight='bold',
                    fontFamily='Times-new-roman'
                )
            )
        ])
    ],
        style=dict(
            display='grid',
            gridTemplateColumns='repeat(2, 1fr)',
            # gridGap='20px',
            flexDirection='column',
            marginTop='20px',
            # alignItems='center',
            justifyContent='left',
            textAlign='center',
            marginBottom='50px',
            border='1px dotted black',
            width='30%',
            height='100vh'
    )
    ),

    html.Div([
        html.H2(
            children='No incident Points, so distplot has not updated. Try different inputs'
        ),
    ],
        # the id here is not in the h2 because we want to change the style and not the text within the Div
        id='no_incid_pnts',
    ),

    html.Div([
        dcc.Graph(
            id='disk_outline_plot',

        )
    ],
        style=dict(
        display='flex',
        alignItems='center',
        justifyContent='center',
        textAlign='center',
    )
    ),

    html.Div([
        dcc.Graph(
            id='light_echo_dist',

        )
    ],
        style=dict(
            display='flex',
            alignItems='center',
            justifyContent='center',
            textAlign='center',
    )
    )
],
    style=dict(
    boxSizing='border-box',
    margin=0,
    display='flex'
)
)


# checks if all inputs are not null
@ app.callback(
    Output(component_id='submit_btn', component_property='disabled'),
    [Input('r_input', 'value'),
     Input('R_input', 'value'),
     Input('total_num_input', 'value')]
)
def check_inputs(r, R, t):
    if (r == None or R == None or t == None):
        return True
    else:
        return False


def getIncidentPoints(r, theta, phi, R, t):
    # duplicate calculation of h, j and k
    h = r * math.sin(phi) * math.cos(theta)
    j = r * math.sin(phi) * math.sin(theta)
    k = r * math.cos(phi)
    print('h: {} \n j: {} \n k: {}'.format(h, j, k))

    # random variates on (0, 1)
    u = np.random.rand(t)
    v = np.random.rand(t)

    # equispaced thetas and phis on the BLC surface
    theta_e = 2 * math.pi * u
    phi_e = np.arccos((2 * v) - 1)
    print('theta_e: {} \n phi_e: {}'.format(
        theta_e, phi_e))

    # filter the angles to only contain those in the upper hemisphere
    bool_mask = [phi_e <= (math.pi / 2)]
    print('bool_mask: {}'.format(bool_mask))

    theta_e = theta_e[bool_mask]
    phi_e = phi_e[bool_mask]
    print('theta_e (filtered): {} \n phi_e (filtered): {}'.format(theta_e, phi_e))

    # get all points on the sphere in the upper hemisphere
    x_upper = R * np.sin(phi_e) * np.cos(theta_e) + h
    y_upper = R * np.sin(phi_e) * np.sin(theta_e) + j
    z_upper = R * np.cos(phi_e) + k
    print('x_upper: {} \n y_upper: {} \n z_upper: {}'.format(
        x_upper, y_upper, z_upper))

    # create the boolean array with the condition that x y and z are within the AGN positional distance sphere
    bool_mask = [(x_upper ** 2) + (y_upper ** 2) + (z_upper ** 2) <= (r ** 2)]
    print('bool_mask: {}'.format(bool_mask))

    # filter all the x, y, and z using the boolean mask
    x_incident = x_upper[bool_mask]
    y_incident = y_upper[bool_mask]
    z_incident = z_upper[bool_mask]
    print('x_incident: {} \n y_incident: {} \n z_incident: {}'.format(
        x_incident, y_incident, z_incident))

    return x_incident, y_incident, z_incident

# app callbacks must always contain in the order Output, Input, State


@ app.callback(
    Output(component_id='disk_outline_plot', component_property='figure'),
    [Input('submit_btn', 'n_clicks')],
    [State('r_input', 'value'),
     State('theta_slider', 'value'),
     State('phi_slider', 'value'),
     State('R_input', 'value'),
     State('total_num_input', 'value')]
)
def update_figure(n_clicks, r, theta, phi, R, t):
    # calculations

    # position of the BLC center i.e. sphere center relative to the AGN i.e. active galactic nucleus i.e. origin
    # r
    # theta
    # phi

    h = r * math.sin(phi) * math.cos(theta)
    j = r * math.sin(phi) * math.sin(theta)
    k = r * math.cos(phi)
    print('h: {} \n j: {} \n k: {}'.format(h, j, k))

    # position of the points on the surface of the BLC
    # R
    # theta_d
    # phi_d

    # theta_d = all numbers b/w 0 and (2 * pi)
    theta_d = np.linspace(0, 2 * math.pi, 24)

    # phi_d = all numbers b/w 0 and pi
    phi_d = np.linspace(0, math.pi, 24)

    tGrid, pGrid = np.meshgrid(theta_d, phi_d)

    # equation of AGN positional distance surface
    x_AGN = r * np.sin(pGrid) * np.cos(tGrid)
    y_AGN = r * np.sin(pGrid) * np.sin(tGrid)
    z_AGN = r * np.cos(pGrid)
    print('x_AGN: {} \n y_AGN: {} \n z_AGN: {}'.format(
        x_AGN, y_AGN, z_AGN))

    # equation of BLC surface
    x_BLC = R * np.sin(pGrid) * np.cos(tGrid) + h
    y_BLC = R * np.sin(pGrid) * np.sin(tGrid) + j
    z_BLC = R * np.cos(pGrid) + k
    print('x_BLC: {} \n y_BLC: {} \n z_BLC: {}'.format(
        x_BLC, y_BLC, z_BLC))

    # get the incident point coordinates in x, y, z
    x_incident, y_incident, z_incident = getIncidentPoints(r, theta, phi, R, t)

    # create the data and layout
    # AGN_pos_surface = go.Surface(
    #     x=x_AGN,
    #     y=y_AGN,
    #     z=z_AGN,
    #     name='AGN Positional Surface'
    # )

    BLC_surface = go.Surface(
        x=x_BLC,
        y=y_BLC,
        z=z_BLC,
        name='BLC Surface'
    )

    incident_surface = go.Scatter3d(
        x=x_incident,
        y=y_incident,
        z=z_incident,
        mode='markers',
        marker=dict(color='green', size=2),
        name='Incident Surface'
    )

    origin_point = go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(color='red', size=5),
        name='AGN'
    )

    data = [BLC_surface, incident_surface, origin_point]

    # create the layout
    # cannot use go.Layout() because it does not take zaxis parameter
    # so instead update layout after defining fig

    fig = go.Figure(data)

    fig.update_layout(
        title='Incident Points on the BLC of light echoes from the AGN',
        scene=dict(
            xaxis=dict(nticks=10, title='x-axis'),
            yaxis=dict(nticks=10, title='y-axis'),
            zaxis=dict(nticks=10, title='z-axis'),
            # if you uncomment the aspect stuff below, the sphere will stretch becasue the scale will be preserved and teh cells will become more rectangular. By defualt the scale is the same for all three axes, so no need to change any axis aspect # aspectmode='manual',
            # aspectratio=dict(x=1, y=1, z=1)
        ),
        width=900,
        height=600)

    return fig


def getExtraDist(x_incident, y_incident, z_incident):
    # find the direct distance from the origin
    # for negative values of z_incident the direct distance is added to the indirect path since z_indirect will be negative
    dist_direct = z_incident - 0

    # find the indirect distance from origin to the incident point
    dist_indirect = np.sqrt((x_incident ** 2) +
                            (y_incident ** 2) + (z_incident ** 2))

    # find the extra distance travelled
    dist_diff = dist_indirect - dist_direct
    print('dist_diff: {}'.format(dist_diff))

    return dist_diff


@app.callback(
    Output(component_id='light_echo_dist', component_property='figure'),
    [Input('submit_btn', 'n_clicks')],
    [State('r_input', 'value'),
     State('theta_slider', 'value'),
     State('phi_slider', 'value'),
     State('R_input', 'value'),
     State('total_num_input', 'value')]
)
def update_dist(n_clicks, r, theta, phi, R, t):
    # get the incident point coordinates in x, y, z
    x_incident, y_incident, z_incident = getIncidentPoints(r, theta, phi, R, t)

    # get the difference in distance when travelling to the observer directly vs indirectly
    dist_diff = getExtraDist(x_incident, y_incident, z_incident)

    # create the trace with time in nano seconds
    time_delay = dist_diff / 0.2998

    # creat the data of the figure
    dist_data = [time_delay]

    # create the labels
    group_labels = ['Time Delays in ns']

    # create the figure
    # in bin_size np.ptp calculates the range of an array
    # histnorm probability makes the y-axis probability
    fig = ff.create_distplot(dist_data, group_labels,
                             bin_size=[np.ptp(time_delay) / 20], histnorm='probability')

    fig.update_layout(
        title='Time delay distribution',
        width=900,
        height=600
    )

    return fig


@ app.callback(
    Output('theta_actual', 'children'),
    [Input('theta_slider', 'value')]
)
def theta_val_on_slide(value):
    return 'Current θ chosen: {:.2f}'.format(value)


@ app.callback(
    Output('phi_actual', 'children'),
    [Input('phi_slider', 'value')]
)
def phi_val_on_slide(value):
    return 'Current φ chosen: {:.2f}'.format(value)


@ app.callback(
    Output('theta_d_actual', 'children'),
    [Input('theta_d_slider', 'value')]
)
def theta_d_val_on_slide(value):
    return 'Current θd chosen: {:.2f}'.format(value)


@ app.callback(
    Output('phi_d_actual', 'children'),
    [Input('phi_d_slider', 'value')]
)
def phi_d_val_on_slide(value):
    return 'Current φd chosen: {:.2f}'.format(value)


@ app.callback(
    Output('incident_num', 'children'),
    [Input('submit_btn', 'n_clicks')],
    [State('r_input', 'value'),
     State('theta_slider', 'value'),
     State('phi_slider', 'value'),
     State('R_input', 'value'),
     State('total_num_input', 'value')]
)
def num_incident_points(n_clicks, r, theta, phi, R, t):
    x, y, z = getIncidentPoints(r, theta, phi, R, t)

    # number of incident points could be length of either x y or z because all three are of equal lengths
    num_incident = len(x)
    print('num_incident: {}'.format(num_incident))

    return 'Number of incident points: {}'.format(num_incident)


@ app.callback(
    Output('no_incid_pnts', 'style'),
    [Input('submit_btn', 'n_clicks')],
    [State('r_input', 'value'),
     State('theta_slider', 'value'),
     State('phi_slider', 'value'),
     State('R_input', 'value'),
     State('total_num_input', 'value')]
)
def no_incid_pnts_mssg_display(n_clicks, r, theta, phi, R, t):
    x, y, z = getIncidentPoints(r, theta, phi, R, t)

    if(len(x) == 0 or len(y) == 0 or len(z) == 0):
        style = dict(
            display='flex',
            alignItems='center',
            justifyContent='center',
            textAlign='center',
            minWidth='200px',
            marginLeft='20px'
        )
    else:
        style = dict(
            display='none',
            alignItems='center',
            justifyContent='center',
            textAlign='center',
        )

    return style


# run server
if __name__ == "__main__":
    app.run_server()


# app.layout = html.Div([
#     html.H2('Hello World'),
#     dcc.Dropdown(
#         id='dropdown',
#         options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
#         value='LA'
#     ),
#     html.Div(id='display-value')
# ])


# @app.callback(dash.dependencies.Output('display-value', 'children'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)


# if __name__ == '__main__':
#     app.run_server(debug=True)
