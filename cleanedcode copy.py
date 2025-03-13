import pandas as pd
import numpy as np
import plotly.express as px
from flask import Flask, render_template, request, redirect, url_for

dataset = pd.read_csv("Data.csv")

dataset.drop(columns=['Driving Test Categories','UNIT','Statistic Label'], inplace=True)
changed_data = dataset

dataset['Month'] = pd.to_datetime(dataset['Month'] + ' 01', format='%Y %B %d')
dataset.sort_values(by='Month', inplace=True)

dataset_pivot = dataset.pivot_table(index="Month", columns="County", values="VALUE", aggfunc='mean')
dataset_pivot.reset_index(inplace=True)

dataset['Month'] = dataset['Month'].dt.strftime('%d-%m-%Y')
dataset_pivot['Month'] = pd.to_datetime(dataset_pivot['Month']).dt.strftime('%d-%m-%Y')

dataset_pivot.to_csv('cleaneddata.csv', index=False)

dataset_cleaned = pd.read_csv("cleaneddata.csv")

dataset_cleaned.columns = dataset_cleaned.columns.str.strip()

stats_dictionary = {}
numeric_cols = ['Co. Donegal', 'Co. Dublin', 'Co. Galway']
for col in numeric_cols:
        stats_data = dataset_cleaned[col].dropna() 
        stats_dictionary[col] = {
            'Mean': stats_data.mean(),
            'Median': stats_data.median(),
            'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
            'Range': stats_data.max() - stats_data.min() }

#concerts statistics dictionary to a dataframe and saves it to a csv file called 'statistics.csv'
statistics_dataset = pd.DataFrame(stats_dictionary).T
statistics_dataset.to_csv('statistics.csv', index=True)

#prints statistics 
print("Statistics DataFrame:")
print(statistics_dataset)

#Creates bar chart for Dublin pass rates using ploty 
bc_dublin = px.bar(
    dataset_cleaned,
    x='Month',
    y='Co. Dublin',
    title="Co.Dublin Pass Rates",
    color_discrete_sequence=['navy']  )
#Creates bar chart for Galway pass rates using ploty 
bc_galway = px.bar(
    dataset_cleaned,
    x='Month',
    y='Co. Galway',
    title="Co.Galway Pass Rates",
    color_discrete_sequence=['navy'] )
#creates bar chart for Donegal pass rates using ploty 
bc_donegal = px.bar(
    dataset_cleaned,
    x='Month',
    y='Co. Donegal',
    title="Co.Donegal Pass Rates",
    color_discrete_sequence=['navy'])
#Concerts bar charts to html
bc_dublin_html = bc_dublin.to_html(full_html=False, include_plotlyjs="cdn")
bc_galway_html = bc_galway.to_html(full_html=False, include_plotlyjs="cdn")
bc_donegal_html = bc_donegal.to_html(full_html=False, include_plotlyjs="cdn")
#transforms data for  the line chart 
data_long = dataset_cleaned.melt(
    id_vars=['Month'],
    value_vars=[col for col in dataset_cleaned.columns if col != 'Month'],
    var_name="Variable",
    value_name="Value")
#Creates a line chart for all counties pass rates           
line_chart = px.line(
    data_long,
    x='Month',
    y='Value',
    color="Variable",
    title="Line Chart",
    labels={                 
        'Value': "Pass Rate Comparison", 
        'Variable': "Counties" })

#creates a scatter plot to show the relationship between county Dublin and Galway
scatter_plot = px.scatter(
    dataset_cleaned,
    x='Co. Dublin',
    y='Co. Galway',
    title="Dublin  and Galway Passs Rate Relationship",
    labels={'Co. Dublin': "Dublin Pass Rate", 'Co. Galway': "Galway Pass Rate"} ) 

#Reshape data for scatter plot
data_long_scatter = dataset_cleaned.melt(
    id_vars=["Month"],
    value_vars=[col for col in dataset_cleaned.columns if col != 'Month'], 
    var_name="County",
    value_name="Value" )
#creates scatter plot to compare all counties
scatter_plot_2 = px.scatter(
    data_long_scatter,
    x='Month',
    y='Value',
    color='County',
    title="Pass Rate Comparison", )
#Converts line chart to html
line_chart_html = line_chart.to_html(full_html=False, include_plotlyjs="cdn")
#Converts scatter plot to HTML
scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")
#converts scatter plot to html 
scatter_plot_2_html = scatter_plot_2.to_html(full_html=False, include_plotlyjs="cdn")
#displays all graphs
"""
bc_dublin.show()
bc_galway.show()
bc_donegal.show()
line_chart.show()
scatter_plot.show()
scatter_plot_2.show()
"""
#sFlask application setup
app = Flask(__name__)
#routes flask to home.html
@app.route('/')
def home():
    return render_template(
        'home.html',
        bc_dublin=bc_dublin_html,
        bc_galway=bc_galway_html,
        bc_donegal=bc_donegal_html,
        line_chart=line_chart_html,
        scatter_plot=scatter_plot_html,
        scatter_plot_2=scatter_plot_2_html )

#routes flask to survey.html
@app.route('/survey') 
def survey():
    
   return render_template('survey.html')

@app.route('/recommendations')
def recommendations():
    return render_template(
        'recommendations.html',
        bc_dublin=bc_dublin_html,
        bc_galway=bc_galway_html,
        bc_donegal=bc_donegal_html )

#Runs flask  
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5001, debug=False)