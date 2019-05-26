import numpy as np

def sine_hz(fs, duration, f):
    # fs: sample rate (Hz, int)
    # duration: duration of sine wave (sec, float)
    # f: frequency of sine wave (Hz, float)
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    return samples

def dft(x, N=None, abs=True):
    if(not N):
        N = len(x)

    X = []
    for k in range(N):
        X.append(np.sum([x[n] * np.exp((1j * -2 * np.pi * k * n) / N) for n in range(N)]))
    if(abs):
        X = np.abs(X)
    return X

def stft(x, nfft, overlap=128, sample_rate=44100):
    STFT = []
    for n in range(0, len(x), nfft):
        x_trim = x[max(0, n-overlap):max(0, n-overlap)+nfft] # Use a rectangular window
        dft_x = dft(x_trim)
        STFT.append(dft_x)
    
    return STFT