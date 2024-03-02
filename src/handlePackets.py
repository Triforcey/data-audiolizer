from combineWavs import combineWavs
from coolInsturment import coolInsturment
from scipy.io.wavfile import write
from datetime import datetime
import pytz
import numpy as np
import sounddevice as sd

class HandlePackets:
  def progress_bar(self, current, total, eta): 
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

    date_string = packet['frame.time']
    date_format = "%b %d, %Y %H:%M:%S.%f000 %Z"
    date_object = datetime.strptime(date_string, date_format)

    date_object_utc = date_object.replace(tzinfo=pytz.timezone('MST')).astimezone(pytz.utc)
    unix_timestamp = date_object_utc.timestamp()
    if self.initialTimestamp is None:
      self.initialTimestamp = unix_timestamp

    packet_timing = unix_timestamp - self.initialTimestamp

    if self.lastPacketTime is not None:
      if packet_timing - self.lastPacketTime <= .3:
        return
      self.lastPacketTime = packet_timing
    else:
      self.lastPacketTime = packet_timing

    if live:
      wavData = coolInsturment(packet, sampleRate, True)

      if len(wavData) == 0:
        return


      wavData = wavData / np.max(np.abs(wavData), axis=0)
      sd.play(wavData, sampleRate, blocking=False)
      return

    self.counter += 1
    finalRun = self.counter == self.maxPackets

    wavData = coolInsturment(packet, sampleRate, True)

    packet_timing_samples = int(packet_timing * sampleRate)

    buffer = [0] * packet_timing_samples

    buffer.extend(wavData)

    self.totalWav = combineWavs(self.totalWav, buffer, finalRun)

    remaining_packets = self.maxPackets - self.counter
    time_per_packet = (datetime.now(pytz.utc) - date_object_utc).total_seconds()
    eta = remaining_packets * time_per_packet

    print(self.progress_bar(self.counter, self.maxPackets, eta))

    if finalRun:
      print('Length in seconds:', len(self.totalWav) / sampleRate)
      write('output.wav', sampleRate, self.totalWav)
      exit(0)
