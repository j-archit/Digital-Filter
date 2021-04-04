import csv
import codecs
import matplotlib.pyplot as plt

opcolor = '#ffffff'
opcolor2 = '#44c4d4'

unfil = []
fil = []

with codecs.open("output.txt", "r", "utf-8") as f:
    data = csv.reader(f, delimiter = ",")

    for row in data:
        try:
            a, b = row
            unfil.append(int(a))
            fil.append(int(b))
        except:
            continue

# Unfiltered Input Sequence
plt.figure()
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color(opcolor2)
ax.spines['left'].set_color(opcolor2)
ax.yaxis.label.set_color(opcolor2)
ax.xaxis.label.set_color(opcolor2)
ax.tick_params(length = 0, labelcolor = opcolor2, labelrotation = 45, label1On = False, label2On = False)
ax.set_aspect(0.05)

plt.plot(unfil, color = opcolor)
plt.ylabel("Input")
plt.xlabel("Samples")
plt.savefig("unf.png", transparent = True, dpi = 1200)


# Filtered Output Sequence
plt.figure()
ax1 = plt.axes()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_color(opcolor2)
ax1.spines['left'].set_color(opcolor2)
ax1.yaxis.label.set_color(opcolor2)
ax1.xaxis.label.set_color(opcolor2)
ax1.tick_params(length = 0, labelcolor = opcolor2, labelrotation = 45, label1On = False, label2On = False)
ax1.set_aspect(0.1)

plt.plot(fil, color = opcolor)
plt.ylabel("Filtered Output")
plt.xlabel("Samples")
plt.savefig("fil.png", transparent = True, dpi = 1200)
