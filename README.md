# Assignment1

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
This resource provides summaries for all games that occured on the specified date. Game objects are labelled by their NHL-provided id. Each game object contains the following elements:
    away_goals: Number of goals scored by the away team.
    away_team: Object representing the away team.
    home_goals: Number of goals scored by the home team.
    home_team: Object representing the home team.
    outcome: "FINAL" if the game ended normally or "FINAL/OT" if the game ended in overtime.
    player_stats: A hyperlink to the Game Player Stats resource for this game.
    team_stats: A hyperlink to the Game Results Details resource for this game.
The away_team and home_team objects each contain the following elements:
    URL: A hyperlink to a hypothetical api resource for the team
    abbreviation: The three letter abbreviation of the team's name
    team name: The name of the team
    city: The team's home city

Design rationale:
    My rationale for labelling the games by their NHL-provided id was to ensure that every game returned by a single request had a unique identifier. I considered labelling the games according to the teams (e.g. "Devils vs. Panthers") for a more human-readable name, but I this would have left the possibility that two games could have the same name (e.g. if the Devils played against the Panthers twice in one day.)

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

# testing URLs
/api/results?date=2012-04-15
/api/results/2011030221/teams
/api/results/2011030221/players