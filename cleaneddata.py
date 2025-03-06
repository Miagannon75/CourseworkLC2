import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template

import plotly.express as px

data = pd.read_csv('Data.csv')

data['Month'] = pd.to_datetime(data['Month'] + ' 01', format='%Y %B %d')
data.sort_values(by='Month', inplace=True)
data.columns = data.columns.str.strip().str.lower()
changed_data = data.pivot_table(index='month',
                            columns='county',
                            values='value',
                            #columns='county',  
                            aggfunc='mean')


changed_data.columns = [f"{col} pass rate" for col in changed_data.columns]
changed_data.reset_index(inplace=True)
changed_data['month'] = changed_data['month'].dt.strftime('%d-%m-%Y')
changed_data.to_csv('cleaneddata.csv', index=False)

numeric_cols = changed_data.columns[1:] 

data = pd.read_csv('cleaneddata.csv')
print(data.columns)
stats_dictionary = {}


for col in numeric_cols:
    stats_data = changed_data[col].dropna() 
    stats_dictionary[col] = {
        'Mean': stats_data.mean(),
        'Median': stats_data.median(),
        'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
        'Range': stats_data.max() - stats_data.min()
    }


statistics_df = pd.DataFrame(stats_dictionary).T

statistics_df.to_csv('statistics.csv', index=True)


print("Statistics DataFrame:")
print(statistics_df)

bar_chart_dublin = px.bar(
    changed_data,
    x='month',
    y='Co. Dublin pass rate',
    title="Co.Dublin Pass Rates",
    labels={'month': 'month', 'Co. Dublin pass rate' : 'Co. Dublin pass rate'}
)

bar_chart_galway = px.bar(
    changed_data,
    x='month',
    y='Co. Galway pass rate',
    title="Co.Galway Pass Rates",
    labels={'month': 'month', 'Co. Galway pass rate': 'Co. Galway pass rate'}

)

bar_chart_donegal = px.bar(
    changed_data,
    x='month',
    y='Co. Donegal pass rate',
    title="Co.Donegal Pass Rates",
    labels={'month': 'month', 'Co. Donegal pass rate': 'Co. Donegal pass rate'}

)

bar_chart_dublin_html = bar_chart_dublin.to_html(full_html=False, include_plotlyjs="cdn")
bar_chart_galway_html = bar_chart_galway.to_html(full_html=False, include_plotlyjs="cdn")
bar_chart_donegal_html = bar_chart_donegal.to_html(full_html=False, include_plotlyjs="cdn")

data_long = data.melt(
    id_vars=['month'],
    value_vars=[col for col in data.columns if col !='month'],
    var_name="Variable",
    value_name="Value"
)
           
line_chart = px.line(
    data_long,
    x='month',
    y='Value',
    color="Variable",
    title="Line Chart",
    labels={                
        'month': "month", 
        'Value': "Pass Rate Comparison", 
        'Variable': "Counties" 
    }
)
line_chart_html = line_chart.to_html(full_html=False, include_plotlyjs="cdn")

scatter_plot = px.scatter(
    changed_data,
    x='Co. Dublin pass rate',
    y='Co. Galway pass rate',
    title="Dublin  and Galway Passs Rate Relationship",
    labels={data.columns[3]: "Values"}
)
scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")

data_long_scatter = data.melt(
    id_vars=["month"],
    value_vars=[data.columns[1], data.columns[2], data.columns[3]],  # Make sure column 4 is Co.Kildare
    var_name="County",
    value_name="Value"
)

scatter_plot_2 = px.scatter(
    data_long_scatter,
    x='month',
    y='Value',
    color='County',
    title="Pass Rate Comparison",
    labels={'month': 'Month', 'Value': 'Values', 'County': 'County'}
)


scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")


scatter_plot_2_html = scatter_plot_2.to_html(full_html=False, include_plotlyjs="cdn")

"""
bar_chart_dublin.show()
bar_chart_galway.show()
bar_chart_donegal.show()
line_chart.show()
scatter_plot.show()
scatter_plot_2.show()
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'home.html',
        bar_chart_dublin=bar_chart_dublin_html,
        bar_chart_galway=bar_chart_galway_html,
        bar_chart_donegal=bar_chart_donegal_html,
        line_chart=line_chart_html,
        scatter_plot=scatter_plot_html,
        scatter_plot_2=scatter_plot_2_html
    )


@app.route('/survey') 
def survey():
    
   return render_template('survey.html', )
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
