import csv
import numpy as np
import matplotlib.pyplot as plt

n = int(input("Sensor number to be printed: "))

file = ""


def generate_plot():
    # Read data using the CSV library
    reader = csv.reader(file, delimiter=",")

    # Create a list from the data
    data = list(reader)

    # Sort the list using a lambda sort descriptor
    # A lambda function is an anonymous function (= an unnamed function),
    # which makes it convenient. A sort descriptor is a function that
    # (usually, but not here) returns a value indicating which of two values
    # come before or after in the ordering.
    # Here, instead we simply return a floating point value for each data point
    data.sort(key=lambda data_point: float(data_point[2]))

    # Store the x and y coordinates in two arrays
    x = []
    y = []

    for _ in range(len(data)):
        # Extract the data point
        data_point = data.pop(0)
        sensor = int(data_point.pop(0))
        if sensor == n:
            y.append(float(data_point.pop(0)))
            x.append(float(data_point.pop(0)))

    # Use Numpy's polyfit function to fit a 2nd degree polynomial to the points using quadratic regression
    # This function returns an array with the coefficients
    fit = np.polyfit(x, y, 2)

    # The formula to output to the plot
    formula = f"F(U) = {round(float(fit[0]), 4)}U^2+{round(float(fit[1]), 4)}U+{round(float(fit[2]), 4)}"

    # Create a fit function from the previously determined coefficients
    fit_fn = np.poly1d(fit) # Returns a function that takes a list of x-coordinate as argument

    # Plot the line on the graph
    plt.plot(x, fit_fn(x), color="BLUE", label="T(U)")

    # Scatter Plot the data points that we have
    plt.scatter(x, y, color="MAGENTA", marker="o", label="Data")

    # Label the graph
    plt.ylabel("Temperature")
    plt.xlabel("Voltage")
    plt.title("Sensor MCP9701A #{}".format(n))

    # Scale the axis appropriately
    plt.axis((0.6, 2.0, 15.0, 70.0))

    # Print a legend and set the graph to be annotated
    plt.legend(loc="lower right")
    plt.annotate(formula, xy=(0.85, 60))

    # Enable the background grid
    plt.grid(True)

    # Finally, show the graph
    plt.show()

    # Get user input whether to save the plot or not
    saveit = input("Do you wish to save the plot? (y/N) ").lower()

    if saveit == "y":
        # Save the plot as Sensor[Number] (e.g. Sensor9) as png, pdf and svg
        plt.savefig("Sensor" + str(n) + ".png")
        plt.savefig("Sensor" + str(n) + ".pdf", format="pdf")
        plt.savefig("Sensor" + str(n) + ".svg", format="svg")
        print("==> Images saved")
    else:
        print("==> Images discarded")


# Since we have defined a function above as a function, this here is executed first
filename = input("Please enter a file path to the csv file to be plotted: ")

# Try to open the file
try:
    file = open(filename, "r")
    generate_plot()
except FileNotFoundError:
    print("Failed to open file (non-existent or corrupted?)")
