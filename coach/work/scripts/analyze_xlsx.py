import base64
import zlib
import struct

with open('calc-load.xlsx', 'r') as f:
    s = f.read()

# Manual chunked decode (skip incomplete last group)
d = bytearray()
for i in range(0, len(s) // 4 * 4, 4):
    chunk = s[i:i+4]
    d.extend(base64.b64decode(chunk))
d = bytes(d)

print('Decoded:', len(d), 'bytes')

# Parse local header
# Offset 0: LOCAL header
if d[:4] == b'PK\x03\x04':
    comp_size = struct.unpack_from('<I', d, 18)[0]
    uncomp_size = struct.unpack_from('<I', d, 22)[0]
    name_len = struct.unpack_from('<H', d, 26)[0]
    extra_len = struct.unpack_from('<H', d, 28)[0]
    crc = struct.unpack_from('<I', d, 14)[0]
    method = struct.unpack_from('<H', d, 8)[0]
    flags = struct.unpack_from('<H', d, 6)[0]
    name = d[30:30+name_len].decode('utf-8', errors='replace')
    header_end = 30 + name_len + extra_len
    
    print()
    print('Local header:')
    print('  Name:', name)
    print('  Method:', method, '(8=deflate, 0=store)')
    print('  Flags:', hex(flags))
    print('  CRC:', hex(crc))
    print('  Comp size:', comp_size)
    print('  Uncomp size:', uncomp_size)
    print('  Extra len:', extra_len)
    print('  Header end:', header_end)
    
    # Data from header_end onwards
    compressed_data = d[header_end:]
    print()
    print('Compressed data:', len(compressed_data), 'bytes')
    print('First 20 bytes:', compressed_data[:20].hex())
    
    # Try to inflate
    try:
        decompressed = zlib.decompress(compressed_data, -zlib.MAX_WBITS)
        print('Decompressed:', len(decompressed), 'bytes')
        print('Content:', decompressed[:500].decode('utf-8', errors='replace'))
    except Exception as e:
        print('Decompress failed:', e)
        # Try with different window bits
        for wbits in [15, -15, 31, 25, -zlib.MAX_WBITS, zlib.MAX_WBITS]:
            try:
                decompressed = zlib.decompress(compressed_data, wbits)
                print('Decompressed with wbits', wbits, ':', len(decompressed), 'bytes')
                print('Content:', decompressed[:500].decode('utf-8', errors='replace'))
                break
            except:
                pass

# Also print out all printable strings in the data
print()
print('Printable strings in decoded data:')
current = ''
for b in d:
    if 32 <= b < 127:
        current += chr(b)
    else:
        if len(current) > 10:
            print(' ', current)
        current = ''
if len(current) > 10:
    print(' ', current)
