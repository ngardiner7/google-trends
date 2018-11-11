import numpy as np
import pandas as pd
import yaml
from pytrends.request import TrendReq
from datetime import timedelta

# Connects to Google

def get_daily_search_interest():

    with open('keywords.yaml', 'r') as f:
        keyword_dict = yaml.load(f)

    # Create empty dataframe to append results to
    df = pd.DataFrame(columns=['date','searchInterest','isPartial','keyword'])

    # Change the dict below to get output for different teams
    for keyword in keyword_dict["event_type"]["nba"]["short_name"]:

        df = df.append(make_trends_call(keyword))

    # Remove index, rename "index" column to "week", drop all partial incomplete weeks
    # df.reset_index(inplace=True)
    # df.rename(columns={'index': "week"}, inplace=True)
    df.drop(columns=['isPartial'], inplace=True)
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

    # should be able to clena up the crap below a bit
    interest_over_time_df.rename(index=str, columns={keyword: "searchInterest"}, inplace=True)
    interest_over_time_df.reset_index(inplace=True)

    interest_over_time_df['date'] = pd.to_datetime(interest_over_time_df['date'], format='%Y-%m-%d')
    daily_df = interest_over_time_df.set_index('date').resample('D').ffill().reset_index()

    return daily_df
