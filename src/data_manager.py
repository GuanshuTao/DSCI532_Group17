# authors: Yuanzhe Marco Ma, Sicheng Sun, Guanshu Tao, Yuan Xiong
# date: 2021-01-23
import pandas as pd
import numpy as np
import altair as alt
from numerize import numerize 


"""
Class for data wrangling
Makes table, plots and map as well as update
"""
class DataManager():

    # Retreieves data
    def get_data(self):
        df = pd.read_csv('data/processed/processed_data.csv', index_col=0)
        return df

    # Makes initial table, land-on page
    #
    # Input:
    #     data : dataframe
    def make_table(self, data):
        table = data[['Name', 'Nationality', 'Age', 'Value(€)', 'Overall']]
        table = table.sort_values('Overall', ascending=False)[:15]
        table['Ranking'] = np.arange(table.shape[0]) + 1
        return table

    # Makes charts, including both bar-plots and scatter-plot
    #
    # Inputs:
    #     data : dataframe
    #     by : string, rank-by column selected
    #     ascending : boolean
    #     show_n : top n number of bars shown
    # Returns:
    #     bar-plot : altair chart, by Nationality
    #     bar-plot : altair chart, by Club
    #     scatter-plot : altair chart, rank-by column vs 'Overall'
    def plot_altair(self, data, by='Overall', ascending=False, show_n=10):
        df_nation = data.groupby('Nationality').agg({by: 'mean'}).round(2).reset_index()
        df_nation = df_nation.sort_values(by, ascending=ascending)[:show_n]
        nation_chart = alt.Chart(df_nation).mark_bar(color='lightslategrey').encode(
            alt.X('Nationality', sort='-y'),
            alt.Y(by),
            tooltip=alt.Tooltip(by)).properties(
                height=150,
                width=200)

        df_club = data.groupby('Club').agg({by: 'mean'}).round(2).reset_index()
        df_club = df_club.sort_values(by, ascending=ascending)[:show_n]
        club_chart = alt.Chart(df_club).mark_bar(color='lightslategrey').encode(
            alt.X('Club', sort='-y'),
            alt.Y(by),
            tooltip=alt.Tooltip(by)).properties(
                height=150,
                width=200)

        alt.data_transformers.disable_max_rows()
        scatter = alt.Chart(data).mark_circle(opacity=0.5, size=20, color='lightslategrey').encode(
            alt.X(by, scale=alt.Scale(zero=False)),
            alt.Y('Overall', scale=alt.Scale(zero=False))
        ).properties(
            height=220,
            width=200,
            title='Scatterplot of Rank-by Attribute vs Overall\n'
        )

        return nation_chart, club_chart, scatter

    # Makes histogram of the rank-by attribute
    #
    # Inputs:
    #     data : dataframe
    #     by : string, rank-by attribute selected
    #     order : boolean, ranking order
    # Returns:
    #     histogram : altair chart
    def plot_histo(self, data, by='Overall', order=False):
        df = data.sort_values(by, ascending=order)
        df['Ranking'] = np.linspace(1, len(df), len(df))

        alt.data_transformers.disable_max_rows()
        chart = alt.Chart(df).mark_bar(color='lightslategrey').encode(
            x=alt.X(by, bin=alt.Bin(maxbins=50), title=by),
            y=alt.Y('count()', scale=alt.Scale(zero=False)),
            tooltip=alt.Tooltip(by)
        ).properties(
            width=550,
            height=100,
            title='Histogram of Rank-by Attribute'
        )
        return chart

    # Updates table from given parameters
    #
    # Inputs:
    #     df : dataframe, processed dataset
    #     by : str, column to sort by
    #     order : bool, determines ascending or not
    #     cols : list(str), columns to include in table
    #     filter_natn : str, column to filter Nationality on
    #     filter_club : str, column to filter Club on
    #
    # returns: 
    #     table : dataframe, top 15 rows of the sorted dataset
    def update_table(self, data, by, order, cols,
                     filter_cont, filter_club, slider_update):

        # column conditions
        # 1. by (sort by) column must be present
        # 2. player Name must be present
        if not(by in cols):
            cols.append(by)
        if not('Name' in cols):
            cols.append('Name')

        # update table
        if filter_cont:
            data = data[data['Continent'] == filter_cont]
        if filter_club:
            data = data[data['Club'] == filter_club]
        table = data[cols]
        table = table.sort_values(by=by, ascending=False)
        table['Ranking'] = np.arange(table.shape[0]) + 1
        table_length = table.shape[0] # before trim
        table = table.sort_values(by='Ranking', ascending=order)[slider_update - 1: slider_update + 14]
        
        # format big number to human readable forms
        if 'Value(€)' in cols:
            table['Value(€)'] = table['Value(€)'].map(numerize.numerize)
        if 'Wage(€)' in cols:
            table['Wage(€)'] = table['Wage(€)'].map(numerize.numerize)

        # Re-arrange columns
        cols.append('Ranking')
        cols.insert(0, cols.pop(cols.index('Name')))
        cols.insert(0, cols.pop(cols.index('Ranking')))
        table = table[cols]
        return table, table_length
    
    # Prepares a dataframe for map widget
    #
    # Inputs:
    #     data : dataframe
    # Returns:
    #     dataframe : dataframe for making the map
    def prepare_map(data):
        df_country = data.groupby(['Nationality']).mean().round(2).reset_index()
        code_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
        df_country_code = df_country.merge(code_df, left_on='Nationality', right_on='COUNTRY', how='left')

        return(df_country_code)
