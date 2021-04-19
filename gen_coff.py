from scipy import signal
import matplotlib.pyplot as plt
# scipy.signal.butter(N, Wn, btype='low', analog=False, output='ba', fs=None)

order = 4
sos = signal.butter(order, 100 , 'low', analog=True, output='sos')
print(sos[1])
# for i in sos[1]
