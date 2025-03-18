import pandas as pd
import datetime


def read_my_excel_file(excel_name: str, column_index: int):

    abc = excel_name
    if excel_name[-5:] != ".xlsx":
        abc = str(excel_name + ".xlsx")

    return pd.read_excel(abc, index_col=column_index)


def create_fixtures_list_for_day_x_from_today(dataframe, analysis_days_from_today: int) -> list:
    today = datetime.date.today()
    analyzed_day = str(today + datetime.timedelta(days=analysis_days_from_today))
    print("analysis day is ", analyzed_day)
    df_inter_list = dataframe[dataframe['Fixture Date'] == analyzed_day]

    return df_inter_list['Fixture ID'].to_list()
