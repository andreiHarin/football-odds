import json
import http.client


def call_odds_api(fixture_id, api_header_info):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    conn.request("GET", f"/odds?fixture={fixture_id}", headers=api_header_info)
    res = conn.getresponse()
    print(f"status for fixture {fixture_id} is ", res.status)
    return res.read()


def call_team_stats_api(season_year, team_api_id, league_api_id, api_header_info):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    conn.request("GET", f"/teams/statistics?season={season_year}&team={team_api_id}&league={league_api_id}", headers=api_header_info)
    res = conn.getresponse()
    return res.read()


def bytes_to_json(byte_data):
    try:
        json_data = byte_data.decode('utf-8')  # Decode bytes to UTF-8 string
        json_object = json.loads(json_data)  # Parse JSON string into Python object
        return json_object
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Error converting bytes to JSON: {e}")
        return None

