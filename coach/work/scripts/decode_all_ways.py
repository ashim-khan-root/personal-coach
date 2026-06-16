import base64
import sys

with open('calc-load.xlsx', 'r') as f:
    lines = f.read()

# Try removing different numbers of characters from the end
# and different padding strategies
for remove_end in range(0, 10):
    test = lines[:len(lines)-remove_end] if remove_end > 0 else lines
    
    # Try different padding
    for pad_mode in ['none', 'add', 'replace']:
        if pad_mode == 'none':
            pass  # use as-is
        elif pad_mode == 'add':
            while len(test) % 4 != 0:
                test += '='
        elif pad_mode == 'replace':
            test = test.rstrip('=')
            while len(test) % 4 != 0:
                test += '='
        
        try:
            d = base64.b64decode(test)
            import zipfile, io
            with zipfile.ZipFile(io.BytesIO(d)) as zf:
                names = zf.namelist()
                if names:
                    print(f'Remove {remove_end}, {pad_mode}: VALID ZIP, {len(d)} bytes')
                    print(f'  Files: {names}')
                    for name in names:
                        content = zf.read(name)
                        print(f'    {name}: {len(content)} bytes')
                    sys.exit(0)
        except:
            pass

# Also try binary decoding with various fixes
import struct

# The raw bytes of the file
raw = open('calc-load.xlsx', 'rb').read()
print(f'Raw file size: {len(raw)}')

# Try base64 decode with just the raw bytes interpreted as ASCII
raw_str = raw.decode('ascii')
print(f'Raw as string: {len(raw_str)}')

# The last char
print(f'Last char: {repr(raw_str[-1])} (code {ord(raw_str[-1])})')
print(f'Second-to-last: {repr(raw_str[-2])} (code {ord(raw_str[-2])})')
print(f'Third-to-last: {repr(raw_str[-3])} (code {ord(raw_str[-3])})')

# Try removing trailing newlines/carriage returns
for end_char in ['\n', '\r', '\r\n', '']:
    stripped = raw_str.strip(end_char) if end_char else raw_str
    test = stripped.rstrip('=')
    while len(test) % 4 != 0:
        test += '='
    try:
        d = base64.b64decode(test)
        import zipfile, io
        with zipfile.ZipFile(io.BytesIO(d)) as zf:
            print(f'Stripped {repr(end_char)}: VALID ZIP, {len(d)} bytes, {zf.namelist()}')
    except:
        pass

print('No valid ZIP found with any approach')
print(f'\\nDecoded data stats:')
# Try one more approach - what if the base64 uses different alphabet?
# Try standard base64 with case-insensitive or other variations
