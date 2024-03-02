import numpy as np
from scipy.io.wavfile import write

import numpy as np
from scipy.io.wavfile import write

def create_beat(gap, frequency, bpm, volume, thump_length_ms, pitch):
    # Parameters
    samplerate = 44100  # Sample rate in Hz
    beat_duration = 60 / bpm  # Duration of a beat in seconds
    thump_duration = thump_length_ms / 1000  # Duration of the thump in seconds
    t_beat = np.arange(int(samplerate * beat_duration)) / samplerate  # Time array for one beat
    t_thump = np.arange(int(samplerate * thump_duration)) / samplerate  # Time array for the thump

    # Create the beat
    beat = volume * np.sin(2 * np.pi * frequency * pitch * t_beat)  # Signal for the beat

    # Create the thump
    thump = volume * np.sin(2 * np.pi * frequency * pitch * t_thump)  # Low-frequency sine wave

    # Create the gap
    gap_duration = gap / 1000  # Duration of the gap in seconds
    gap = np.zeros(int(samplerate * gap_duration))  # Silence for the gap

    # Create a rhythm by repeating the beat, thump and gap
    rhythm = np.concatenate((beat, thump, gap))

    # Write the data to a WAV file
    write('beat.wav', samplerate, (rhythm * np.iinfo(np.int16).max).astype(np.int16))

# Call the function with your parameters
create_beat(gap=500, frequency=440, bpm=120, volume=0.5, thump_length_ms=100, pitch=1)


# Call the function with your parameters
create_beat(gap=500, frequency=440, bpm=120, volume=0.5, crash_length_ms=100, pitch=1)