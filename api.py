from flask import Flask, jsonify, abort
import pandas as pd

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
    gs = pd.read_csv("./game_goalie_stats")
    return gs

def load_game_skater_stats():
    ss = pd.read_csv("./game_skater_stats.csv")
    return ss

def load_game_teams_stats():
    ts = pd.read_csv("./game_teams_stats.csv")
    return ts



#global variables
team_data = load_teams_data()
game_data = load_game_data()
game_teams_stats = load_game_teams_stats()
game_goalie_stats = load_game_goalie_stats()
game_skater_stats = load_game_skater_stats()
print("successfully loaded teams data")


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


if __name__ == '__main__':
    app.run(debug=True)
