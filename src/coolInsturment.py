
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def flatten_json(json_obj, flat_json={}):
    for key in json_obj:
        if isinstance(json_obj[key], dict):
            flatten_json(json_obj[key], flat_json)
        else:
            flat_json[key] = json_obj[key]
    return flat_json
def coolInsturment(packetdata, samplerate, dontWrite = False):

    from scipy.io.wavfile import write
    import numpy as np
    import json
    # from flatten_json import flatten
    # packetdata ={}
    # with open(dir_path + '/oopsdroppedthis.json', 'r') as f:
    #     packetdata = json.load(f)
    # packetdata = flatten_json(packetdata)
    # print(packetdata)
    packetLength = (float(packetdata['frame.len'])/20.)**1.2
    fromMac=[int(x,16) for x in packetdata['wlan.ta'].split(":")]
    toMac=[int(x,16) for x in packetdata['wlan.ra'].split(":")]
    # print(packetdata['wlan.ra'].split(":"))
    dataRate=(int(packetdata['wlan_radio.data_rate']))
    sigdbm=int(packetdata['wlan_radio.signal_dbm'].lstrip("-"))/1000
    # print(fromMac)
    numWaves = 1
    # print(packetLength)
    # samplerate = 44100
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
    if 100<=fromMac[2]/3 <256:
        modulator = np.linspace(startFreq, endFreq, int(samplerate*packetLength))
    elif 40<fromMac[2]/3 <100:
        # Create a sine wave modulator
        modulator = np.sin(modSpeed * np.pi * t / packetLength)  # One cycle over the packet length
        modulator = startFreq + (endFreq - startFreq) * (modulator + 1) / modShifter  # Shifts the modulator
    else:
        modulator = np.tan(2.0 * np.pi * t / packetLength)  # One cycle over the packet length
        modulator = startFreq + (endFreq - startFreq) * (modulator + 1) / modShifter  # Shifts the modulator
    # if not toMac[3]<=25:
        print(toMac[3])
    if  toMac[3]<=205:
        print('normal stuff')
        if 100<=toMac[2]/3 <256:
            data = amplitude * np.sin(2. * np.pi * modulator * t)
        elif 40<toMac[2]/3 <100:
            data = amplitude * np.cos(2. * np.pi * modulator * t)
        else:
            data = (amplitude * np.tan(2. * np.pi * modulator * t)).astype(np.int16)
            if (not dontWrite): write("example.wav", samplerate, data)
            return data
    elif toMac[3]<=230:
        print('2nd condition')
        samplerate = 44100
        fs1 = min(fromMac[3], fromMac[4]) / (toMac[0] / 32)
        fs2 = max(fromMac[3], fromMac[4]) * (toMac[1] / 32)
        packetLength = 10
        data1 = amplitude * np.sin(2. * np.pi * fs1 * t)
        #data2 = amplitude * np.sin(2. * np.pi * fs2 * t)
        if 170<=toMac[5]/3 <256:
             data2 = amplitude * np.sin(2. * np.pi * fs2 * t)
        elif 85<toMac[5]/3 <170:
             data2 = amplitude * np.cos(2. * np.pi * fs2 * t)
        else:
             data2 = amplitude * np.tan(2. * np.pi * fs2 * t)

    #         data2 = amplitude * np.tan(2. * np.pi * fs2 * t)
        data = (data1 + data2).astype(np.int16)
        if (not dontWrite): write("example.wav", samplerate, data)
        return data
    # elif toMac[3] <0:
    else:
        print('dial up cuh')
        from scipy.io.wavfile import write
        import numpy as np
        samplerate = 44100  # Sample rate in Hz
        freq = fromMac[4]  # Frequency of the beat in Hz (low frequency for a "thump" sound)
        bpm = toMac[4]  # Beats per minute
        volume = 0.5  # Volume of the sound (0 to 1)

        duration = packetLength+1  # Desired total duration in seconds
        t = np.linspace(0., duration, int(samplerate * duration))  # Time array that lasts for 'duration' seconds

        beat_duration = 60 / bpm  # Duration of a quarter note in seconds
        beat = volume * np.sin(2. * np.pi * freq * t[:int(samplerate * beat_duration)])  # Signal for one beat
        silence = np.zeros_like(beat)  # Silence for one beat

        # Create a rhythm by repeating the beat and silence
        rhythm = np.tile(np.concatenate((beat, silence)), int(duration / (2 * beat_duration)))  # Repeat as many times as fit into 'duration'

        # Write the data to a WAV file
        data = (rhythm * np.iinfo(np.int16).max).astype(np.int16)
        if (not dontWrite): write('beat.wav', samplerate, data)
        return data

    # print(data)
