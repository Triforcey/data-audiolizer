import { createReadStream } from 'fs';

const readPcapngFile = (pcapngFile: string) => {
  const fileStream = createReadStream(pcapngFile);
  fileStream.on('error', err => {
    console.error('Error reading file:', err);
    process.exit(1);
  });
};

export default readPcapngFile;
