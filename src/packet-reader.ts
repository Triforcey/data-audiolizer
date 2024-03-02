import { spawn } from 'child_process';
import { resolve } from 'path';
import readline from 'readline';

const readPcapngFile = async (pcapngFile: string) => {
  const path = resolve(process.cwd(), pcapngFile);
  const tshark = spawn('tshark', ['-r', path, '-T', 'json'], {
    stdio: 'pipe',
  });
  const rl = readline.createInterface({
    input: tshark.stdout,
    output: process.stdout,
    terminal: false
  });
  let jsonBuffer = '';
  rl.on('line', (line) => {
    if (line === '[') return;
    if (line === ']') return;
    jsonBuffer += line;
    if (line.startsWith('  }')) {
      if (jsonBuffer.endsWith(',')) jsonBuffer = jsonBuffer.slice(0, -1);
      const packet = JSON.parse(jsonBuffer);
      console.log(JSON.stringify(packet, null, 2));
      jsonBuffer = '';
      process.exit(0);
    }
  });
};

export default readPcapngFile;
