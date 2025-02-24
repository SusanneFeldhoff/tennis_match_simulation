import numpy as np
import pandas as pd

# probability function

def win_prob(Player1,Player2,Surface,Tournament):

    # Surface = ["Hard", "Clay", "Grass"]
    # Tournament = ["GrandSlam", "Masters", "Others"]

# Probability calculation

    Prob_df = pd.read_csv("Data/Prob_df.csv")

    # Elo Values
    Elo1 = Prob_df.loc[Prob_df["Player_Name"]==Player1,f"Elo_{Surface}"].values[0]
    Elo2 = Prob_df.loc[Prob_df["Player_Name"]==Player2,f"Elo_{Surface}"].values[0]

    # stat features
    stat_features = [f'TBWon_{Surface}_{Tournament}', f'Break_{Surface}_{Tournament}', f'DF_{Surface}_{Tournament}',
                    f'Aces_{Surface}_{Tournament}', f'Winners_{Surface}_{Tournament}', f'UFE_{Surface}_{Tournament}',
                    f'BPConv_{Surface}_{Tournament}', f'BPSvd_{Surface}_{Tournament}', f'MPConv_{Surface}_{Tournament}',
                    f'MPSvd_{Surface}_{Tournament}']


    stat_diff = 0
    for feature in stat_features:
            stat1 = Prob_df.loc[Prob_df["Player_Name"] == Player1, feature].values[0]
            stat2 = Prob_df.loc[Prob_df["Player_Name"] == Player2, feature].values[0]
            stat_diff += (stat1 - stat2) * 100

    #weighing elo an stats
    weight_Elo = 1.0
    weight_stats = 0.5
    adjusted_Elo_diff = weight_Elo * (Elo1 - Elo2) + weight_stats * stat_diff

    win_prob = 1/ (1+10**(-adjusted_Elo_diff/400))
    return win_prob

# monte carlo simulation function


def MCS(Player1,Player2,Surface,Tournament):

    if Tournament == "GrandSlam":
        best_of = 5
        required_wins = best_of //2+1
    else:
        best_of = 3
        required_wins = best_of //2+1    
    

    prob = win_prob(Player1,Player2,Surface,Tournament)


    for i in range(1000000):
        
        Player1_wins = 0 # reset for each simluation
        Player2_wins = 0

        while (Player1_wins < required_wins) and (Player2_wins < required_wins):
            if np.random.rand() < prob:
                Player1_wins += 1
            else:
                Player2_wins += 1

        if Player1_wins > Player2_wins:
            final_winner = Player1
        else:
            final_winner = Player2
    match_result = [final_winner, (Player1_wins, Player2_wins)]
    
    return match_result

