
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def flatten_json(json_obj, flat_json={}):
    for key in json_obj:
        if isinstance(json_obj[key], dict):
            flatten_json(json_obj[key], flat_json)
        else:
            flat_json[key] = json_obj[key]
    return flat_json
if __name__ == "__main__":

    from scipy.io.wavfile import write
    import numpy as np
    import json
    # from flatten_json import flatten
    packetdata ={}
    with open(dir_path + '/oopsdroppedthis.json', 'r') as f:
        packetdata = json.load(f)
    packetdata = flatten_json(packetdata)
    # print(packetdata)
    packetLength = float(packetdata['frame.len'])/10
    fromMac=packetdata['wlan.sa'].split(":")
    toMac=packetdata['wlan.da'].split(":")
    numWaves = 1
    # print(packetLength)
    samplerate = 44100
    packetSpeed = 10
    fs = 1/packetLength
    linTo = 1.
    t = np.linspace(0., linTo*packetLength, int(samplerate*packetLength))
    amplitude = 0;

    ampConst = 1
    startFreq = 0
    endFreq = 1000

    if True:
        # amplitude = (endFreq - startFreq)*2
        amplitude = np.iinfo(np.int16).max*ampConst
    else:
        amplitude = np.iinfo(np.int32).max*ampConst

    modShifter=2
    modSpeed = 2.
    if False:
        modulator = np.linspace(startFreq, endFreq, int(samplerate*packetLength))
    elif True:
        # Create a sine wave modulator
        modulator = np.sin(modSpeed * np.pi * t / packetLength)  # One cycle over the packet length
        modulator = startFreq + (endFreq - startFreq) * (modulator + 1) / modShifter  # Shifts the modulator
    else:
        modulator = np.tan(2.0 * np.pi * t / packetLength)  # One cycle over the packet length
        modulator = startFreq + (endFreq - startFreq) * (modulator + 1) / modShifter  # Shifts the modulator

    if True:
        data = amplitude * np.sin(2. * np.pi * modulator * t)
    elif True:
        data = amplitude * np.cos(2. * np.pi * modulator * t)
    else:
        data = amplitude * np.tan(2. * np.pi * modulator * t)

    # if False:
    #     #maybe secondary wave here idk
    
    data = data[:int(len(data)*numWaves)]

    print(data)
    write("example.wav", samplerate, data.astype(np.int16))
