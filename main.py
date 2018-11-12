import numpy as np
import pandas as pd
import gsheets
import gtrends
from datetime import timedelta

def main():
    daily_df = gtrends.get_daily_search_interest()
    print "Finished pulling Google Trends data"

    # Save output to CSV
    daily_df.to_csv('google_trends.csv', index=True)
    print "Data saved to csv"

    # had to rewrite this to a string because of some stupid json serialization issue that I was too lazy to try and fix
    daily_df['date'] = daily_df['date'].dt.strftime('%Y-%m-%d')

    # should make sheet name global and maybe rename it
    gsheets.write_df_to_sheet('Trends Data Raw', daily_df)

if __name__ == '__main__':
    main()
