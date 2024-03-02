import { spawn } from 'child_process';
import { resolve } from 'path';
import readline from 'readline';

const readPcapngFile = async (pcapngFile: string) => {
  const path = resolve(process.cwd(), pcapngFile);
  const tshark = spawn('tshark', ['-r', path], {
    stdio: 'pipe',
  });
  const rl = readline.createInterface({
    input: tshark.stdout,
    output: process.stdout,
    terminal: false
  });
  rl.on('line', (line) => {
    console.log(line);
  });
};

export default readPcapngFile;
