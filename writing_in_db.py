from Algoritm1 import calculate_algorithm1


def write_back_into_excel(df, odds_dictionary):
    for index, row in df.iterrows():
        if int(row['Fixture ID']) in odds_dictionary:
            abc = row['Fixture ID']
            df.loc[index, 'Home Team Odds'] = odds_dictionary[abc][0]['odd']
            df.loc[index, 'Away Team Odds'] = odds_dictionary[abc][2]['odd']
            df.loc[index, 'Algoritm1'] = calculate_algorithm1(df.loc[index, 'Home Team Odds'], df.loc[index, 'Away Team Odds'])
