
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
    print(packetdata)
    packetLength = float(packetdata['frame.len'])/10
    fromMac=[int(x,16) for x in packetdata['wlan.ta'].split(":")]
    toMac=[int(x,16) for x in packetdata['wlan.ra'].split(":")]
    dataRate=(int(packetdata['wlan_radio.data_rate']))
    sigdbm=int(packetdata['wlan_radio.signal_dbm'].lstrip("-"))/1000
    # print(fromMac)
    numWaves = 1
    # print(packetLength)
    samplerate = 44100
    packetSpeed = 1
    fs = 1/packetLength
    # linTo = 30.
    linTo = dataRate/20.
    t = np.linspace(0., linTo*packetLength, int(samplerate*packetLength))
    amplitude = 0
    maxFreq = 10000

    ampConst = sigdbm
    startFreq = (fromMac[0]/255) * 10000
    endFreq = (toMac[0]/255) * 10000

    if True:
        # amplitude = (endFreq - startFreq)*2
        amplitude = np.iinfo(np.int16).max*ampConst
    else:
        amplitude = np.iinfo(np.int32).max*ampConst

    modShifter= (fromMac[1]/255)* 5
    modSpeed = (toMac[1]/255)* 5
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
