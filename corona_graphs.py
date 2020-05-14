import pandas as pd 
import numpy as np
#from plotly.offline import iplot
import plotly.graph_objs as go 
import plotly.express as px


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

  def state_case(self):
    state_wise = pd.DataFrame(self.complete_data)
    state_wise = state_wise.groupby(state_wise['Name of State / UT']).sum()
    state_wise['Name of State / UT'] = list(state_wise.index)
    lat = {'Delhi':28.7041, 'Haryana':29.0588, 'Kerala':10.8505, 'Rajasthan':27.0238,
         'Telengana':18.1124, 'Uttar Pradesh':26.8467, 'Ladakh':34.2996, 'Tamil Nadu':11.1271,
          'Jammu and Kashmir':33.7782, 'Punjab':31.1471, 'Karnataka':15.3173, 'Maharashtra':19.7515,
          'Andhra Pradesh':15.9129, 'Odisha':20.9517, 'Uttarakhand':30.0668, 'West Bengal':22.9868, 
          'Puducherry': 11.9416, 'Chandigarh': 30.7333, 'Chhattisgarh':21.2787, 'Gujarat': 22.2587, 
          'Himachal Pradesh': 31.1048, 'Madhya Pradesh': 22.9734, 'Bihar': 25.0961, 'Manipur':24.6637, 
          'Mizoram':23.1645, 'Goa': 15.2993, 'Andaman and Nicobar Islands': 11.7401, 'Assam' : 26.2006, 
          'Jharkhand': 23.6102, 'Arunachal Pradesh': 28.2180, 'Tripura': 23.9408, 'Nagaland': 26.1584, 
          'Meghalaya' : 25.4670, 'Dadar Nagar Haveli' : 20.1809}

    lon = {'Delhi':77.1025, 'Haryana':76.0856, 'Kerala':76.2711, 'Rajasthan':74.2179,
          'Telengana':79.0193, 'Uttar Pradesh':80.9462, 'Ladakh':78.2932, 'Tamil Nadu':78.6569,
          'Jammu and Kashmir':76.5762, 'Punjab':75.3412, 'Karnataka':75.7139, 'Maharashtra':75.7139,
          'Andhra Pradesh':79.7400, 'Odisha':85.0985, 'Uttarakhand':79.0193, 'West Bengal':87.8550, 
          'Puducherry': 79.8083, 'Chandigarh': 76.7794, 'Chhattisgarh':81.8661, 'Gujarat': 71.1924, 
          'Himachal Pradesh': 77.1734, 'Madhya Pradesh': 78.6569, 'Bihar': 85.3131, 'Manipur':93.9063, 
          'Mizoram':92.9376, 'Goa': 74.1240, 'Andaman and Nicobar Islands': 92.6586, 'Assam' : 92.9376, 
          'Jharkhand': 85.2799, 'Arunachal Pradesh': 94.7278, 'Tripura': 91.9882, 'Nagaland': 94.5624,
          'Meghalaya' : 91.3662, 'Dadar Nagar Haveli' : 73.0169}
    state_wise['Latitude'] = state_wise['Name of State / UT'].map(lat)

    state_wise['Longitude'] = state_wise['Name of State / UT'].map(lon)
    return state_wise

  def return_figures(self):

    figures = []
    temp = self.data_cleaning()
    state_wise = self.state_case()

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



