import requests
import matplotlib.pyplot as plt
import pprint

pp = pprint.PrettyPrinter()

top_players = requests.get('https://srb2circuit.eu/highscores/api/leaderboard', verify=False)
top_players = list(top_players.json().keys())

maps = requests.get('https://srb2circuit.eu/highscores/api/maps', verify=False)
maps = maps.json()
maps = [m['name'] for m in maps]

def plot_score(mapname):
    print(mapname)
    resp = requests.get(f'https://srb2circuit.eu/highscores/api/search?mapname={mapname}', verify=False)
    data = resp.json()

    scores = [d for d in data if d['time'] < 10*60*30 and d['skin'] == 'sonic'][::-1]
    times = [d['time']/30 for d in scores]
    print("Samples: " + str(len(times)))

    plt.plot(times)
    plt.xlabel('runs')
    plt.ylabel('time (s)')
    plt.title(mapname)
    plt.show()
    return scores

for m in maps:
    plot_score(m)
# plot_score('frozen night')
