from API_call import call_odds_api, bytes_to_json, call_team_stats_api
from reading_db import read_my_excel_file, create_fixtures_list_for_day_x_from_today
from betting_info import add_odds_to_dict, create_list_of_betting_companies

from writing_in_db import write_back_into_excel
from email_information import email_information
from email_sending import connect_to_outlook, send_outlook_message
from Algoritm1 import calculate_algorithm1, compute_form

import time, datetime

header_api = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "9f00fc5a4c2caa958b2ed1375e038a80"
    }


if __name__ == "__main__":
    days_into_future = 2
#   reading data
    df = read_my_excel_file("ALL_Fixtures_for_leagues.xlsx", column_index=0)
    fixtures_list = create_fixtures_list_for_day_x_from_today(df, days_into_future)

    #fixtures_list = fixtures_list[:3]
    dict_of_info = {}
    print("list of fixtures: ", fixtures_list)
    print("total number of fixtures: ", len(fixtures_list))
    time.sleep(3)
    games_analyzed = 0
    teams_analyzed = 0

#   extracting data using API and constructing a dictionary which will be used then
    for y in fixtures_list:
        read_odds_api = call_odds_api(y, header_api)
        data_odds = bytes_to_json(read_odds_api)
        list_of_betting_info = create_list_of_betting_companies(data_odds)

        if len(data_odds['response']) != 0:
            add_odds_to_dict(data_odds, list_of_betting_info, dict_of_info)
        else:
            continue

        if games_analyzed % 9 == 8:
            time.sleep(65)
        games_analyzed += 1
        print(games_analyzed)

        if games_analyzed > 96:
            continue

    print('dict of info:', dict_of_info)
#   writing bet odds into excel file + doing the algorithm in there
    write_back_into_excel(df, dict_of_info)
    df.to_excel('ALL_Fixtures_for_leagues.xlsx')

#   preparing a new DF which will be sent via e-mail
    df_inv = df[df['Home Team Odds'].notnull()].copy()
    analysis_date = str(datetime.date.today() + datetime.timedelta(days=days_into_future))
    df_inv = df_inv[df_inv['Fixture Date'] == analysis_date]  # so that we send only relevant date via email

    if not df_inv.empty:
        df_inv['Algoritm1_inv'] = df_inv.apply(lambda x: calculate_algorithm1(x['Home Team Odds'], x['Away Team Odds']), axis=1)
        df_inv = df_inv[df_inv['Algoritm1_inv'] == 1]
    else:
        print("no data to be analysed, DF is empty")

#   store data somewhere or directly apply in the df as a column? best would be to write it in a dictionary with all info
#   maybe from that dictionary later I will use something more or maybe not

#   after last API, i need a pause before starting again api, because 10 calls for every minute!!!!
    time.sleep(60)

#   'Algoritm1_inv is created only when it has at least some data, so I would need to approach it with verifying =1 when not empty'
    for index, row in df_inv.iterrows():
        print(teams_analyzed, 'api for team id:', row['Home Team ID'], ' fixture id: ', row['Fixture ID'], 'league id', row['League ID'])

        read_team_api = call_team_stats_api(row['League Season'], row['Home Team ID'], row['League ID'], header_api)
        data_team = bytes_to_json(read_team_api)

#   this verification is not very needed, was set here because of a strange error which was starting new APIs,
#   but not wait 60 sec
        if type(data_team['response']) == dict:
            df_inv.loc[index, "Form"] = data_team['response']['form']
            #df_inv.loc[index, "Avg_For"] = str(data_team['response']['goals']['for']['average'])
            #df_inv.loc[index, "Avg_Against"] = str(data_team['response']['goals']['against']['average'])

        if teams_analyzed % 9 == 8:
            time.sleep(65)
        teams_analyzed += 1
        time.sleep(2)

    if not df_inv.empty:
        df_inv['Form Value'] = df_inv.apply(lambda x: '__' + str(round(compute_form(x['Form'])*100)) + '%', axis=1)
        #df_inv['Form Value sort'] = df_inv.apply(lambda x: round(compute_form(x['Form'])), axis=1)
        #df_inv = df_inv.sort_values(by=['Form Value sort'], ascending=False)
    else:
        print("no data to be analysed, DF is empty")


    info_to_send = email_information(df_inv, days_into_future)

    list_of_emails = ['andrei.harin@gmail.com', 'aaaaaaaa@gmail.com']
    EMAIL_SENDER = connect_to_outlook()

    for receiver in list_of_emails:
        send_outlook_message(EMAIL_SENDER, receiver, info_to_send)

    EMAIL_SENDER.quit()

