# Tennis Match Simulation
For my final project I created a streamlit app for a user to simulate tennis matches between the top 10 ATP Players on 04 Feb 2025.

## Objective
This project is for users interested in tennis to match up 2 Players by selecting their names, the surface and the tournament type.

## Methods 
For the simulation I decided to go with the Monte-Carlo method, because it considers the winning probability for each player and also the aspect of uncertainty (in tennis for instance weather conditions). For calculating the winning probability I created myown database focusing on Elo Points and key point statistics wheightes by all combinations of surface and tournament type:
- Why Elo Points? In contrast to the ATP Ranking system the Elo Ranking system gives insights on how good a player has played over the past year.
- Why Key Point statistics? In my opinion in key situations all pillars of successful tennis must come into place:  physical fitness, technique and mental strength. Those key points include: Aces, Double Faults, Break Points, SetPoints, MatchPoints, TieBreak, Winners and UFE. All data I obtained from www.tennisabstract.com
- Why the weighing? The ball's speed and bouncing height depends on the court surface. Thus it has a direct impact on the players' performances as they have different playing styles. Also a Grandslam tournament poses a much higher pressure on a top player than any other tournament. Yet, not every player can always withstand this.

## Challenges
- finding the right methos for a tennis match simulation
- setting up the database with pandas in the right form to be usable within the monte-carlo-simulation
- deciding on the statistical features
- Streamlit implementation

## Next Steps
- automate database update
- expand database to include more players
- modify simulation to also include double matches

