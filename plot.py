import codecs
import matplotlib.pyplot as plt
from re import findall

opcolor = '#000000'
opcolor2 = '#000000'
DPI = 300

ip = []
op = []

with codecs.open("out.txt", "r", "utf-8") as f:
    lines = f.readlines()
    for row in lines:
        data = findall("[-]*[0-9]+", row)
        if len(data) == 3:
            continue
        ip.append(int(data[0]))
        op.append(int(data[1]))
        
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

plt.plot(ip, color = opcolor)
plt.ylabel("Input")
plt.xlabel("Samples")
plt.savefig("ip.png", transparent = True, dpi = DPI)


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

plt.plot(op, color = opcolor)
plt.ylabel("Filtered Output")
plt.xlabel("Samples")
plt.savefig("op.png", transparent = True, dpi = DPI)