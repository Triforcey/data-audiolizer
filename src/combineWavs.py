from scipy.io import wavfile
import numpy as np

def combineWavs(wave1, wave2, normalize=False):
  # Ensure both waves have the same length
  max_length = max(len(wave1), len(wave2))
  wave1 = np.pad(wave1, (0, max_length - len(wave1)), 'constant', constant_values=(0))
  wave2 = np.pad(wave2, (0, max_length - len(wave2)), 'constant', constant_values=(0))

  if normalize:
    # Add the waves together
    combined_wave = wave1 + wave2

    # Normalize the volume of the combined wave
    combined_wave_normalized = combined_wave / np.max(np.abs(combined_wave)) if np.max(np.abs(combined_wave)) != 0 else combined_wave

    return combined_wave_normalized
  else:
    # Add the waves together
    combined_wave = wave1 + wave2
    print(np.max(np.abs(combined_wave)))

    return combined_wave
