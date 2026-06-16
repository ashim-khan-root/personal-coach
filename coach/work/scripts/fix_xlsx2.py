import binascii
import base64
import zipfile
import struct

with open('calc-load.xlsx', 'r') as f:
    s = f.read()

# Use binascii.a2b_base64 which has strict_mode parameter
# In Python 3.12+, binascii has this
try:
    d = binascii.a2b_base64(s, strict_mode=False)
    print('binascii lenient decoded:', len(d), 'bytes')
except Exception as e:
    print('binascii lenient failed:', e)
    # Older Python fallback: manually add padding and use standard
    # Let's check our Python version
    import sys
    print('Python version:', sys.version)
    d = None

if d is None:
    # Manual approach: decode 4 chars at a time
    # Skip the last incomplete group
    d = bytearray()
    for i in range(0, len(s) // 4 * 4, 4):
        chunk = s[i:i+4]
        try:
            d.extend(base64.b64decode(chunk))
        except:
            print('Failed on chunk', i, repr(chunk))
            break
    d = bytes(d)
    print('Manual chunked decode:', len(d), 'bytes')

with open('calc-load_manual.xlsx', 'wb') as f:
    f.write(d)

# Check if valid ZIP
try:
    with zipfile.ZipFile('calc-load_manual.xlsx') as zf:
        print('Valid ZIP! Contents:', zf.namelist())
        for name in zf.namelist():
            print('  -', name, zf.getinfo(name).file_size, 'bytes')
except Exception as e:
    print('Not valid ZIP:', e)
    # Dump the structure
    local_count = 0
    for i in range(len(d)):
        if d[i:i+4] == b'PK\x03\x04':
            local_count += 1
            name_len = struct.unpack_from('<H', d, i+26)[0]
            name = d[i+30:i+30+name_len].decode('utf-8', errors='replace')
            print('LOCAL #' + str(local_count) + ' at ' + str(i) + ': "' + name + '"')
        elif d[i:i+4] == b'PK\x01\x02':
            name_len = struct.unpack_from('<H', d, i+28)[0]
            name = d[i+46:i+46+name_len].decode('utf-8', errors='replace')
            print('CENTRAL at ' + str(i) + ': "' + name + '"')
    print('Total locals:', local_count)
