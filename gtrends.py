import numpy as np
import pandas as pd
import yaml
from pytrends.request import TrendReq
from datetime import timedelta

# Connects to Google

def get_weekly_search_interest_df():

    with open('keywords.yaml', 'r') as f:
        keyword_dict = yaml.load(f)

    # Create empty dataframe to append results to
    df = pd.DataFrame(columns=['searchInterest','isPartial','keyword'])

    # Change the dict below to get output for different teams
    for keyword in keyword_dict["event_type"]["nba"]["short_name"]:
    # for keyword in keyword_dict["event_type"]["nba"]["short_name"]:

        df = df.append(make_trends_call(keyword))

    # Remove index, rename "index" column to "week", drop all partial incomplete weeks
    df.reset_index(inplace=True)
    df.rename(columns={'index': "week"}, inplace=True)
    df = df.query('isPartial == "False"')

    return df


def make_trends_call(keyword):
    pytrend = TrendReq()
    kw_list = []
    # Add keyword to an array for the request
    kw_list.append(keyword)
    print "Pulling trends for ", keyword

    # Pulls trends data for a given keyword using pytrends library
    pytrend.build_payload(kw_list)
    interest_over_time_df = pytrend.interest_over_time()

    # Add keyword to the dataframe for each row
    kw_df = np.repeat(keyword, interest_over_time_df.shape[0])
    interest_over_time_df['keyword'] = kw_df

    interest_over_time_df.rename(index=str, columns={keyword: "searchInterest"}, inplace=True)

    return interest_over_time_df


def convert_weekly_df_to_daily_df(weekly_df):
    # Convert week to datetime object
    weekly_df['week'] = pd.to_datetime(weekly_df['week'])
    daily_df = pd.DataFrame(columns=['date', 'searchInterest','keyword'])
    days_in_week = 7

    # Iterate through every row in the trends dataframe and turn weekly data into daily data
    # Assumes same exact search interest for every day in a given week
    for index, row in weekly_df.iterrows():
        for x in range(days_in_week):
            daily_df.loc[index * days_in_week + x] = [row['week'] + timedelta(days=x), row['searchInterest'], row['keyword']]

    return daily_df
