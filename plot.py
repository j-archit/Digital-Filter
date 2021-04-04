import csv
import codecs
import matplotlib.pyplot as plt

unfil = []
fil = []

with codecs.open("output.txt", "r", "utf-16") as f:
    data = csv.reader(f, delimiter = ",")

    for row in data:
        try:
            a, b = row
            unfil.append(int(a))
            fil.append(int(b))
        except:
            continue

plt.figure()
plt.subplot(211)
plt.plot(unfil)
plt.ylabel("unfiltered")

plt.subplot(212)
plt.plot(fil)
plt.ylabel("filtered")

plt.savefig("plot.png")