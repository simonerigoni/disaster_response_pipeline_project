# Dash App
#
# python dash_app.py


import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import disaster_response_pipeline


MAX_INPUT_LENGTH = 512
EXTERNAL_STYLESHEETS = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
        'crossorigin': 'anonymous'
    },
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp',
        'crossorigin': 'anonymous'
    }
]


def _create_app():
    ''' 
    Creates dash application

    Returns:
        app (dash.Dash): Dash application
    '''

    app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

    model = disaster_response_pipeline.load_pipeline()

    app.layout = dash.html.Div(
        [
            dbc.Nav(
                [
                    dash.html.Div(
                        [
                            dash.html.Div(
                                [
                                    dash.html.A('Disaster Response Pipeline Project',
                                                href='/', className='navbar-brand')
                                ], className='navbar-header'), dash.html.Div(
                                [
                                    dash.html.Ul(
                                        [
                                            dash.html.Li(dash.html.A('Made with Udacity', href='https://www.udacity.com/')), dash.html.Li(dash.html.A(
                                                'Github', href='https://github.com/simonerigoni/disaster_response_pipeline_project'))
                                        ], className='nav navbar-nav')
                                ], className='collapse navbar-collapse')
                        ], className='container')
                ], className='navbar navbar-inverse navbar-fixed-top'), dash.html.Div(
                [
                    dash.html.Div(
                        [
                            dash.html.H1('Disaster Response Pipeline Project', className='text-center'), dash.html.P('Analyzing message data for disaster response', className='text-center'), dash.html.Hr(), dash.html.Div(
                                [
                                    dash.html.Div(
                                        [
                                            dash.dcc.Input(id='input-message', type='text', value='', placeholder='Enter a message to classify', maxLength=MAX_INPUT_LENGTH, className='form-control form-control-lg'), dash.html.Hr(), dash.html.Div(
                                                [
                                                    dash.html.Button(
                                                        'Classify Message', id='button-submit', className='btn btn-lg btn-success')
                                                ], className='col-lg-offset-5')
                                        ], className='col-lg-12 form-group-lg')
                                ], className='row')
                        ], className='container')
                ], className='jumbotron'), dash.html.Div(id='results')
        ], className='container')

    @app.callback(dash.dependencies.Output('results', 'children'), [dash.dependencies.Input('button-submit', 'n_clicks')], [dash.dependencies.State('input-message', 'value')])
    def update_results(n_click, message):
        '''
        Update the results section. 

        Args:
            message (str): value of the input-message
            n_click (int): value of n_clicks of button-submit

        Returns:
            results (list): list of dash components 
        '''
        results = []
        if len(message) > 0:  # and int(0 if n_click is None else n_click) > 0:
            category_predicted = model.predict([message])[0]
            name_category_predicted = disaster_response_pipeline.get_predicted_category_names(
                category_predicted)
            print('Message to be classified: {}'.format(message))
            print('Categories:')
            print(name_category_predicted)
            results.append(dash.html.Div(
                [
                    dash.html.H2('Results', className='text-center'), dash.html.H3('Message to be classified: {}'.format(
                        message)), dash.html.H3('Categories', className='text-center')
                    # , dash.html.H3(', '.join(disaster_response_pipeline.get_predicted_category_names(category_predicted)))
                    # , dash.html.Ul(
                    #     [
                    #     ], className = 'list-group')
                ]))

            for category in disaster_response_pipeline.get_category_names():
                if category in name_category_predicted:
                    results.append(dash.html.Li(category.replace('_', ' ').title(
                    ), className='list-group-item list-group-item-success text-center'))
                else:
                    results.append(dash.html.Li(category.replace('_', ' ').title(
                    ), className='list-group-item list-group-item-dark text-center'))
        else:
            genre_distribution = disaster_response_pipeline.get_genre_distribution()
            top_n_categories = disaster_response_pipeline.get_top_n_categories()

            results.append(dash.html.Div(
                [
                    dash.html.H2('Overview of Training Dataset', className='text-center'), dash.dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x=list(genre_distribution.keys()), y=list(genre_distribution.values()), name='Count', marker=go.bar.Marker(color='rgb(55, 83, 109)')
                                )
                            ], layout=go.Layout(
                                title='Message Genre Distribution', showlegend=True, legend=go.layout.Legend(x=0, y=1.0), margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                            )
                        ), style={'height': 300}, id='genre-distribution-graph'), dash.dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x=list(top_n_categories.keys()), y=list(top_n_categories.values()), name='Count', marker=go.bar.Marker(color='rgb(55, 83, 109)')
                                )
                            ], layout=go.Layout(
                                title='Categories Distribution', showlegend=True, legend=go.layout.Legend(x=0, y=1.0), margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                            )
                        ), style={'height': 300}, id='categories-distribution-graph')
                ]))
        return results

    return app


if __name__ == '__main__':
    app = _create_app()
    app.run(debug=True)
else:
    pass
