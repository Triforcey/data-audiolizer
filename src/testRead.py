import numpy as np
import scipy.io.wavfile as wavf
# Open the WAV file
wav_file = open("StarWars3.wav", "rb")

# Read the data from the file
data = np.fromfile(wav_file, dtype=np.int16)

# Close the file
wav_file.close()

# Print the data
# with np.printoptions(threshold=np.inf):
#     print(data)

if __name__ == "__main__":

    from scipy.io.wavfile import write
    import numpy as np
    samplerate = 44100; fs = 100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    write("example.wav", samplerate, data.astype(np.int16))