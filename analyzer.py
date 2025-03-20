import json
import pandas as pd

TEAM_1 = 'Creek Smash Red Team'
TEAM_2 = 'ACHS Varsity'

with open(f'match_data/{TEAM_1}.json', 'r', encoding='UTF-8') as f:
    team_1 = json.loads(f.read())

with open(f'match_data/{TEAM_2}.json', 'r', encoding='UTF-8') as f:
    team_2 = json.loads(f.read())

mu_chart = pd.DataFrame(index=team_1.keys(), columns=team_2.keys())
mu_chart.fillna(0)

def total(item):
    _, record = item
    return record['win'] + record['loss']

for player_1 in team_1:
    for player_2 in team_2:
        for stage in player_1['stage']:
            record_1 = player_1['stage'][stage]
            record_2 = player_2['stage'][stage]
