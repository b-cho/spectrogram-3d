import numpy as np
import matplotlib.pyplot as plt

def sine_hz(fs, duration, f):
    # fs: sample rate (Hz, int)
    # duration: duration of sine wave (sec, float)
    # f: frequency of sine wave (Hz, float)
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    return samples

def dft(x, N=None, rl=True):
    if(not N):
        N = len(x)

    X = []
    for k in range(int(N/2)): # Accounting for the Nyquist frequency and DFT folding
        X.append(np.sum([x[n] * np.exp((1j * -2 * np.pi * k * n) / N) for n in range(N)]))
    if(rl):
        X = np.abs(X)
    return X

def stft(x, nfft, sample_rate, overlap=None):
    STFT = []
    if(overlap == None):
        overlap = int(nfft/2)

    for n in range(0, len(x), nfft):
        x_trim = x[max(0, n-overlap):max(0, n-overlap)+nfft] # Use a rectangular window
        dft_x = dft(x_trim)
        STFT.append(dft_x)
    
    return np.swapaxes(np.array(STFT), 0, 1), len(x) # The array is vertical, not horizontal.

def show_spectrogram(S, sample_rate=None, n_samples=None):
    fig = plt.figure(figsize=(8,7))
    plt.imshow(S, origin="lower")

    plt.xlabel("Time (sec)")
    if(sample_rate and n_samples):
        x_labels = np.round(np.linspace(0, (n_samples/sample_rate), 8), 1)
    plt.xticks(np.round(np.linspace(0, S.shape[1], 8), 1), x_labels)

    plt.ylabel("Frequency (Hz)")
    if(n_samples and sample_rate):
        y_labels = np.round(np.linspace(0, sample_rate/2, 8), 1)
    plt.yticks(np.round(np.linspace(0, S.shape[0], 8), 1), y_labels)

    plt.show()