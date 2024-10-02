import pandas as pd
import plotly.express as px
import dash             
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Read and preprocess data
df = pd.read_excel("datasets\coviddata.xlsx")
dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths','cases']].sum()

# Define the app layout
app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            style_cell_conditional=[
                {'if': {'column_id': 'countriesAndTerritories'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'deaths'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'cases'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='piedropdown',
                options=[
                        {'label': 'Deaths', 'value': 'deaths'},
                        {'label': 'Cases', 'value': 'cases'}
                ],
                value='cases',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),

        html.Div([
            dcc.Dropdown(id='linedropdown',
                options=[
                         {'label': 'Deaths', 'value': 'deaths'},
                         {'label': 'Cases', 'value': 'cases'}
                ],
                value='deaths',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='piechart'),
        ],className='four columns'),

        html.Div([
            dcc.Graph(id='scatterchart'),
        ],className='eight columns'),
    ],className='row'),
])

@app.callback(
    [Output('scatterchart', 'figure'),
     Output('piechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = dff[dff['countriesAndTerritories'].isin(['China','Iran','Spain','Italy'])]
    else:
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='countriesAndTerritories',
            values=piedropval,
            hole=.3,
            labels={'countriesAndTerritories':'Countries'}
            )

    #extract list of chosen countries
    list_chosen_countries=df_filterd['countriesAndTerritories'].tolist()
    #filter original df according to chosen countries
    #because original df has all the complete dates
    df_scatter = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

    scatter_chart = px.scatter(
            data_frame=df_scatter,
            x='dateRep',
            y=linedropval,
            color='countriesAndTerritories',
            hover_data=['deaths', 'cases'],
            labels={'countriesAndTerritories':'Countries', 'dateRep':'Date'},
            )
    
    return (pie_chart,scatter_chart)

if __name__ == '__main__':
    app.run_server(debug=True)
