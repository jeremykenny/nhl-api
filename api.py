from flask import Flask, jsonify, abort, request
import pandas as pd
import numpy as np

app = Flask(__name__)


# sample code for loading the team_info.csv file into a Pandas data frame.  Repeat as
# necessary for other files
def load_teams_data():
    td = pd.read_csv("./team_info.csv")
    return td

def load_game_data():
    gd = pd.read_csv("./game.csv")
    return gd

def load_game_goalie_stats():
    gs = pd.read_csv("./game_goalie_stats.csv")
    return gs

def load_game_skater_stats():
    ss = pd.read_csv("./game_skater_stats.csv")
    return ss

def load_game_teams_stats():
    ts = pd.read_csv("./game_teams_stats.csv")
    return ts

def load_player_data():
    pld = pd.read_csv("./player_info.csv")
    return pld



#global variables
team_data = load_teams_data()
game_data = load_game_data()
game_teams_stats = load_game_teams_stats()
game_goalie_stats = load_game_goalie_stats()
game_skater_stats = load_game_skater_stats()
player_data = load_player_data()
#print("successfully loaded teams data")

def team_summary(team_id):
    '''
    Return a dictionary representing a summary of a team.
    Summary includes abbreviation, name, and URL.
    Error handling deferred to caller.

    Args: 
    team_id: string ID of the team
    '''
    teams = team_data[team_data["team_id"] == int(team_id)]
    team = teams.iloc[0]
    team = team.drop(["team_id","franchiseId","shortName","link"])
    team = team.rename(index={"teamName": "team name"})
    
    teamJSON = team.to_dict()
    teamJSON["URL"] = "/api/teams/" + team["abbreviation"]
    return teamJSON

def get_team_summaries(ids):
    return [team_summary(team_id) for team_id in ids.values]

def make_hyperlink(ids, str1, str2):
    return [str1 + str(game_id) + str2 for game_id in ids.values]

def format_outcomes(outcome):
    return "FINAL/OT" if "OT" in outcome else "FINAL"

@app.route('/')
def index():
    return "NHL API"


# route mapping for HTTP GET on /api/schedule/TOR
@app.route('/api/teams/<string:team_id>', methods=['GET'])
def get_task(team_id):
    # fetch sub dataframe for all teams (hopefully 1) where abbreviation=team_id
    teams = team_data[team_data["abbreviation"] == team_id]

    # return 404 if there isn't one team
    if teams.shape[0] < 1:
        abort(404)

    # get first team
    team = teams.iloc[0]

    # return customized JSON structure in lieu of Pandas Dataframe to_json method
    teamJSON = {"abbreviation": team["abbreviation"],
                "city": team["shortName"],
                "name": team["teamName"]}

    # jsonify easly converts maps to JSON strings
    return jsonify(teamJSON)

# Game Results Summary
@app.route('/api/results', methods=['GET'])
def get_game_summaries():
    date = request.args.get('date')
    
    # fetch sub dataframe for all games where date portion of date_time=date
    games = game_data[game_data["date_time"] == date]
    
    # return 404 if there isn't one game
    
    if games.shape[0] < 1:
        abort(404)


    games = games.drop(["season", "type", "date_time", "date_time_GMT", \
    "home_rink_side_start", "venue", "venue_link", "venue_time_zone_id", "venue_time_zone_tz", "venue_time_zone_offset"], axis=1)
    #exception can occur here if an entry in game.csv references a nonexistent team id
    try:
        games = games.assign(home_team=lambda g:get_team_summaries(g['home_team_id']))
        games = games.assign(away_team=lambda g:get_team_summaries(g['away_team_id']))
    except Exception:
        abort(500)
    games = games.drop(["home_team_id", "away_team_id"], axis=1)
    # Change format of outcomes
    games['outcome'] = games['outcome'].map(format_outcomes)
    # URLs
    games = games.assign(team_stats=lambda g:make_hyperlink(g['game_id'], "/api/results/", "/teams"))
    games = games.assign(player_stats=lambda g:make_hyperlink(g['game_id'], "/api/results/", "/players"))
    games.set_index("game_id", inplace=True)
    games.rename(columns={"team_stats": "team stats", "player_stats": "player stats", "home_team": "home team", "away_team": "away team"})
    return jsonify(games.to_dict(orient="index"))
    
    


# Game Results Details
@app.route('/api/results/<string:game_id>/teams')
def get_game_teams_details(game_id):
    # fetch sub dataframe for all games (hopefully 2) where game_id=game_id
    games = game_teams_stats[game_teams_stats["game_id"] == int(game_id)]

    #return 404 if there isn't one game
    if games.shape[0] < 1:
        abort(404)
    # return 500 if there are more than two games
    if games.shape[0] > 2:
        abort(500)

    # get games
    game1 = games.iloc[0]
    game2 = games.iloc[1]
    home = game1 if game1.HoA == "home" else game2
    away = game2 if game2.HoA == "away" else game1
    results = { "home team": team_summary(home['team_id']),
                "away team": team_summary(away['team_id'])}
    home = home.drop(["game_id","team_id","HoA","won","settled_in","head_coach"])
    away = away.drop(["game_id","team_id","HoA","won","settled_in","head_coach"])
    home = home.rename({"powerPlayOpportunities": "power play opportunities","powerPlayGoals": "power play goals","faceOffWinPercentage": "face-off win percentage"})
    away = away.rename({"powerPlayOpportunities": "power play opportunities","powerPlayGoals": "power play goals","faceOffWinPercentage": "face-off win percentage"})
    results["home team results"] = home.to_dict()
    results["away team results"] = away.to_dict()
    # Something above causes Pandas to convert numeric entries to numpy types.
    # Flask cannot jsonify numpy types, so we need to convert numeric values to python native types
    for key, dictionary in results.items():
        if (isinstance(dictionary, dict)):
            for key2, val in dictionary.items():
                if isinstance(val, np.generic):
                    # convert to python native type
                    results[key][key2] = val.item()
                # This json structure is only two levels deep, so this is good enough.
                # A more general solution should use a recursive function.
    results["player stats"] = "/api/results/" + game_id + "/players"

    return jsonify(results)


# Game Player Stats
@app.route('/api/results/<string:game_id>/players')
def get_game_players_details(game_id):
    # fetch sub dataframe for all games where game_id=game_id
    games = game_skater_stats[game_skater_stats["game_id"] == int(game_id)]

    #return 404 if there isn't one game
    if games.shape[0] < 1:
        abort(404)

    # games should have one entry for each player in the game, except for goalies
    game_player_stats = games.merge(player_data, on="player_id")
    game_player_stats = game_player_stats.assign(full_name=lambda gps: gps['firstName'] +" " + gps['lastName'])
    game_player_stats.set_index("full_name", inplace=True)
    game_player_stats = game_player_stats.assign(team=lambda g:get_team_summaries(g['team_id']))
    game_player_stats = game_player_stats.assign(URL=lambda g:make_hyperlink(g['player_id'], "/api/players/", ""))
    game_player_stats = game_player_stats.drop(["team_id", "firstName", "lastName", "game_id","player_id","nationality","birthCity","primaryPosition","birthDate","link"], axis=1)

    # as above, this time for goalies
    games_goalies = game_goalie_stats[game_goalie_stats["game_id"] == int(game_id)]
    if games_goalies.shape[0] < 1:
        abort(404)

    goalie_stats = games_goalies.merge(player_data, on="player_id")
    goalie_stats = goalie_stats.assign(full_name=lambda gs: gs['firstName'] +" " + gs['lastName'])
    goalie_stats.set_index("full_name", inplace=True)
    goalie_stats = goalie_stats.assign(team=lambda g:get_team_summaries(g['team_id']))
    goalie_stats = goalie_stats.assign(URL=lambda g:make_hyperlink(g['player_id'], "/api/players/", ""))
    goalie_stats = goalie_stats.drop(["team_id", "decision", "firstName", "lastName", "game_id","player_id","nationality","birthCity","primaryPosition","birthDate","link"], axis=1)

    skater_dict = game_player_stats.to_dict(orient="index")
    goalie_dict = goalie_stats.to_dict(orient="index")


    statsJSON = {   "skaters": skater_dict,
                    "goalies": goalie_dict}
    return jsonify(statsJSON)
    

if __name__ == '__main__':
    app.run(debug=True)
