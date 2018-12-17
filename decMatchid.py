import pandas as pd
import requests as re
from tqdm import tqdm
import time


def appendDFToCSV_void(df, csvFilePath):
    import os
    if not os.path.isfile(csvFilePath):
        df.to_csv(csvFilePath, mode='a', index=False)
    else:
        df.to_csv(csvFilePath, mode='a', index=False, header=False)

start_id = 4233783794

data = pd.DataFrame()

proxy = {"http" : "88.135.15.234", "port" : "60977"}

for id in tqdm(range(start_id, (start_id - 15000), -1)):
    try:
        request = re.get("https://api.opendota.com/api/matches/" + str(id), proxies = proxy).json()
        tmp = dict()
        tmp["match_id"] = request["match_id"]
        tmp["game_mode"] = request["game_mode"]
        tmp["radiant_win"] = request["radiant_win"]
        player_index = 0
        matchdetails = request["players"]
        for player in matchdetails:
            tmp["player_" + str(player_index) + "_hero"]     = player["hero_id"]
            tmp["player_" + str(player_index) + "_gold_10m"] = player["gold_t"][10]
            #print(player["gold_t"])
            tmp["player_" + str(player_index) + "_lh_10m"]   = player["lh_t"][10]
            tmp["player_" + str(player_index) + "_dn_10m"]   = player["dn_t"][10]
            tmp["player_" + str(player_index) + "_xp_10m"]   = player["xp_t"][10]

            sumkill = 0
            for kills in player["kills_log"]:
                if int(kills["time"]) < 600:
                    sumkill += 1

            tmp["player_" + str(player_index) + "_kills_10m"] = sumkill

            count_item_buy = 0
            for items in player["purchase_log"]:
                if int(items["time"]) < 600:
                    count_item_buy += 1

            tmp["player_" + str(player_index) + "_buy_items_10m"] = count_item_buy
            player_index += 1
        # print(tmp)
        data = data.append(tmp, ignore_index=True)
        print("added")
        time.sleep(1)
    except:
        print("not added")
        time.sleep(1)


appendDFToCSV_void(data, "veryNEWDATA.csv")