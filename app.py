import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils.jira_api import get_jira_tasks


# appの初期化
app = dash.Dash()
# bootstrapの追加
app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'})

# メインhtmlの作成
app.layout = \
    html.Div(className="container", children=[

        html.H1(children='Task Dashboard'),
        dcc.Input(
            id='startdate-input',
            type='Date',
            value=dt.date.today() - dt.timedelta(days=30)
        ),
        dcc.Input(
            id='enddate-input',
            type='Date',
            value=dt.date.today()
        ),
        dcc.Graph(id='task_graph'),

    ])

# 日付を入力
@app.callback(
    Output('task_graph', 'figure'),
    [Input(component_id='startdate-input', component_property='value'),
     Input(component_id='enddate-input', component_property='value')]
)
def update_task_graph(start_date, end_date):
    print("start={} end={}".format(start_date, end_date))
    df = get_jira_tasks(start_date, end_date)
    task_info = df.groupby(['name']).sum()
    graph = {
            'data': [
                {'x': task_info.index, 'y': list(task_info.ix[:, 0]), 'type': 'bar', 'name': '予'},
                {'x': task_info.index, 'y': list(task_info.ix[:, 1]), 'type': 'bar', 'name': '実'},
            ],
            'layout': {
                'title': 'Member tasks {}〜{}'.format(start_date, end_date)
            }
        }
    return graph


if __name__ == '__main__':
    app.run_server(debug=True)