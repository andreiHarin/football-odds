

def create_list_of_betting_companies(data_odds):
    """
    :param data_odds:
    :rtype: list
    :return: list_of_potential_bet_companies
    """
    list_of_potential_bet_companies = []

    if len(data_odds['response']) != 0:
        for i in range(len(data_odds['response'][0]['bookmakers'])):
            try:
                a = data_odds['response'][0]['bookmakers'][i]['name']
                list_of_potential_bet_companies.append(a)
            except ValueError as e:
                print(f"Betting company index: {e}")

    return list_of_potential_bet_companies


def add_odds_to_dict(data_odds, list_of_potential_bet_companies, dict_odds) -> dict:
    if 'Bet365' in list_of_potential_bet_companies:
        obtain_index_of_bet365 = list_of_potential_bet_companies.index('Bet365')
        dict_odds[int(data_odds['parameters']['fixture'])] = data_odds['response'][0]['bookmakers'][obtain_index_of_bet365]['bets'][0]['values']

    elif 'Marathonbet' in list_of_potential_bet_companies:
        obtain_index_of_marathonbet = list_of_potential_bet_companies.index('Marathonbet')
        dict_odds[int(data_odds['parameters']['fixture'])] = data_odds['response'][0]['bookmakers'][obtain_index_of_marathonbet]['bets'][0]['values']
    else:
        dict_odds[int(data_odds['parameters']['fixture'])] = data_odds['response'][0]['bookmakers'][0]['bets'][0]['values']

    return dict_odds
