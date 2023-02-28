import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('/home/olawale/Desktop/freecodecamp/time_series_visualizer/fcc-forum-pageviews.csv', index_col=0, parse_dates=True)

# Clean data
df = df[(df.value > df.value.quantile(0.025)) & (df.value < df.value.quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    linePlot = df.plot(figsize=(15,6), legend=False, title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019", color='r')
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    
    fig = linePlot.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Create month and year columns
    df_bar['month'] = pd.DatetimeIndex(df_bar.index).month_name()
    df_bar['year'] = pd.DatetimeIndex(df_bar.index).year

    # Order the monnth for each year from January to December
    months = [
      "January", "February",
       "March", "April", "May",
       "June", "July", "August",
       "September",  "October",
       "November", "December"
    ]

    df_bar.month = pd.Categorical(
              df_bar.month,
              categories=months,
              ordered=True
      )
    # Create a pivot of the dataframe by year and month
    df_bar_pivot = pd.pivot_table(df_bar, values="value", index='year', columns='month', aggfunc="mean", fill_value=0)
  
    # Draw bar plot
    barP = df_bar_pivot.plot(kind='bar', figsize=(8, 8), ylabel='Average Page Views', xlabel='Years')
    barP.legend().set_title('Months')

    fig = barP.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(24,8))
    
    ax1 = sns.boxplot(y="value", x= "year", data=df_box,  orient='v' , ax=axes[0])
    ax2 = sns.boxplot(y="value", x= "month", data=df_box.sort_values('month', key = lambda x : pd.to_datetime(x, format='%b').dt.month),  orient='v' , ax=axes[1])
    
    ax1.set(xlabel="Year")
    ax1.set(ylabel="Page Views")
    ax1.set(title="Year-wise Box Plot (Trend)")
    ax1.set_ylim(0, 200000)
    ax1.set_yticks(range(0, 220000, 20000))
    
    ax2.set(xlabel="Month")
    ax2.set(ylabel="Page Views")
    ax2.set(title="Month-wise Box Plot (Seasonality)")
    ax2.set_ylim(0, 200000)
    ax2.set_yticks(range(0, 220000, 20000))
  
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
