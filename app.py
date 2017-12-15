import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        dcc.Graph(id='task_bar_graph'),
        dcc.Graph(id='task_line_graph'),
    ])

# 日付を入力
@app.callback(
    Output('task_bar_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('startdate-input', 'value'),
     State('enddate-input', 'value')]
)
def update_task_bar_graph(n_clicks, start_date, end_date):

    df = get_jira_tasks(start_date, end_date)
    task_info = df.groupby(['name']).sum()
    graph = {
            'data': [
                {'x': task_info.index, 'y': list(task_info.loc[:, "timeoriginalestimate"]), 'type': 'bar', 'name': '予'},
                {'x': task_info.index, 'y': list(task_info.loc[:, "timespent"]), 'type': 'bar', 'name': '実'},
            ],
            'layout': {
                'title': 'Member tasks {}〜{}'.format(start_date, end_date)
            }
        }
    return graph

# 日付を入力
@app.callback(
    Output('task_line_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('startdate-input', 'value'),
     State('enddate-input', 'value')]
)
def update_task_line_graph(n_clicks, start_date, end_date):

    df = get_jira_tasks(start_date, end_date)
    task_info = df.groupby(['day']).sum()
    graph = {
            'data': [
                {'x': task_info.index, 'y': list(task_info.loc[:, "timeoriginalestimate"]), 'type': 'line', 'name': '予'},
                {'x': task_info.index, 'y': list(task_info.loc[:, "timespent"]), 'type': 'line', 'name': '実'},
            ],
            'layout': {
                'title': 'Team tasks {}〜{}'.format(start_date, end_date)
            }
        }
    return graph


if __name__ == '__main__':
    app.run_server()