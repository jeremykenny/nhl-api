# Assignment1
The data files used by this project can be obtained from https://www.kaggle.com/martinellis/nhl-game-data. Place the csv files in the root directory of this repository.
# resource requirement
Game Results Summary
# user story
As a casual fan, I want to see the scores of recent NHL games so I can see who won.
# acceptance criteria
Ability to specify date to provide game results summaries for.
For each game, provide:
    - Hyperlink to corresponding Game Result Details resource
    - Hyperlink to corresponding Game Player Stats resource
    - How game ended (normal, overtime, etc)
    - For each team:
        - Hyperlink to team resource
        - abbreviation of team name 
        - number of goals scored.
# resource description
URL = /api/results?date={YYY-MM-DD} (e.g. /api/results?date=2012-04-15)
This resource provides summaries for all games that occured on the specified date. 
The resource includes one game object for each game that occurred on that date. Game objects are labelled by their NHL-provided id. Each game object contains the following elements:
    away_goals: Number of goals scored by the away team.
    away_team: Object containing information about the away team.
    home_goals: Number of goals scored by the home team.
    home_team: Object containing information about the home team.
    outcome: "FINAL" if the game ended normally or "FINAL/OT" if the game ended in overtime.
    player_stats: A hyperlink to the Game Player Stats resource for this game.
    team_stats: A hyperlink to the Game Results Details resource for this game.
The away_team and home_team objects each contain the following elements:
    URL: A hyperlink to a hypothetical api resource for the team
    abbreviation: The three letter abbreviation of the team's name
    team name: The name of the team
    city: The team's home city

Design rationale:
    My rationale for labelling the games by their NHL-provided id was to ensure that every game returned by a single request had a unique identifier. I considered labelling the games according to the teams for a more human-readable name (e.g. "Devils vs. Panthers"), but this would have left the possibility that two games could have the same name (e.g. if the Devils played against the Panthers twice in one day.)

    The home_team and away_team objects:
        I wanted the team information to act as a summary of the team's permanent profile. I felt that it should stay the same from game to game, so I kept the number of goals scored by a team separate as a separate object.

        I provided a hyperlink to a hypothetical team resource as a convenient way for users to find additional information about the team.

        While the marquee image given in the handout does not include the teams' names and cities, I chose to include them in this resource. Rather than limit my API to be used by the specific given marquee design, I included information that similar applications might include or exclude at their own discretion. The processing trade-off of including this is miniscule as this function already has to access the team data table to retrieve the teams' abbreviations.

    I included a hyperlink to the Game Results Details, since viewing a game's details is a natural next step for a user to take after viewing the game summary.
    
    While most users would probably visit the Game Results Details before the Game Player Stats, I include the Player Stats URL here because it is a sister to the Game Results Details resource in the URL structure. This does not incur significant overhead as the function can construct the URL without joining additional tables.
    

# resource requirement
Game Results Details
# user story
As a stats junkie, I want detailed performance information for each team in a game so I can predict the winners of future games.
# acceptance criteria
Ability to specify game to provide result details for.
Provide hyperlink to Game Player Stats resource
For each team in the specified game, provide:
    - team name
    - Hyperlink to team resource
    - number of goals
    - number of shots
    - number of hits
    - number of penalty infraction minutes (PIM)
    - number of power play opportunities
    - number of power play goals
    - face-off win percentage
    - number of giveaways
    - number of takeaways
# resource decsription
URL = /api/results/{ID}/teams (e.g. /api/results/2011030221/teams)
This resource provides performance information for each team involved in a game.
The resource includes the following objects:
    away team: Object containing information about the away team.
    home team: Object containing information about the home team.
    player stats: A hyperlink to the Game Player Stats resource for this game.
The away team and home team objects each contain the following elements:
    team information: Basic information about the team. Contains:
        URL: A hyperlink to a hypothetical api resource for the team
        abbreviation: The three letter abbreviation of the team's name
        team name: The name of the team
        city: The team's home city
    team game results: Performance stats for this team in this game.
The team game results object contains the following elements:
    "face-off win percentage"
    "giveaways"
    "goals"
    "head_coach"
    "hits"
    "pim"
    "power play goals"
    "power play opportunities"
    "shots"
    "takeaways"

Design rationale:
    Because this resource provides more data per team than the Game Results Summary, I chose a more organized JSON structure for this part. I decided to nest all information pertaining to the home team in one object, and all information pertaining to the away team in another object. As before, I kept the teams' basic identifying information in a separate object from information pertaining to the teams' performance in particular games.

    This resource provides the same team information as is provided by the Game Results Summary. The team name and city are sufficient to identify a team, and users looking for additional information can follow the hyperlink to the team's profile page. The team's abbreviation does not strictly need to be included but does not cost additional overhead and is convenient for designers who may want to display it in their applications.

    The team game results objects contain almost all the data provided in game_team_stats.csv for each team in this game. They do not include:
        team_id or game_id: Not included because the user doesn't need to know them.
        HoA (home or away): Not included because it is already provided by the structure of the JSON object.
        settled_in: Not included as this information does not pertain to a specific team but to the game as a whole.
    I provided the remaining stats as they are all things a user might be interested in. I chose not to compute any additional stats for the sake of time and because I think the provided information is detailed enough for most people's purposes.

    Finally, I included a hyperlink to the Game Player Stats resource associated with this game. The purpose of this resource is to provide details about games, so devlopers accessing this resource may also want the additional details provided by the Game Player Stats resource. Providing a hyperlink here helps them explore the API and find data relevant to their purposes.

# resource requirement
Game Player Stats
# user story
As a fantasy hockey player, I want detailed performance information for each player in a game so I can track my fantasy hockey team's score.
# acceptance criteria
Ability to specify game to provide player stats for.
For each player in a game, provide:
    - player name
    - team
    - time on ice
    - goals
    - assists
    - shots
    - hits
    - power play goals
    - power play assists
    - penalty minutes
    - face-off wins
    - face-off taken
    - takeaways
    - giveaways
    - short handed goals
    - short handed assist
    - blocked
    - plus/minus
    - short handed time on ice
    - even time on ice
    If a goalie:
        - saves
        - power play saves
        - short handed saves
        - even shots against
        - power play shots against
        - save percentage
        - power play save percentage
        - even strength save percentage
# resource description
/api/results/{ID}/players (e.g. /api/results/2011030221/players)
This resource provides details about the performance of individual players in a game.
This resource includes a JSON object for each player in a game. Players are grouped into two categories, goalies and skaters (all non-goalies are considered skaters). Players are labelled by their names. Each player object contains:
    URL: a link to a hypothetical resource which could provide a profile of the player
    team: object containing information about the player's team.
    the player's stats for this game
The structure of the team object is the same as in the other two resources:
    URL: A link to a hypothetical api resource for the team
    abbreviation: The three letter abbreviation of the team's name
    team name: The name of the team
    city: The team's home city

Design rationale:
    I placed goalies in a separate group from non-goalies because goalies have stats that non-goalies do not (e.g. saves). This means their JSON objects have extra elements not found in those of normal skaters. Separating players into these categories lets developers accessing this resource be sure that all players within a category have the same JSON structure.

    I could have grouped players according to their teams, but chose not to based on the user story I wrote. Fantasy hockey players are interested in the performance of the players on their fantasy teams. The performances of specific players are of interest to this user, while the teams the players belong to is of lesser importance. Likewise, the performance of the team as a whole is generally not of interest to fantasy hockey players, which is why this resource does not provide a link to the Game Results Details resource. This decision resulted in some redundancy, as the team information summary is provided once for every player on a team. It also means developers who do want to list players according to their teams have to do so themselves.

# testing URLs
Working Game Results Summary URL with single result:
/api/results?date=2013-05-21

Working Game Results Summary URL with multiple results:
/api/results?date=2012-04-15

Game Results Summary URL with no results: 
/api/results?date=2030-05-10

Working Game Results Details URLs:
/api/results/2011030221/teams
/api/results/2012030235/teams

Working Game Player Stats URLs
/api/results/2011030221/players
/api/results/2012030235/players

