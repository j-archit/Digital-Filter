from os import system as sys
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import codecs
from re import findall


# Design Control Parameters for - Filter and Testbench
params = {
    "filter_type"   : "low",
    "fs"            : 48000,
    "fc"            : 5000,
    "order"         : 2,
    "bitwidth"      : 32,
    "fac"           : 24,
    "gainl"         : 0,
    "gainm"         : 0,
    "htp"           : 10 
}
plot_params = {
    "infile"   : "out.txt",
    "color1"    : '#000000',
    "color2"    : '#000000',
    "DPI"       : 300
}

with open("inp.txt", "r") as p:
    ips = p.readlines()
with open("filter_tb.v", "r") as f:
    tb_lines = f.readlines()

def nbit_bin (a, n = 2*params["bitwidth"]):
    """Generate a n-bit binary representation of the input a

    Args:
        a (int): input integer
        n (int, optional): number of bits in representation. Defaults to 2*params["bitwidth"].

    Returns:
        str: n bit binary representation of the number a
    """
    binary = bin(a)
    for k, bit in enumerate(binary):
        if bit == 'b':
            binary = binary[k+1:]
            break
    if(len(binary) < n):
           binary = f"{(a<0)*1}"*(n - len(binary)) + binary 
    return binary

def get_write_filter_coeffs(order, fs, fc, filter_type, fac, bitwidth, **extra):
    """ Makes a filter depending on the inputs and 
    Writes the coefficients in the specified format 
    to coefficient files

    Args:
        order (int)         : Order of the Filter
        fs (float)          : Sampling Frequency of the input samples
        fc (float)          : Cutoff Frequency of the required Filter
        filter_type (str)   : "low", "high"
        fac (int)           : Coefficient Left shift (2^fac) for the Hardware Implementation
        bitwidth (int)      : Bitwidth for the hardware Implementation
    
    Return:
        k (float)   : Filter Gain
        sos (tuple) : Contains the Coefficients in Second Order Sections
    """
    
    fc_n = 2*fc/fs; # Normalised Frequency for Digital Filter
    
    # This is necessary because the SciPy Library is doing some stupid stuff.
    k = signal.butter(N = order, Wn = fc_n, btype = filter_type, output='zpk', analog = False)[2]
    # print(f"Gain Factor: {k}")
 
    sos = signal.butter(N = order, Wn = fc_n, btype = filter_type, output='sos', analog = False)
    # Compute Coefficient as required from raw values 
    # and write to Files as per required format
    for j, co in enumerate(sos):
        f = open(f"{str(int(j/10))}{str(j%10)}", mode = "w")
        line = ""
        dline = ""
        for i, val in enumerate(co):
            if i < 3:
                if j == 0 :
                    val =  val / k # Because the first section was doing weird things
            if i == 3: # Skip the Fourth Coefficient Entirely
                continue
            dline = dline + str((val)) + " "
            line = line + nbit_bin(int(round(( val * (2**fac) ))), 2*bitwidth) + " "
        f.write(line)
    
    return k, sos

def write_testbench(order, fac, bitwidth, gainl, gainm, htp, **extra):
    vparams = {
        "order": order,
        "fac": fac,
        "bitwidth": bitwidth,
        "gainl": gainl,
        "gainm": gainm,
        "htp": htp
    }

    # Build Stimulus Block of Lines
    stim = [f"\t\t#(2*HTP); x = {int(s)};\n" for s in ips]
    # Build Param Block of Lines
    params = [f"  localparam {key.upper()} = {value};\n" for key, value in vparams.items()]
    # Build final lines list
    new = []
    flag = 0
    for line in tb_lines:
        if not flag:
            new.append(line)
        l = line.strip().lower()
        if l == "// params":
            new = [*new, *params]
            flag = 1
        if l == "// stimuli":
            new = [*new, *stim]
            flag = 1
        # Reset Flag to resume copying        
        if l == "// stimuli end" or l == "// params end":
            new.append(line)
            flag = 0

    with open("filter_tb.v", "w") as f:
        f.writelines(new)

def plot_everything(infile, color1, color2, DPI, sos, **extra):
    ip = []
    op = []

    with codecs.open(infile, "r", "utf-8") as f:
        inf = f.readlines()
        for row in inf:
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
    ax.spines['bottom'].set_color(color2)
    ax.spines['left'].set_color(color2)
    ax.yaxis.label.set_color(color2)
    ax.xaxis.label.set_color(color2)
    ax.tick_params(length = 0, label1On = False, label2On = False)

    plt.plot(ip, color = color1)
    plt.ylabel("Input")
    plt.xlabel("Samples")
    plt.savefig("input.png", transparent = True, dpi = DPI)

    # Hardware Filtered Output Sequence
    plt.figure()
    ax1 = plt.axes()
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_color(color2)
    ax1.spines['left'].set_color(color2)
    ax1.yaxis.label.set_color(color2)
    ax1.xaxis.label.set_color(color2)
    ax1.tick_params(length = 0, label1On = False, label2On = False)

    plt.plot(op, color = color1)
    plt.ylabel("Filtered Output")
    plt.xlabel("Samples")
    plt.savefig("output.png", transparent = True, dpi = DPI)

    # Software Ref Output Sequence
    ip = np.array(ip)
    filtered = signal.sosfilt(sos, ip)
    plt.figure()
    ax = plt.axes()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(color2)
    ax.spines['left'].set_color(color2)
    ax.yaxis.label.set_color(color2)
    ax.xaxis.label.set_color(color2)
    ax.tick_params(length = 0, label1On = False, label2On = False)

    plt.plot(filtered, color = color2)
    plt.ylabel("Reference Output")
    plt.xlabel("Samples")
    plt.savefig("output_ref.png", transparent = True, dpi = DPI)

# Run Everything
if __name__ == "__main__":
    k, sos = get_write_filter_coeffs(**params)
    write_testbench(**params)
    sys(r".\run.bat")
    plot_everything(sos = sos, **plot_params)
    sys("cls")