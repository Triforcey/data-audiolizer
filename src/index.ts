#!/usr/bin/env node
import { parseArgs } from 'util';
import readPcapngFile from './packet-reader.js';

const parsedArgs = parseArgs({ allowPositionals: true });

if (!parsedArgs.positionals.length) throw new Error('pcapngFile is required');
const pcapngFile = parsedArgs.positionals[0];

readPcapngFile(pcapngFile);
