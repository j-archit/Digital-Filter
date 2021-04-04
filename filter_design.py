from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

sos = signal.butter(4, 0.5, 'low', output='sos')