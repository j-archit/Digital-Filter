from scipy import signal

# Control Parameters
filter_type = "low"
fs = 48000
fc = 5000    
fc_n = 2*fc/fs
vparams = {
    "bitwidth": 32,
    "order": 4,
    "fac": 20,
    "gainl": 0,
    "gainm": 0,
    "htp": 10 }

def nbit_bin (a, n = 2*vparams["bitwidth"]):
    binary = bin(a)
    for k, bit in enumerate(binary):
        if bit == 'b':
            binary = binary[k+1:]
            break
    if(len(binary) < n):
           binary = f"{(a<0)*1}"*(n - len(binary)) + binary 
    return binary

def get_write_filter_coeffs():
    # This is necessary because the SciPy Library was doing some stupid stuff.
    k = signal.butter(N = vparams["order"], Wn = fc_n, btype = filter_type, output='zpk', analog = False)[2]
    # print(f"Gain Factor: {k}")
    
    # Get Coefficients 
    sos = signal.butter(N = vparams["order"], Wn = fc_n, btype = filter_type, output='sos', analog = False)

    # Compute Coefficient as per Required Format and write to File(names as per required format)
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
            line = line + nbit_bin(int(round(( val * (2**vparams["fac"]) ))), 2*vparams["bitwidth"]) + " "
        f.write(line)

def write_testbench():
    # Write changes to tesbench - inp.txt and vparams
    new = []
    with open("filter_tb.v", "r") as f:
        lines = f.readlines()

        # Build Stimulus Block of Lines
        stim = []
        with open("inp.txt", "r") as ipf:
            ips = ipf.readlines()
            stim = [f"\t\t#(2*HTP); x = {int(s)};\n" for s in ips]
        # Build Param Block of Lines
        params = [f"  localparam {key.upper()} = {value};\n" for key, value in vparams.items()]

        # Build final lines list
        flag = 0
        for line in lines:
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

get_write_filter_coeffs()
write_testbench()