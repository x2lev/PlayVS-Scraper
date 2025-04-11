import json
import os

FREQ_CUTOFF = .30

teams = {}
for team_name in os.listdir('team_data'):
    if team_name != 'Creek Smash Red Team.json':
        with open(f'team_data/{team_name}', 'r', encoding='UTF-8') as f:
            teams[team_name] = json.loads(f.read())

char_freq = {}
weighted_char_freq = {} 
for team_name, team in teams.items():
    for player_name, player in team.items():
        total = 0
        char_num = {}
        for char, record in player['char'].items():
            char_num.setdefault(char, 0)
            char_num[char] += record['win'] + record['loss']
            total += record['win'] + record['loss']
        for char, num in char_num.items():
            record = player['char'][char]
            if (freq := char_num[char] / total) >= FREQ_CUTOFF:
                char_freq.setdefault(char, 0)
                weighted_char_freq.setdefault(char, 0)
                char_freq[char] += freq
                weighted_char_freq[char] += freq * record['win'] / (record['win'] + record['loss'])

sorted_char_freq = sorted(char_freq.items(), key=lambda t: list(t)[1])
sorted_weighted_char_freq = sorted(weighted_char_freq.items(), key=lambda t: list(t)[1])

for (c1, f), (c2, wf) in zip(sorted_char_freq, sorted_weighted_char_freq):
    print(f'{c1:>15}: {round(f, 3)}\t{c2:>15}: {round(wf, 3)}')
