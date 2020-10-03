import requests
import matplotlib.pyplot as plt
import numpy as np

endpoint = "https://srb2circuit.eu/highscores/api/time_stats"

weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

def plot_day():
    data = requests.get(endpoint, verify=False)
    data = data.json()
    y = []
    for day in weekdays:
        y.append(data[day])

    plt.bar(weekdays, y)
    plt.xlabel("Day of the week")
    plt.ylabel("Number of records")
    plt.show()

def plot_day_hour():
    data = requests.get(endpoint + "?day&hour", verify=False)
    data = data.json()
    avg = np.zeros(24)
    for day in weekdays:
        x, y = zip(*data[day].items())
        avg += y
        plt.plot(x,y, label=day)
        plt.xlabel("Hour of the day")
        plt.ylabel("Number of records")
    avg /= 7
    plt.plot(avg, label="Average", linewidth=4)
    plt.legend()
    plt.show()

def plot_hour():
    data = requests.get(endpoint + "?hour", verify=False)
    data = data.json()
    x, y = zip(*data.items())
    plt.plot(x,y)
    plt.xlabel("Hour of the day")
    plt.ylabel("Number of records")
    plt.show()
