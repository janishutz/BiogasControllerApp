import csv
import numpy as np
import matplotlib.pyplot as plt

n = int(input("Sensor number to be printed: "))

file = ""

def generate_plot():
    reader = csv.reader(file, delimiter=',')
    data = list(reader)
    data.sort(key=lambda imp: float(imp[2]))
    lenght = len(data)
    x = []
    y = []

    for _ in range(lenght):
        extract = data.pop(0)
        sensor = int(extract.pop(0))
        if sensor == n:
            ye = extract.pop(0)
            xe = extract.pop(0)
            y.append(float(ye))
            x.append(float(xe))

    fit = np.polyfit(x, y, 2)

    formula = f"F(U) = {round(float(fit[0]), 4)}U^2+{round(float(fit[1]), 4)}U+{round(float(fit[2]), 4)}"

    fit_fn = np.poly1d(fit)

    plt.plot(x, fit_fn(x), color="BLUE", label="T(U)")

    plt.scatter(x, y, color="MAGENTA", marker="o", label="Data")
    plt.ylabel("Temperature")
    plt.xlabel("Voltage")
    title = 'Sensor MCP9701A #{}'.format(n)
    plt.title(title)
    plt.axis((0.6, 2.0, 15.0, 70.0))
    plt.legend(loc="lower right")
    plt.annotate(formula, xy=(0.85, 60))
    plt.grid(True)
    plt.show()

    saveit = input("Do you wish to save the plot? (y/N) ").lower()

    if saveit == "y":
        plt.savefig("Sensor"+str(n)+".png")
        plt.savefig("Sensor"+str(n)+".pdf", format="pdf")
        plt.savefig("Sensor"+str(n)+".svg", format="svg")
        print("==> Images saved")
    else:
        print("==> Images discarded")

filename = input("Please enter a file path to the csv file to be plotted: ")
try:
    file = open(filename, "r")
    generate_plot()
except FileNotFoundError:
    print("Failed to open file (non-existent or corrupted?)")
