"""This Program is CLI only!"""

import matplotlib.pyplot as plt
import csv
import os

path = input("Path to csv-file to be plotted: ")
date = input("Date & time at which the measurement was taken (approx.): ")
group = input("Group-name: ")
saveit = input("Should the graph be saved? (y/n) ").lower()

imp = open(path, "r")
reader = csv.reader(imp, delimiter=',')
rohdaten = list(reader)
lenght = len(rohdaten)
x = []
y = []
for i in range(lenght):
    extract = rohdaten.pop(0)
    x.append(float(extract.pop(0)))
    y.append(float(extract.pop(0)))

plt.plot(x, y, color="MAGENTA")
plt.xlabel("Time")
plt.ylabel("Voltage")
title = f"GC - Biogasanlage {date}"
plt.title(title)
plt.grid(True)
if saveit == "y":
    pos = 0
    for letter in path[::-1]:
        if letter == "/":
            break
        else:
            pos += 1
    pos_c = len(path) - pos
    ppath = path[:pos_c]
    save_path = f"{ppath}graphs/"
    try:
        os.mkdir(save_path)
    except FileExistsError:
        pass
    plt.savefig(save_path)
    os.rename(f"{save_path}/.png", f"{save_path}/GC-{date}-{group}.png")
    print(f"saved images to {save_path}")
else:
    print("didn't save images")
plt.show()


