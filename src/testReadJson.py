
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    from scipy.io.wavfile import write
    import numpy as np
    import json
    packetdata ={}
    with open(dir_path + '/oopsdroppedthis.json', 'r') as f:
        packetdata = json.load(f)
    samplerate = 44100; fs = 100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    print(data)
    write("example.wav", samplerate, data.astype(np.int16))
