import subprocess
import json
import sys

def read_pcapng_file(pcapng_file, on_packet):
  tshark = subprocess.Popen(['tshark', '-r', pcapng_file, '-T', 'json'], stdout=subprocess.PIPE)
  json_buffer = ''
  for line in iter(tshark.stdout.readline, b''):
    line = line.decode('utf-8').rstrip()
    if line == '[' or line == ']':
      continue
    json_buffer += line
    if line.startswith('  }'):
      if json_buffer.endswith(','):
        json_buffer = json_buffer[:-1]
      packet = json.loads(json_buffer)
      on_packet(packet)
      json_buffer = ''
  return packets

packets = read_pcapng_file(sys.argv[1], lambda packet: print(packet))
