declare module 'pcap-ng-parser' {
  import { Writable } from 'stream';
  export type ParsedPacket = {
    interfaceId: number;
    timestampHigh: number,
    timestampLow: number,
    data: Buffer
  };
  const PCAPNGParser: {
    new(): Writable & {
      on(event: 'data', listener: (data: ParsedPacket) => void): this;
    }
  };
  export default PCAPNGParser;
}
