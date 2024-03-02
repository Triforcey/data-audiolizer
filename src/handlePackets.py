from combineWavs import combineWavs
from coolInsturment import coolInsturment
from scipy.io.wavfile import write
from datetime import datetime
import pytz
import numpy as np
import sounddevice as sd

class HandlePackets:
  def progress_bar(self, current, total, eta): # Added self as the first parameter
      bar_length = 20
      progress = current / total
      block = int(round(bar_length * progress))
      text = "\rProgress: [{0}] {1:.1f}% ETA: {2}s".format("#" * block + "-" * (bar_length - block), progress * 100, eta)
      return text

  def __init__(self):
    self.initialTimestamp = None
    self.totalWav = np.array([0], dtype=np.int16)
    self.counter = 0
    self.maxPackets = 100
    self.lastPacketTime = None

  def handle(self, packet, live):
    sampleRate = 44100

    # Parse the date string
    date_string = packet['frame.time']
    date_format = "%b %d, %Y %H:%M:%S.%f000 %Z"
    date_object = datetime.strptime(date_string, date_format)

    # Convert the date to UTC and get the unix timestamp
    date_object_utc = date_object.replace(tzinfo=pytz.timezone('MST')).astimezone(pytz.utc)
    unix_timestamp = date_object_utc.timestamp()
    if self.initialTimestamp is None:
      self.initialTimestamp = unix_timestamp

    # Get packet timing is in seconds
    packet_timing = unix_timestamp - self.initialTimestamp

    # Decide if using packet
    if self.lastPacketTime is not None:
      if packet_timing - self.lastPacketTime <= .3:
        return
      self.lastPacketTime = packet_timing
    else:
      self.lastPacketTime = packet_timing

    if live:
      # Get wave data
      wavData = coolInsturment(packet, sampleRate, True)

      # Play the wave data immediately
      sd.play(wavData, sampleRate)
      return

    self.counter += 1
    finalRun = self.counter == self.maxPackets

    wavData = coolInsturment(packet, sampleRate, True)

    # Convert packet timing to samples
    packet_timing_samples = int(packet_timing * sampleRate)

    # Create a silent buffer of the appropriate length
    buffer = [0] * packet_timing_samples

    # Add the wavData at the correct position in the buffer
    buffer.extend(wavData)

    self.totalWav = combineWavs(self.totalWav, buffer, finalRun)

    # Calculate ETA
    remaining_packets = self.maxPackets - self.counter
    time_per_packet = (datetime.now(pytz.utc) - date_object_utc).total_seconds()
    eta = remaining_packets * time_per_packet

    # Print progress bar
    print(self.progress_bar(self.counter, self.maxPackets, eta))

    if finalRun:
      print('Length in seconds:', len(self.totalWav) / sampleRate)
      write('output.wav', sampleRate, self.totalWav)
      exit(0)
