from scipy import signal
import numpy as np

def nbit_bin (a, n = 32):
    binary = bin(a)
    for k, bit in enumerate(binary):
        if bit == 'b':
            binary = binary[k+1:]
            break
    if(len(binary) < n):
           binary = f"{(a<0)*1}"*(n - len(binary)) + binary 
    return binary

bitwidth = 32
order = 2
fac = 2**20
fs = 48000
fc = 4800
fc_n = 2*fc/fs

sos = signal.butter(N = order, Wn = fc_n, btype = 'low', output='sos', fs = fs, analog = False)
# print(sos)

# Compute Coefficient as per Required Format and write to File(names as per required format)
for j, co in enumerate(sos):
    
    f = open(str(int(j/10)) + str(j%10)  , mode = "w")
    
    line = ""
    dline = ""
    
    for i, val in enumerate(co):

        if i == 3: # Skip the Fourth Coefficient
            continue
        
        dline = dline + str((val)) + " "
        line = line + nbit_bin(int(round((val *fac))))[2:] + " "
    
    print(dline)
    print(line)
    f.write(line)
            