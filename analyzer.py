import json

with open('data.json', 'r', encoding='UTF-8') as f:
    data = json.loads(f.read())

print(data.pop(0))
players = {}
for match in data:
    for pos, series in enumerate(match):
        name = series['name']
        if name not in players:
            players[name] = {'pos': [0, 0, 0, 0, 0], 'stage': {}, 'char': {}, 'opp': {}}
        if pos not in players[name]['pos']:
            players[name]['pos'][pos] = 0
        players[name]['pos'][pos] += 1
        for game in series['games']:
            stage = game['stage']
            char = game['char']
            opp = game['opp']
            result = game['result']
            if stage not in players[name]['stage']:
                players[name]['stage'][stage] = {'win': 0, 'loss': 0}
            if char not in players[name]['char']:
                players[name]['char'][char] = {'win': 0, 'loss': 0}
            if opp not in players[name]['opp']:
                players[name]['opp'][opp] = {'win': 0, 'loss': 0}

            players[name]['stage'][stage][result] += 1
            players[name]['char'][char][result] += 1
            players[name]['opp'][opp][result] += 1

lines = []
for name, player in players.items():
    lines.append(f'\n{name}')
    lines.append('  Position')
    for i in range(5):
        lines.append(f'    {i+1}: {player['pos'][i]} series')
    lines.append('  Stages')
    for stage, results in player['stage'].items():
        w = results['win']
        t = results['win'] + results['loss']
        lines.append(f'    {stage}: {t} game(s), {round(w/t, 4)*100}% win rate')
    lines.append('  Characters')
    for char, results in player['char'].items():
        w = results['win']
        t = results['win'] + results['loss']
        lines.append(f'    {char}: {t} game(s), {round(w/t, 4)*100}% win rate')
    lines.append('  Opponents')
    for opp, results in player['opp'].items():
        w = results['win']
        t = results['win'] + results['loss']
        lines.append(f'    {opp}: {t} game(s), {round(w/t, 4)*100}% win rate')

print('\n'.join(lines))

with open('output', 'w', encoding='UTF-8') as f:
    f.write('\n'.join(lines))
