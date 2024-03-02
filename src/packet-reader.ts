import { createReadStream } from 'fs';
import PCAPNGParser from 'pcap-ng-parser';

const readPcapngFile = (pcapngFile: string) => {
  const fileStream = createReadStream(pcapngFile);
  fileStream.on('error', err => {
    console.error('Error reading file:', err);
    process.exit(1);
  });
  const parser = new PCAPNGParser();
  fileStream.pipe(parser);
  parser.on('data', (packet) => {
    console.log(packet);
  });
};

export default readPcapngFile;
