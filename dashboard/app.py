import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)


@app.callback(
    Output('bar', 'figure'),
    Input('district', 'value')
)
def update_bar_chart(district):
    mask = regions['district'] == district
    fig = px.bar(regions[mask],
                 x='region', y='count',
                 labels={
                     'region': 'Регион',
                     'count': 'Количество вузов'})
    return fig


if __name__ == '__main__':
    dataframe = pd.read_csv('data/Вузы (с адресами).csv').dropna()

    districts = dataframe['Округ'].value_counts()
    fig_pie = px.pie(names=districts.index, values=districts.values)

    app.layout = html.Div([
        html.H1('Аналитика по расположению вузов в РФ'),
        html.P(
            [html.Span('Общее число вузов: '),
             html.U(len(dataframe), className='count_value'),
             html.Span(' (с информацией об адресах)')],
            className='count'
        ),
        html.Div([
            html.H2('Количество вузов в округах РФ'),
            dcc.Graph(id='pie',
                      figure=fig_pie)
        ]),
        html.Div([
            html.H2('Количество вузов в регионах РФ'),
            dcc.Graph(id='bar'),
            html.P('Округ'),
            dcc.Dropdown(
                id='district',
                options=dataframe['Округ'].unique().tolist(),
                value='Центральный'
            )
        ])
    ], className='main')

    region_counts = dataframe['Регион'].value_counts()
    regions = pd.DataFrame()
    regions['region'] = region_counts.index
    regions['count'] = region_counts.values
    buffer = dataframe[['Регион',
                        'Округ']].drop_duplicates().dropna()
    regions['district'] = [
        ''.join(buffer['Округ'].loc[buffer['Регион'] == region].tolist())
        for region in regions['region']
    ]

    app.run_server(debug=True)
