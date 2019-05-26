import numpy as np
import matplotlib.pyplot as plt

def sine_hz(sample_rate, duration, freq):
    # sample_rate: sample rate (Hz, int)
    # duration: duration of sine wave (sec, float)
    # freq: frequency of sine wave (Hz, float)
    samples = (np.sin(2*np.pi*np.arange(sample_rate*duration)*freq/sample_rate)).astype(np.float32) # just construct a regular sine wave with a frequency f, irrelevant to the DFT itself
    return samples

def dft(x, N=None, real=True): # Implement the regular DFT algorithm.
    # x: the input signal (float[])
    # N: typically just len(x) but represents the number of samples in the input (int)
    # rl: whether or not to convert the complex-valued output of the DFT "X" to a real number by taking np.abs(X)
    if(not N): # if N is set then skip
        N = len(x)

    X = [] # the output of the DFT
    for k in range(int(N/2)): # Accounting for the Nyquist frequency and DFT folding
        X.append(np.sum([x[n] * np.exp((1j * -2 * np.pi * k * n) / N) for n in range(N)]))
    if(real): # real or complex?
        X = np.abs(X)
    return X

def stft(x, nfft, sample_rate, overlap=None):
    # The short-time Fourier transform (STFT) is essentially just a bunch of DFT outputs of small segments of the initial signal combined into one matrix.
    # x: the input signal (float[])
    # nfft: the number of samples to use for each DFT in the STFT. This also determines the frequency resolution, as the DFT maps an input set {x_n} --> {X_k} in a 1:1 correspondence. As X_k represents frequency bins, having more means a higher frequency resolution.
    # sample_rate: the sample rate of the input signal.
    # overlap: the number of samples that overlap in each DFT. Typically left as nfft/2.
    STFT = []
    if(overlap == None):
        overlap = int(nfft/2)

    for n in range(0, len(x), nfft):
        x_trim = x[max(0, n-overlap):max(0, n-overlap)+nfft] # Use a rectangular window, trimming the signal down for each individual DFT.
        dft_x = dft(x_trim) # run the DFT on the trimmed part of the signal
        STFT.append(dft_x) # add back to the original STFT, and construct this piece by piece.
    
    return np.swapaxes(np.array(STFT), 0, 1), len(x) # The array is vertical, not horizontal. Note that len(x) is just the total number of samples

def show_spectrogram(S, sample_rate=None, n_samples=None): # Typically n_samples is the second output len(x) of the stft function, although neither are necessary just for the raw graph
    # S: the spectrogram output of stft() (float[][])
    # sample_rate: sample rate of the original signal (optional, int)
    # n_samples: the number of samples in the original signal (optional, int)
    fig = plt.figure(figsize=(8,7))
    plt.imshow(S, origin="lower") # Set the origin to the bottom left of the screen.

    plt.xlabel("Time (sec)")
    if(sample_rate and n_samples):
        x_labels = np.round(np.linspace(0, (n_samples/sample_rate), 8), 1) # This just labels the time axis of the spectrogram -- if we know the number of samples and the sample rate, simple division allows us to find the length.
    plt.xticks(np.round(np.linspace(0, S.shape[1], 8), 1), x_labels) # Draw the x-axis labels to the screen in equally spaced intervals across the graph, instead of at pixel numbers.

    plt.ylabel("Frequency (Hz)")
    if(sample_rate):
        y_labels = np.round(np.linspace(0, sample_rate/2, 8), 1) # We only graph up to sample_rate/2 Hz because of the Nyquist frequency (i.e., we can only be sure of a frequency up to half the sample rate.)
    plt.yticks(np.round(np.linspace(0, S.shape[0], 8), 1), y_labels) # Draw the y-axis labels to the screen in equally spaced intervals across the graph, instead of at pixel numbers.

    plt.show() # Show the plot.