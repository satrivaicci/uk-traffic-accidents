import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'US Accidents'
sourceurl = 'https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents'
githublink = 'https://github.com/satrivaicci/us-traffic-accidents'

########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/US_Accidents_Dec21_updated.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


#### Define Years list

def getYear(startTime):
    return int(startTime[0:4])

df['Year'] = df['Start_Time'].apply(getYear)
years_list = df.Year.unique()
years_list.sort()


### Group by year and state

dfByState = df.groupby(['Year', 'State']).size().reset_index(name='Counts')

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('2016-2021 US Traffic Accidents, by State'),
    html.Div([
        html.Div([
                html.H6('Select a year for analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in years_list],
                    value='2016'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Traffic accidents in {varname}'
    mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = "Total count"

    data=go.Choropleth(
        locations=dfByState['State'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = dfByState[dfByState['Year'] == varname]['Counts'], # Data to be color-coded
        colorscale = ['lightgrey','blue'],
        colorbar_title = 'some title',
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
