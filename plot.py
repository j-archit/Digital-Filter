import codecs
import matplotlib.pyplot as plt

opcolor = '#000000'
opcolor2 = '#000000'
aspin = 0.3
aspout = 0.1
DPI = 300

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
ax.tick_params(length = 0, label1On = False, label2On = False)
#ax.set_aspect(aspin)

plt.plot(unfil, color = opcolor)
plt.ylabel("Input")
plt.xlabel("Samples")
plt.savefig("unf.png", transparent = True, dpi = DPI)


# Filtered Output Sequence
plt.figure()
ax1 = plt.axes()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_color(opcolor2)
ax1.spines['left'].set_color(opcolor2)
ax1.yaxis.label.set_color(opcolor2)
ax1.xaxis.label.set_color(opcolor2)
ax1.tick_params(length = 0, label1On = False, label2On = False)
#ax1.set_aspect(aspout)

plt.plot(fil, color = opcolor)
plt.ylabel("Filtered Output")
plt.xlabel("Samples")
plt.savefig("fil.png", transparent = True, dpi = DPI)