import numpy as np
import pandas as pd
import gsheets
import gtrends
from datetime import timedelta

def main():
    daily_df = gtrends.get_daily_search_interest()
    #This is VERY slow. Need to figure out how to speed up. Ideally pandas or numpy has some more built in functions I can take advantage of

    # Save output to CSV
    daily_df.to_csv('google_trends-weekly.csv', index=True)
    print "Data saved to csv"

    # had to rewrite this to a string because of some stupid json serialization issue that I was too lazy to try and fix
    # might want to find a workaround because sheet won't be formatted to date (also could probably just call function for this)
    daily_df['date'] = daily_df['date'].dt.strftime('%Y-%m-%d')

    # should make sheet name global and maybe rename it
    gsheets.write_df_to_sheet('Trends Data Raw', daily_df)

if __name__ == '__main__':
    main()
