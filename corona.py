from flask import Flask,render_template
app = Flask(__name__)

import plotly.graph_objs as go 
import plotly, json
import pandas as pd 
import numpy as np

complete_data = pd.read_csv('complete.csv')
complete_data =complete_data.drop(
  ['Total Confirmed cases (Indian National)',
  'Total Confirmed cases ( Foreign National )'],
  axis =1)
  
'''
import plotly.express as px
fig = px.scatter_geo(complete_data,lat="Latitude", lon="Longitude", color='Total Confirmed cases', size='Total Confirmed cases', 
                     projection="natural earth",
                     hover_name='Name of State / UT', scope='asia', animation_frame="Date",
                     color_continuous_scale=px.colors.diverging.curl,center={'lat':20, 'lon':78}, 
                     range_color=[0, max(complete_data['Total Confirmed cases'])])
fig.update_layout(plot_bgcolor='rgb(275, 270, 100)')

'''

from corona_graphs import Build_graphs
build_graphs = Build_graphs(complete_data)
figures = build_graphs.return_figures()



#figures = [fig]
ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]
figuresJSON = json.dumps(figures,cls=plotly.utils.PlotlyJSONEncoder)



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',ids=ids,figuresJSON=figuresJSON)

@app.route('/state-wise')
def statewise():
    return render_template('state-wise.html')

@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

if __name__ == "__main__":
    app.run(debug=True)