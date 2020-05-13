import pandas as pd 
import numpy as np
#from plotly.offline import iplot
import plotly.graph_objs as go 
  

class Build_graphs:
  def __init__(self,complete_data):
    self.complete_data = complete_data
    
  def data_cleaning(self):
    temp_data = pd.DataFrame()
    temp_data['Date'] = self.complete_data['Date']
    temp_data['Death'] = self.complete_data['Death']
    temp_data['Cured'] = self.complete_data['Cured/Discharged/Migrated']
    temp_data['Total'] = self.complete_data['Total Confirmed cases']
    temp_data['Date'] = pd.to_datetime(temp_data['Date'])
    temp = temp_data.groupby(temp_data['Date'].dt.date).sum()
    temp['Date'] = list(temp.index)
    temp['Active'] = temp['Total'] - temp['Death'] - temp['Cured']
    def daily(col):
      new_col = [0 for i in range(len(col))]
      new_col[0] = col[0]
      for i in range(len(col)-1,1,-1):
        new_col[i] = col[i] - col[i-1]
      return new_col
    temp['Daily_Cases'] = daily(temp['Total'])
    temp['Daily_Cured'] = daily(temp['Cured'])
    temp['Daily_Death'] = daily(temp['Death'])
    return temp

  def return_figures(self):

    figures = []
    temp = self.data_cleaning()

    # fig 1
    '''trace = go.Scatter(x = temp['Date'],
                    y = temp['Total'],
                    name = 'Total Cases',
                    opacity = 0.8)
    data = [trace]
    layout = dict(title = 'Total Corona cases in India',
                  xaxis=dict(title='Dates'),
                  yaxis=dict(title='Total Cases'))
    fig1 = dict(data = data,layout=layout)'''
    fig1 = go.Figure(data=[
                        go.Bar(name='Deaths', x=temp['Date'], y=temp['Death'],marker_color='#ff0000'),
                        go.Bar(name='Recovered Cases', x=temp['Date'], y=temp['Cured'],marker_color='#2bad57'),
                        go.Bar(name='Confirmed Cases', x=temp['Date'], y=temp['Total'],marker_color='#326ac7')]
                        ,layout = dict(title='COVID-19 Updates',xaxis=dict(title='Dates'),yaxis=dict(title='Cases | Recoveries | Deaths')))
    fig1.update_layout(barmode='stack')
    figures.append(fig1)

    #fig 2
    trace1 = go.Bar(x = temp['Date'],
                    y = temp['Death'],
                    name = 'Deaths',
                    opacity = 0.8)

    data = [trace1]
    layout = dict(title = 'Total Deaths in India',
                  xaxis=dict(title='Dates'),
                  yaxis=dict(title='Total Deaths')
                  )
    fig2 = dict(data = data,layout=layout)
    figures.append(fig2)

    # fig 3
    trace1 = go.Scatter(x = temp['Date'],
                    y = temp['Daily_Cases'],
                    name = 'New Cases',
                    opacity = 0.8)
    trace2 = go.Scatter(x = temp['Date'],
                    y = temp['Daily_Death'],
                    name = 'New Deaths',
                    opacity = 0.8)
    trace3 = go.Scatter(x = temp['Date'],
                    y = temp['Daily_Cured'],
                    name = 'New Recoveries',
                    opacity = 0.8)
    data = [trace1,trace2,trace3]
    layout = dict(title = 'Daily Update of Covid-19 cases - India',
                  xaxis=dict(title='Daily Cases'),
                  yaxis=dict(title='Daily Cases'))
    fig3 = dict(data = data,layout=layout)
    figures.append(fig3)

    return figures



