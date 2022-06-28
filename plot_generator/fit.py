import csv
import numpy as np
import matplotlib.pyplot as plt
n = int(input("Aktuelle Sondennummer: "))

imp = open("Sonden2021.csv", "r")
reader = csv.reader(imp, delimiter=',')
rohdaten = list(reader)
rohdaten.sort(key=lambda imp: float(imp[2]))
lenght = len(rohdaten)
x = []
y = []
for i in range(lenght):
    extract = rohdaten.pop(0)
    sondennummer = int(extract.pop(0))
    if sondennummer == n:
        xe = extract.pop(0)
        ye = extract.pop(0)
        y.append(float(xe))
        x.append(float(ye))

fit = np.polyfit(x,y,2)
print(fit)

formula = "F(U) = %sU^2+%sU+%s"%(str(round(float(fit[0]),4)),str(round(float(fit[1]),4)),str(round(float(fit[2]),4)))

fit_fn = np.poly1d(fit)


plt.plot(x, fit_fn(x), color="BLUE", label="T(U)")
        
plt.scatter(x, y, color="MAGENTA", marker="o", label="Messsdaten")
plt.ylabel("Temperatur")
plt.xlabel("Spannung")
titel = 'Temperatursonde MCP9701A Nummer: {}'.format(n)
plt.title(titel)
plt.axis([0.6, 2, 15, 70])
plt.legend(loc="lower right")
plt.annotate(formula, xy=(0.85,60))
plt.grid(True)
plt.show()

saveit = input("Sollen der Graph gespeichert werden? (y/n) ").lower()
if saveit == "y":
    plt.savefig("Sonde"+str(n)+".png")
    plt.savefig("Sonde"+str(n)+".pdf", format="pdf")
    plt.savefig("Sonde"+str(n)+".svg", format="svg")
    print("saved images")
else:
    print("discarded images")
        
