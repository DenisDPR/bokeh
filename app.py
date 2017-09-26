from flask import Flask, render_template, request, redirect



app = Flask(__name__)


app.vars={}

import simplejson as json
import urllib2
import numpy as np
import pandas as pd
from bokeh.embed import components
import bokeh.charts

quandlkey='8Wy423i2j9KUSTzAoZEA'

@app.route('/')

def main():
  
    return redirect('/index')


@app.route('/index',methods=['GET','POST'])

def index():

    if request.method == 'GET': 
        return render_template('index.html')


    else:
	app.vars['ticker']=request.form['ticker']
	app.vars['selected_features'] = request.form.getlist("features")
	#print app.vars
	return redirect ('/graph')


@app.route('/graph',methods=['GET','POST'])


def graph():
    if request.method == 'GET':
        url=''.join(['https://www.quandl.com/api/v3/datasets/WIKI/',app.vars['ticker'],'.json?api_key=',quandlkey])
        pydata= json.loads(urllib2.urlopen(url).read())
        colname=pydata['dataset']['column_names']
        data=pydata['dataset']['data']
        df=pd.DataFrame(np.array(data),columns=colname)
        df.index=pd.to_datetime(df.pop('Date'))
        col=app.vars['selected_features']
        df_multi=df[col]
	df_multi.rename(columns=lambda x: app.vars['ticker']+':'+x, inplace=True)
        df_multi=df_multi.astype(float)

        plot = bokeh.charts.Line(df_multi, title='Data from Quandle WIKI set', xlabel='date',legend="top_left")
        script, div = components(plot)
        return render_template('graph.html', script=script, div=div, stock=app.vars['ticker'])
	

if __name__ == '__main__':
  
    app.run(port=33507)
