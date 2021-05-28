from os import path, system as sys
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import codecs
from re import findall
import getopt, sys as sys2
from math import tan, pi
import bilinear as BLT

from scipy.signal.signaltools import _compute_factors

# Default Design Control Parameters for - Filter and Testbench
params = {
    # Model Params
    "ftype"     : "low",
    "fs"        : 48000,
    "fc"        : 10000,
    "order"     : 4,
    "bitwidth"  : 32,
    "fac"       : 20,
    "gainl"     : 0,
    "gainm"     : 0,
    "htp"       : 10, 
    # Plot Params
    "infile"    : "out.txt",
    "color1"    : '#444444',
    "color2"    : '#4444AA',
    "color3"    : '#44AA44',
    "color4"    : '#AA6666',
    "DPI"       : 300,
    "l_loc"     : "lower left",
    "l_fancy"   : True,
    "l_box"     : (-0.02, -0.25),
    "l_alpha"   : 0,
    "transp"    : False,
    "t_box"     : (1, 0),
    "t_hor"     : "right",
    "t_ver"     : "center_baseline"
}
DEV = False
cfac = 1

with open("inp.txt", "r") as p:
    ips = p.readlines()
with open("filter_tb.v", "r") as f:
    tb_lines = f.readlines()

def norml(k):
    maxx = max(k)
    minn = min(k)
    L = [(2*(val-minn)/(maxx-minn))-1 for val in k]
    return L

def mse(A,B):
    E = [(a-b)/cfac for a,b in zip(A,B)]
    mse = 0
    for e in E:
        mse += e*e
    return E, mse*(cfac*cfac) / len(E)

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

def getargs(args):
    # Get Command Line Arguements
    try:
        opts = getopt.getopt(args, "t:o:c:s:b:f:l:m:d", ["type=", "order=", "cutoff=", "samplerate=", "bitwidth=", "fac=", "gainl=", "gainm="])
        opts = opts[0]
    except getopt.GetoptError:
        print("Incorrect Usage of Flags, Reverting to Default Parameters")

    for opt, arg in opts:
        if opt == "-d":
            global DEV
            DEV = True
        if opt in ("-t", "--type"):
            params["ftype"] = arg
        elif opt in ("-o", "--order"):
            params["order"] = int(arg)
        elif opt in ("-c", "--cutoff"):
            params["fc"] = int(arg)
        elif opt in ("-s", "--samplerate"):
            params["fs"] = int(arg)
        elif opt in ("-b", "--bitwidth"):
            params["bitwidth"] = int(arg)
        elif opt in ("-f", "--fac"):
            params["fac"] = int(arg)
        elif opt in ("-l", "--gainl"):
            params["gainl"] = int(arg)
        elif opt in ("-m", "--gainm"):
            params["gainm"] = int(arg)

def get_write_filter_coeffs(order, fs, fc, ftype, fac, bitwidth, **extra):
    """ Makes a filter depending on the inputs and 
    Writes the coefficients in the specified format 
    to coefficient files

    Args:
        order (int)         : Order of the Filter
        fs (float)          : Sampling Frequency of the input samples
        fc (float)          : Cutoff Frequency of the required Filter
        ftype (str)   : "low", "high"
        fac (int)           : Coefficient Left shift (2^fac) for the Hardware Implementation
        bitwidth (int)      : Bitwidth for the hardware Implementation
    
    Return:
        sos (tuple) : Contains the Coefficients in Second Order Sections
    """
    # fc_n = 2*fc/fs; # Normalised Frequency for Digital Filter
    # sos = list(signal.butter(N = order, Wn = fc_n, btype = ftype, output='sos', analog = False))

    # Prewarp Frequency
    warp = 2 * fs * tan(pi * fc / fs)
    sos1 = list(signal.butter(N = order, Wn = warp, btype = ftype, output='sos', analog = True))
    sos1= BLT.bilinear_sos(sos1, fs)
    
    # for s in sos: print(list(s))
    # print("\n")
    # for s in sos1: print(list(s))

    # Compute Coefficient as required from raw values 
    # and write to Files as per required format
    for j, co in enumerate(sos1):
        f = open(f"{str(int(j/10))}{str(j%10)}", mode = "w")
        line = ""
        for i, val in enumerate(co):
            if i == 3: # Skip the Fourth Coefficient Entirely
                continue
            line = line + nbit_bin(int(round(( val * (2**fac) ))), 2*bitwidth) + " "
        f.write(line)
    return sos1

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

def plot_everything(
    infile, color1, color2, color3, color4,
    DPI, sos, l_loc, l_fancy, l_box, l_alpha,
    ftype, fs, fc, order, bitwidth, fac,
    gainl, gainm, transp, t_box, t_hor,
    t_ver, **extra):

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
    # Software Ref Output Sequence
    ip = np.array(ip)
    soft_filt = signal.sosfilt(sos, ip)

    # Normalise all  in (-1, 1)
    ip = norml(ip)
    op = norml(op)
    soft_filt = norml(soft_filt)
    E, MSE = mse(op, soft_filt)

    # Get Plots
    figure, axs = plt.subplots(2,1, sharex=True, sharey=False)
    # Plot Input Sequence
    axs[0].tick_params(length = 0, label1On = False, label2On = False)
    axs[0].spines["right"].set_visible(False)
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["left"].set_visible(False)
    axs[0].spines["bottom"].set_visible(False)
    axs[0].set_title("Input")
    axs[0].plot(ip, color = color1)
    
    # Plot Filtered Output Sequence - Hardware and Software Reference
    axs[1].tick_params(length = 0, label1On = False, label2On = False)
    axs[1].spines["right"].set_visible(False)
    axs[1].spines["top"].set_visible(False)
    axs[1].spines["left"].set_visible(False)
    axs[1].spines["bottom"].set_visible(False)
    axs[1].set_title("Output")
    axs[1].plot([(m-r)/cfac for m,r in zip(op,soft_filt)], 
                color = color4, label = "Err", alpha = 0.1)
    axs[1].plot(soft_filt, color = color2, label = "Ref")
    axs[1].plot(op, color = color3, label = "Model")
    axs[1].set_ylim(top = 1.2, bottom = -1.2)
    axs[1].legend(loc = l_loc, fancybox = l_fancy, 
                bbox_to_anchor = l_box, framealpha = l_alpha)
    
    # Construct Plot Text
    ptxt = f"Order {order}\n{ftype.capitalize()}pass\n{fc/1000}/{fs/1000} kHz\nMSE = {MSE:e}"
    
    axs[1].text(*t_box, ptxt, ha = t_hor, va = t_ver, 
                transform=axs[1].transAxes, bbox = dict(facecolor = '#FFFFFF', alpha = l_alpha))
    
    figure.subplots_adjust(bottom = 0.15, left = 0.08)
    savefile = path.join("results",
        f"_{ftype}_{order}_({fc}_{fs})_{bitwidth}_{fac}_{gainl}_{gainm}.png")
    plt.savefig(savefile, transparent = transp, dpi = DPI)
    plt.close()

def run():
    sos = get_write_filter_coeffs(**params)
    write_testbench(**params)
    sys("iverilog -o ivop filter_tb.v iir_N.v iir_2.v")
    sys("vvp ivop > out.txt")
    plot_everything(sos = sos, **params)

# Run Everything
if __name__ == "__main__":
    getargs(sys2.argv[1:])
    sys("cls")
    if not DEV: run()
    else:
        for fc in range(8, 11):
            params["fc"] = fc*1000
            for order in range(1,6):
                params["order"] = order
                try: 
                    run()
                except:
                    continue
    sys("cls")