import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Read data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# App setup
app = dash.Dash(__name__)

# Get min and max payload
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),

    # Task 1: Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] +
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder='Select a Launch Site here',
                 searchable=True),

    html.Br(),

    # Task 2: Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # Task 3: Payload Range Slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)},
                    value=[min_payload, max_payload]),

    # Task 4: Scatter Chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2: Pie Chart Callback
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(site_df, names='class',
                     title=f'Total Success vs Failure for {entered_site}')
    return fig

# Task 4: Scatter Chart Callback
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_plot(site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    if site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs Outcome for All Sites')
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs Outcome for {site}')
    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)



