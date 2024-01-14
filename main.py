import config
from difflib import get_close_matches

Player1_Team = input("Player1 Team: ")
Player1_Rank = input("Player1 Rank: ")
Player1_Level = int(input("Player1 Level: "))

Player2_Team = input("Player2 Team: ")
Player2_Rank = input("Player2 Rank: ")
Player2_Level = int(input("Player2 Level: "))

if not Player1_Level:
    Player1_Level = 0
if not Player2_Level:
    Player2_Level = 0

def get_team_info(user_input):
    input_string = user_input.lower()
    if input_string in config.team_shorts:
        return config.teams[input_string]
    
    for key, value in config.team_shorts.items():
        input_list = [item.lower() for item in value]
        result = get_close_matches(input_string, input_list, n=1)

        if result:
            if config.teams[key]:
                return config.teams[key]
        
def get_rank(user_input, ranks):
    input_string = user_input.lower()
    ranks2 = {k.lower(): k for k, v in ranks.items()}
    if input_string in ranks2:
        return ranks2[input_string]

    input_list = [item.lower() for item in ranks.keys()]
    result = get_close_matches(input_string, input_list, n=1)
    if result:
        return ranks2[result[0]]

def get_player_info(team, rank, level):
    info = {}
    info["Points"] = 0
    info["TeamInfo"] = get_team_info(team)
    if info["TeamInfo"]:
        info["Rank"] = get_rank(rank, info["TeamInfo"]["ranks"])
        if not info["Rank"]:
            return
    else:
        return
    
    info["Points"] = info["Points"] + info["TeamInfo"]["base"]
    info["Points"] = info["Points"] + info["TeamInfo"]["ranks"][info["Rank"]]
    info["Points"] = info["Points"] + level
    return info
    



Player1 = get_player_info(Player1_Team, Player1_Rank, Player1_Level)
if not Player1:
    print("Failed to get player1 info!")
else:
    Player2 = get_player_info(Player2_Team, Player2_Rank, Player2_Level)
    if not Player2:
        print("Failed to get player2 info!")
    else:
        print(f"Player1 Team: {Player1['TeamInfo']['name']}")
        print(f"Player1 Rank: {Player1['Rank']}")
        print(f"Player1 Level: {Player1_Level}")
        print(f"Player1 Points: {Player1['Points']}")
        print("")
        print(f"Player2 Team: {Player2['TeamInfo']['name']}")
        print(f"Player2 Rank: {Player2['Rank']}")
        print(f"Player2 Level: {Player2_Level}")
        print(f"Player2 Points: {Player2['Points']}")
        print("")
        if Player1['Points'] < Player2['Points']:
            print("Player 1 is below player 2")
        elif Player1['Points'] == Player2['Points']:
            print("Player 1 is equal to player 2")
        elif Player1['Points'] > Player2['Points']:
            print("Player 1 is above to player 2")
        else:
            print("We could not automatically determine who is higher!")


input("Press Enter to exit...")