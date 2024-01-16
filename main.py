import config
import requests
from difflib import get_close_matches
from termcolor import colored
import colorama

colorama.init()

def get_latest_release():
   url = f"https://api.github.com/repos/{config.username}/{config.repo}/releases/latest"
   response = requests.get(url)
   return response.json()["tag_name"]

latest_release = get_latest_release()
if config.current_version < latest_release:
   print(colored(f"Your currently using an outdated version. Please update as soon as possible!\nCurrent version: {config.current_version}\nLatest version: {latest_release}\nUpdate link: https://github.com/{config.username}/{config.repo}/releases/tag/{latest_release}", "red"))

def get_team_info(user_input):
    input_string = user_input.lower()
    if input_string in config.team_shorts:
        return config.teams[input_string]
    
    for key, value in config.team_shorts.items():
        input_list = [item.lower() for item in value]
        result = get_close_matches(input_string, input_list, n=1, cutoff=0.5)

        if result:
            if config.teams[key]:
                return config.teams[key]
        
def get_rank(user_input, ranks):
    input_string = user_input.lower()
    ranks2 = {k.lower(): k for k, v in ranks.items()}
    if input_string in ranks2:
        return ranks2[input_string]

    input_list = [item.lower() for item in ranks.keys()]
    result = get_close_matches(input_string, input_list, n=1, cutoff=0.5)
    if result:
        return ranks2[result[0]]

def get_player_info(player):
    info = {}
    info["TeamInfo"] = get_team_info(input(f"Player{player} Team: "))
    if not info["TeamInfo"]:
        print(colored(f"Team not found, please provide more information about the team or simply a shortcut (rrt, sid, md, etc.)", "red"))
        return
    info["Rank"] = get_rank(input(f"Player{player} Rank: "), info["TeamInfo"]["ranks"])
    if not info["Rank"]:
        print(colored(f"Rank not found, please provide more information about the rank and make sure its not CI or CD", "red"))
        return
    info["Level"] = int(input(f"Player{player} Level (0-5): "))
    if not info["Level"] or (info["Level"] < 0 or info["Level"] > 5):
        print(colored(f"Level must be a number ranging from 0 to 5", "red"))
        return
    print("")
    #info["Points"] = info["Points"] + info["TeamInfo"]["base"]
    #info["Points"] = info["Points"] + info["TeamInfo"]["ranks"][info["Rank"]]
    #info["Points"] = info["Points"] + level

    #Formula used: (card level * 2) + (department rank * team multiplier)
    info["Points"] = (info["Level"] * 2) + (info["TeamInfo"]["ranks"][info["Rank"]] * info["TeamInfo"]["base"]) 
    
    return info
    
def start():
    Player1 = get_player_info(1)
    if not Player1:
        return
    Player2 = get_player_info(2)
    if not Player2:
        return
    
    print("")

    print(f"Player1 Team: {Player1['TeamInfo']['name']}")
    print(f"Player1 Rank: {Player1['Rank']}")
    print(f"Player1 Level: {Player1['Level']}")
    print(f"Player1 Points: {Player1['Points']}")
    print("")
    print(f"Player2 Team: {Player2['TeamInfo']['name']}")
    print(f"Player2 Rank: {Player2['Rank']}")
    print(f"Player2 Level: {Player2['Level']}")
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
    print("")

while True:
    start()