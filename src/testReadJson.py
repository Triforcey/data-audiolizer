
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    from scipy.io.wavfile import write
    import numpy as np
    import json
    packetdata ={}
    with open(dir_path + '/oopsdroppedthis.json', 'r') as f:
        packetdata = json.load(f)

    packetLength = float(packetdata['_source']['layers']['wlan_radio']['wlan_radio.duration'])/10
    numWaves = .25
    # print(packetLength)
    samplerate = 44100
    fs = 1/packetLength
    t = np.linspace(0., 1.*packetLength, int(samplerate*packetLength))
    amplitude = np.iinfo(np.int32).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    data = data[:int(len(data)*numWaves)]

    print(data)
    write("example.wav", samplerate, data.astype(np.int16))
