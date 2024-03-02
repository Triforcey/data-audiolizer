
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    from scipy.io.wavfile import write
    import numpy as np
    import json
    packetdata ={}
    with open(dir_path + '/oopsdroppedthis.json', 'r') as f:
        packetdata = json.load(f)

    packetLength = float(packetdata['_source']['layers']['wlan_radio']['wlan_radio.duration'])
    numWaves = 1
    # print(packetLength)
    samplerate = 44100
    packetSpeed = 10
    fs = 1/packetLength
    t = np.linspace(0., 1.*packetLength, int(samplerate*packetLength))
    amplitude = 0;

    ampConst = 1
    startFreq = 5000
    endFreq = 100

    if True:
        # amplitude = (endFreq - startFreq)*2
        amplitude = np.iinfo(np.int16).max*ampConst
    else:
        amplitude = np.iinfo(np.int32).max*ampConst

    # Frequency modulation
    modulation_index = 1.0
    carrier_freq = 1.0 / packetLength
    modulator_freq = startFreq
    # modulator_freq = np.linspace(startFreq,endFreq)
    # modulator = np.sin(2.0 * np.pi * modulator_freq * t)
    modulator = np.linspace(startFreq,endFreq,samplerate)
    product = modulation_index * modulator
    freq_term = np.linspace(startFreq, endFreq, int(samplerate*packetLength))

    data = amplitude * np.tan(2. * np.pi * freq_term * t)

    # if True:
    #     data = amplitude * np.sin(2. * np.pi * fs * t) + startFreq
    # elif True:
    #     data = amplitude * np.cos(2. * np.pi * fs * t) + startFreq
    # else:
    #     data = amplitude * np.tan(2. * np.pi * fs * t) + startFreq
    
    data = data[:int(len(data)*numWaves)]

    print(data)
    write("example.wav", samplerate, data.astype(np.int16))
