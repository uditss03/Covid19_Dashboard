from flask import Flask,render_template,request, redirect, url_for
app = Flask(__name__)

import plotly.graph_objs as go 
import plotly, json
import pandas as pd 
import numpy as np

try:
    complete_data = pd.read_csv("https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/complete.csv")
except:
    complete_data = pd.read_csv('complete.csv')
#complete_data = pd.read_csv('complete.csv')
complete_data =complete_data.drop(
  ['Total Confirmed cases (Indian National)',
  'Total Confirmed cases ( Foreign National )'],
  axis =1)
  


from corona_graphs import Build_graphs




@app.route('/')
@app.route('/index')
def index():
    build_graphs = Build_graphs(complete_data=complete_data)
    figures = build_graphs.return_figures()
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]
    figuresJSON = json.dumps(figures,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',ids=ids,figuresJSON=figuresJSON)


@app.route('/state-wise',methods=['GET','POST'])
def statewise():
    if (request.method=='POST'):
        state_name = request.form['state_name']
        return redirect(url_for("state",state_name=state_name))
    else:
        return render_template('state-wise.html')   


@app.route('/<state_name>')
def state(state_name):
    build_graphs = Build_graphs(complete_data=complete_data,state_name = state_name)
    figures = build_graphs.return_state_figures()
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]
    figuresJSON = json.dumps(figures,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('state.html',state_name=state_name,ids=ids,figuresJSON=figuresJSON)


@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

#if __name__ == "__main__":
#    app.run(debug=True)