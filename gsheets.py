import pygsheets

# should replace this with sheet_id cause errors
def write_df_to_sheet(sheet_name, df):

    # ensure that our dataframe isn't larger than the google sheets max (2,000,000).
    if df.shape[0] * df.shape[1] > 18000000:
        print "Number of records is too large for Google Sheets to handle. Please reduce the number of keywords or timeframe"
        return

    # overwrite max cell write limit. defaults to 50,000. the +1 accounts for the headers
    pygsheets.client.GOOGLE_SHEET_CELL_UPDATES_LIMIT = df.shape[0] * (df.shape[1] + 1)

    # auth things. will need to go through oauth if it's your first time using
    gc = pygsheets.authorize()

    # open sheet and add dataframe to sheet
    sh = gc.open_by_key('')
    f = sh.worksheet('title', sheet_name)
    f.clear()
    f.set_dataframe(df,(1, 1))
