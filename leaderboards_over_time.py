import requests
import calendar
import pickle
from datetime import date
from matplotlib import pyplot as plt
from collections import defaultdict

start_month = (2020, 5)
now = date.today()
end_month = (now.year, now.month)
api_url = "https://srb2circuit.eu/highscores/api/leaderboard"

def get_month_start_end(month):
    last_day = calendar.monthrange(*month)[1]
    return "{}-{:02}-{:02}".format(*month, 1), "{}-{:02}-{:02}".format(*month, last_day)

def get_leaderboard(month):
    start, end = get_month_start_end(month)
    r = requests.get(f"{api_url}?end_date={end}", verify=False)
    return r.json()

def months(start_month, end_month):
    month = start_month
    while month <= end_month:
        yield month
        if month[1] < 12:
            month = (month[0], month[1]+1)
        else:
            month = (month[0]+1, 1)

def get_leaderboards(start_month, end_month, max_users=10):
    points = defaultdict(dict)
    positions = defaultdict(dict)
    for month in months(start_month, end_month):
        leaderboard = get_leaderboard(month)
        for i, v in enumerate(leaderboard):
            if i >= max_users:
                break
            username = v['username']
            positions[username][month] = i+1
            points[username][month] = v['total']
    return points, positions

def save_pickle(points, positions):
    with open('points', 'wb') as f:
        pickle.dump(points, f)
    with open('positions', 'wb') as f:
        pickle.dump(positions, f)

def load_pickle():
    with open('points', 'rb') as f:
        points = pickle.load(f)
    with open('positions', 'rb') as f:
        positions = pickle.load(f)
    return points, positions

def prune(d, min_entries=5):
    pruned = {}
    for username, entries in d.items():
        if len(entries) >= min_entries:
            pruned[username] = entries
    return pruned

def display_month(month):
    return "{}-{:02}".format(*month)

points, positions = get_leaderboards(start_month, end_month)
#save_pickle(points, positions)
#points, positions = load_pickle()

def plot(d, title, start_month, end_month, axis_reversed=True):
    x = []
    ys = defaultdict(list)
    for month in months(start_month, end_month):
        x.append(display_month(month))
        for username, entries in d.items():
            ys[username].append(entries.get(month, None))
    plt.figure()
    plt.title(title)
    if axis_reversed:
        plt.gca().invert_yaxis()
    for username, y in ys.items():
        plt.plot(x, y, label=username)
    plt.legend()
    plt.show()

plot(prune(positions, 4), "Positions", start_month, end_month, True)
plot(prune(points, 4), "Points", start_month, end_month, False)
