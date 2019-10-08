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

# testing URLs
/api/results?date=2012-04-15
/api/results/2011030221/teams