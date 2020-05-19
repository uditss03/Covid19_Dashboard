import pandas as pd 
import numpy as np
#from plotly.offline import iplot
import plotly.graph_objs as go 
import plotly.express as px


class Build_graphs:
  def __init__(self,complete_data,state_name = None):
    self.complete_data = complete_data
    self.state_name = state_name
    
  def data_cleaning(self,data):
    temp_data = pd.DataFrame()
    temp_data['Date'] = data['Date']
    temp_data['Death'] = data['Death']
    temp_data['Cured'] = data['Cured/Discharged/Migrated']
    temp_data['Total'] = data['Total Confirmed cases']
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
    t = self.complete_data
    temp = self.data_cleaning(t)
    
    
    x = self.complete_data['Date'].unique()
    state_wise = pd.DataFrame(self.complete_data.loc[self.complete_data['Date'] == x[len(x)-1]])


    # fig 0
    fig0 = px.scatter_geo(state_wise,lat="Latitude", lon="Longitude", color='Total Confirmed cases', size='Total Confirmed cases', 
                        projection="natural earth",
                        hover_name='Name of State / UT', scope='asia', 
                        color_continuous_scale=px.colors.diverging.curl,center={'lat':20, 'lon':78},
                        range_color=[0, max(state_wise['Total Confirmed cases'])])
    figures.append(fig0)
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
      go.Bar(name='Active Cases', x=temp['Date'], y=temp['Active'],marker_color='#ff7f0e'),
      go.Bar(name='Confirmed Cases', x=temp['Date'], y=temp['Total'],marker_color='#326ac7')])
    fig1.update_layout(barmode='stack')
    figures.append(fig1)


    #fig 2
    cur = temp['Cured'][len(temp)-1]
    act = temp['Active'][len(temp)-1]
    ded = temp['Death'][len(temp)-1]
    labels = ['Active Cases','Recovered','Total Deaths']
    values = [act, cur, ded]

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)],layout=dict(title='Corona Cases till Now'))
    figures.append(fig2)

    # fig 3
    trace1 = go.Scatter(x = temp['Date'],
                    y = temp['Cured'],
                    name = 'Deaths',
                    opacity = 0.8)
    trace2 = go.Scatter(x = temp['Date'],
                    y = temp['Death'],
                    name = 'Deaths',
                    opacity = 0.8)
    data = [trace1,trace2]
    layout = dict(title = 'Total Recoveries and Deaths in India',
                  xaxis = dict(title='Dates'),
                  yaxis = dict(title='Recoveries'))

    fig3 = dict(data = data,layout=layout)
    figures.append(fig3)

    # fig 4
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
    fig4 = dict(data = data,layout=layout)
    figures.append(fig4)

    
    return figures

  def return_state_figures(self):

    figures = []
    state_data = pd.DataFrame(self.complete_data.loc[self.complete_data['Name of State / UT'] == self.state_name])
    temp = self.data_cleaning(state_data)

    st = state_data
    x = st['Date'].unique()
    st.where(st['Date']==x[len(x)-1],inplace=True)
    st = st.dropna()

    # fig 0
    fig0 = px.scatter_geo(st,lat="Latitude", lon="Longitude", color='Total Confirmed cases', size='Total Confirmed cases', 
                        projection="natural earth",
                        hover_name='Name of State / UT', scope='asia', 
                        color_continuous_scale=px.colors.diverging.curl,center={'lat':20, 'lon':78},
                        range_color=[0, max(st['Total Confirmed cases'])])
    figures.append(fig0)
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
      go.Bar(name='Active Cases', x=temp['Date'], y=temp['Active'],marker_color='#ff7f0e'),
      go.Bar(name='Confirmed Cases', x=temp['Date'], y=temp['Total'],marker_color='#326ac7')])
    fig1.update_layout(barmode='stack')
    figures.append(fig1)


    #fig 2
    cur = temp['Cured'][len(temp)-1]
    act = temp['Active'][len(temp)-1]
    ded = temp['Death'][len(temp)-1]
    labels = ['Active Cases','Recovered','Total Deaths']
    values = [act, cur, ded]

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)],layout=dict(title='Corona Cases till Now'))
    figures.append(fig2)

    # fig 3
    trace1 = go.Scatter(x = temp['Date'],
                    y = temp['Cured'],
                    name = 'Deaths',
                    opacity = 0.8)
    trace2 = go.Scatter(x = temp['Date'],
                    y = temp['Death'],
                    name = 'Deaths',
                    opacity = 0.8)
    data = [trace1,trace2]
    layout = dict(title = 'Total Recoveries and Deaths in India',
                  xaxis = dict(title='Dates'),
                  yaxis = dict(title='Recoveries'))

    fig3 = dict(data = data,layout=layout)
    figures.append(fig3)

    # fig 4
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
    fig4 = dict(data = data,layout=layout)
    figures.append(fig4)

    
    return figures


