# authors: Yuanzhe Marco Ma, Sicheng Sun, Guanshu Tao, Yuan Xiong
# date: 2021-01-23
import pandas as pd
import numpy as np
import altair as alt


"""
Class for data wrangling
"""
class DataManager():

    # retreieve data
    def get_data(self):
        df = pd.read_csv('data/processed/processed_data.csv', index_col=0)
        return df

    # make initial table, land-on page
    def make_table(self, data):
        table = data[['Name', 'Nationality', 'Age', 'Value(€)', 'Overall']]
        table = table.sort_values('Overall', ascending=False)[:15]
        table['Ranking'] = np.arange(table.shape[0]) + 1
        return table

    # make initial charts, land-on page
    def plot_altair(self, data, by='Overall', ascending=False, show_n=10):
#         df_nation = data.groupby('Nationality').agg({by: 'mean'}).round(2).reset_index()
        df_nation = data.groupby('Nationality').agg({by: 'mean'}).round(4).reset_index()
        df_nation = df_nation.sort_values(by, ascending=ascending)[:show_n]
        nation_chart = alt.Chart(df_nation).mark_bar().encode(
            alt.X('Nationality', sort='-y'),
            alt.Y(by, scale=alt.Scale(domain=(70, 80))),
            tooltip = alt.Tooltip(by)).properties(
                height=150,
                width=200)

#         df_club = data.groupby('Club').agg({by: 'mean'}).round(2).reset_index()
        df_club = data.groupby('Club').agg({by: 'mean'}).round(4).reset_index()
        df_club = df_club.sort_values(by, ascending=ascending)[:show_n]
        club_chart = alt.Chart(df_club).mark_bar().encode(
            alt.X('Club', sort='-y'),
            alt.Y(by, scale=alt.Scale(domain=(75, 85))),
            tooltip = alt.Tooltip(by)).properties(
                height=150,
                width=200)


        alt.data_transformers.disable_max_rows()
        scatter = alt.Chart(data).mark_circle( opacity = 0.5, size=10 ).encode(
             alt.X(by),
             alt.Y('Overall')
         ).properties(
                 height=250,
                 width=300)



        return nation_chart, club_chart, scatter

    # plot histogram of ranked attribute
    def plot_histo(self, data, by='Overall', order=False):
        df = data.sort_values(by, ascending=order)
        df['Ranking'] = np.linspace(1, len(df), len(df))

        alt.data_transformers.disable_max_rows()
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(by, bin=alt.Bin(maxbins=50), title=by),
            y=alt.Y('count()', scale=alt.Scale(zero = False)),
            tooltip = alt.Tooltip(by)
        ).properties(
            width=450,
            height=100
        )
        return chart


    # Updates table from given parameters
    #
    # df : dataframe, processed dataset
    # by : str, column to sort by
    # order : bool, determines ascending or not
    # cols : list(str), columns to include in table
    # filter_natn: str, column to filter Nationality on
    # filter_club: str, column to filter Club on
    #
    # return : dataframe, top ten rows of the sorted dataset
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

        # Re-arrange columns
        cols.append('Ranking')
        cols.insert(0, cols.pop(cols.index('Name')))
        cols.insert(0, cols.pop(cols.index('Ranking')))
        table = table[cols]
        return table, table_length

