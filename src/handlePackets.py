from combineWavs import combineWavs
from coolInsturment import coolInsturment
from scipy.io.wavfile import write
from datetime import datetime
import pytz
import numpy as np
import sounddevice as sd
<<<<<<< HEAD
import threading
import pyaudio
=======
>>>>>>> parent of fa2e9e4 (multi threading playing)

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

      if len(wavData) == 0:
        return

      # Play the wave data immediately
      # Normalize the wave data to avoid loud sounds
      wavData = wavData / np.max(np.abs(wavData), axis=0)
<<<<<<< HEAD

      # Create a separate thread for playing the audio
      # Create a PyAudio object
      p = pyaudio.PyAudio()

      # Define callback function for the stream
      def callback(in_data, frame_count, time_info, status):
          data = wavData.astype(np.float32).tostring()
          return (data, pyaudio.paContinue)

      # Open a stream with the callback function
      stream = p.open(format=pyaudio.paFloat32,
              channels=1,
              rate=sampleRate,
              output=True,
              stream_callback=callback)

      # Start the stream
      stream.start_stream()

      # Here, you may want to add some logic to stop the stream when the sound is done playing
      # For example, you could use a threading.Timer with a duration of len(wavData) / sampleRate
      # Remember to also close the PyAudio object when you're done with it
      def stop_stream():
          stream.stop_stream()
          stream.close()
          p.terminate()

      play_duration = len(wavData) / sampleRate
      play_thread = threading.Timer(play_duration, stop_stream)
      play_thread.start()
=======
      sd.play(wavData, sampleRate, blocking=False)
>>>>>>> parent of fa2e9e4 (multi threading playing)
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
