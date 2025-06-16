"""This Program is CLI only!"""

import matplotlib.pyplot as plt
import csv
import os

# Get user input for various data
path = input("Path to csv-file to be plotted: ")
print("For the below, it is recommended to enter data in this format: yyyy-mm-dd-hh-mm")
date = input("Date & time at which the measurement was taken (approx.): ")
group = input("Group-name: ")
saveit = input("Should the graph be saved? (y/n) ").lower()

imp = open(path, "r")
reader = csv.reader(imp, delimiter=",")
data = list(reader)
x = []
y = []
for i in range(len(data)):
    # Extract the data
    extract = data.pop(0)
    x.append(float(extract.pop(0)))
    y.append(float(extract.pop(0)))

# Set up plot
plt.plot(x, y, color="MAGENTA")
plt.xlabel("Time")
plt.ylabel("Voltage")

plt.title(f"GC - Biogasanlage {date}")
plt.grid(True)

# Check if user wants to save the image
if saveit == "n":
    print("didn't save images")
else:
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
    plt.savefig(f"{save_path}/GC-{date}-{group}.png")

    print(f"Saved images to {save_path}")
plt.show()
