import subprocess
import json
import sys

from handlePackets import HandlePackets

start = 0
counter = 0

def flatten_json(json_obj, flat_json={}):
    for key in json_obj:
        if isinstance(json_obj[key], dict):
            flatten_json(json_obj[key], flat_json)
        else:
            flat_json[key] = json_obj[key]
    return flat_json

def read_pcapng_file(pcapng_file, on_packet, interface):
  global counter
  global start
  live = False
  if (pcapng_file == '-'): live = True
  tshark = subprocess.Popen(['tshark', '-r', pcapng_file, '-T', 'json'], stdout=subprocess.PIPE) if not live else subprocess.Popen(['tshark', '-Ii', interface, '-T', 'json'], stdout=subprocess.PIPE)
  json_buffer = ''
  activateParsing = False
  for line in iter(tshark.stdout.readline, b''):
    line = line.decode('utf-8').rstrip()
    if line == '[':
      activateParsing = True
      continue
    if line == ']':
      activateParsing = False
      continue
    if not activateParsing:
      continue
    json_buffer += line
    if line.startswith('  }'):
      if json_buffer.endswith(','):
        json_buffer = json_buffer[:-1]
      packet = json.loads(json_buffer)
      counter += 1
      if (counter >= start):
        on_packet(flatten_json(packet), live)
      json_buffer = ''
interface = None
if (len(sys.argv) >= 3): interface = sys.argv[2]
read_pcapng_file(sys.argv[1], HandlePackets().handle, interface)
