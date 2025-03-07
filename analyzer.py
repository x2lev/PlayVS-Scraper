import json

TEAM_NAME = 'Creek Smash Red Team'

with open(f'{TEAM_NAME}.json', 'r', encoding='UTF-8') as f:
    data = json.loads(f.read())

lines = []
lines.append(data.pop(0))
players = {}
for match in data:
    for pos, series in enumerate(match):
        name = series['name']
        if name not in players:
            players[name] = {'season': [], 'pos': [0, 0, 0, 0, 0], 'stage': {}, 'char': {}, 'opp': {}}
        if pos not in players[name]['pos']:
            players[name]['pos'][pos] = 0
        players[name]['pos'][pos] += 1
        for game in series['games']:
            season = game['season']
            stage = game['stage']
            char = game['char']
            opp = game['opp']
            result = game['result']
            if season not in players[name]['season']:
                players[name]['season'].append(season)
            if stage not in players[name]['stage']:
                players[name]['stage'][stage] = {'win': 0, 'loss': 0}
            if char not in players[name]['char']:
                players[name]['char'][char] = {'win': 0, 'loss': 0}
            if opp not in players[name]['opp']:
                players[name]['opp'][opp] = {'win': 0, 'loss': 0}

            players[name]['stage'][stage][result] += 1
            players[name]['char'][char][result] += 1
            players[name]['opp'][opp][result] += 1

for name, player in sorted(players.items(), key=lambda t: list(t)[0]):
    print(player['season'])
    if any(s in ['Spring 2025', 'Fall 2024'] for s in player['season']) or name == 'Anpetu Chrisjohn':
        lines.append(f'\n{name}')
        lines.append(f'  Played in {', '.join(player['season'])}')
        lines.append('  Position')
        for i in range(5):
            lines.append(f'    {i+1}: {player['pos'][i]} series')
        lines.append('  Stages')
        for stage, results in sorted(player['stage'].items(), key=lambda t: list(t)[1]['win'] + list(t)[1]['loss'], reverse=True):
            w = results['win']
            t = results['win'] + results['loss']
            lines.append(f'    {stage}: {t} game(s), {round(w/t*100, 2)}% win rate')
        lines.append('  Characters')
        for char, results in sorted(player['char'].items(), key=lambda t: list(t)[1]['win'] + list(t)[1]['loss'], reverse=True):
            w = results['win']
            t = results['win'] + results['loss']
            lines.append(f'    {char}: {t} game(s), {round(w/t*100, 2)}% win rate')
        lines.append('  Opponents')
        for opp, results in sorted(player['opp'].items(), key=lambda t: list(t)[1]['win'] + list(t)[1]['loss'], reverse=True):
            w = results['win']
            t = results['win'] + results['loss']
            lines.append(f'    {opp}: {t} game(s), {round(w/t*100, 2)}% win rate')

print('\n'.join(lines))

with open(f'formatted_data/{TEAM_NAME}', 'w', encoding='UTF-8') as f:
    f.write('\n'.join(lines))
