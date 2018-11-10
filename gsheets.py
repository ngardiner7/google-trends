import pygsheets

# should replace this with sheet_id cause errors
def write_df_to_sheet(sheet_name, df):
    # overwrite max cell write limit because I was hitting max. Should probably make this dynamic based on df size
    pygsheets.client.GOOGLE_SHEET_CELL_UPDATES_LIMIT = 200000
    # auth things. will need to go through oauth if it's your first time using
    gc = pygsheets.authorize()

    # open sheets and add dataframe
    sh = gc.open_by_key('')
    f = sh.worksheet('title', sheet_name)
    f.clear()
    f.set_dataframe(df,(1, 1))
