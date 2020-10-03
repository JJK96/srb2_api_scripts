import requests

api_url = 'https://srb2circuit.eu/highscores/api/'

num_plays = requests.get(api_url + 'num_plays', verify=False).json()

maps = requests.get(api_url + 'maps?in_rotation', verify=False).json()
maps = sorted(maps, key=lambda map:int(map['votes']), reverse=True)

map_dict = {}
for i, m in enumerate(maps):
    map_dict[int(m['id'])] = {
        "position": i,
        "map": m
    }

table = []
position = 0
for i, j in zip(maps, num_plays):
    voted_pos = map_dict[int(j['id'])]['position']
    difference = voted_pos  - position
    table.append({
        "name": j['name'],
        "voted_pos": voted_pos,
        "position": position,
        "difference": difference
    })
    position += 1

headers = ["Map", "Voted position", "Played position", "Difference"]
print(f"{headers[0]:20} | {headers[1]:20} | {headers[2]:20} | {headers[3]:20}")
for r in sorted(table, key=lambda r:r['difference'], reverse=True):
    print(f"{r['name']:20} | {r['voted_pos']:20} | {r['position']:20} | {r['difference']:20}")

def printList():
    position = 0
    for i, j in zip(maps, num_plays):
        voted = "{} ({})".format(i['name'], i['votes'])
        played = "{} ({})".format(j['name'], j['num_plays'])
        difference =  map_dict[j['id']]['position'] - position
        print(f"{voted:30} | {played:30} | {difference}")
        position += 1
