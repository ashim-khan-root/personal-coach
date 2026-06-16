import struct
import base64
import zipfile

# Read the base64 file
with open('calc-load.xlsx', 'r') as f:
    b64_data = f.read()

# Fix base64: replace last incomplete group
fixed_b64 = b64_data[:980] + 'AA=='
decoded = base64.b64decode(fixed_b64)

print(f'Decoded: {len(decoded)} bytes')

# Find all PK records
local_headers = []
central_headers = []

for i in range(len(decoded)):
    sig = decoded[i:i+4]
    if sig == b'PK\x03\x04':
        name_len = struct.unpack_from('<H', decoded, i+26)[0]
        extra_len = struct.unpack_from('<H', decoded, i+28)[0]
        comp_size = struct.unpack_from('<I', decoded, i+18)[0]
        uncomp_size = struct.unpack_from('<I', decoded, i+22)[0]
        name = decoded[i+30:i+30+name_len].decode('utf-8', errors='replace')
        local_headers.append((i, name, name_len, extra_len, comp_size, uncomp_size))
        print(f'LOCAL #{len(local_headers)} at {i}: "{name}" ({comp_size} bytes -> {uncomp_size})')
    elif sig == b'PK\x01\x02':
        name_len = struct.unpack_from('<H', decoded, i+28)[0]
        extra_len = struct.unpack_from('<H', decoded, i+30)[0]
        comment_len = struct.unpack_from('<H', decoded, i+32)[0]
        local_offset = struct.unpack_from('<I', decoded, i+42)[0]
        name = decoded[i+46:i+46+name_len].decode('utf-8', errors='replace')
        central_headers.append((i, name, name_len, extra_len, comment_len, local_offset))
        print(f'CENTRAL #{len(central_headers)} at {i}: "{name}" local_at={local_offset}')

if local_headers and central_headers:
    # First local header
    first_local = local_headers[0][0]
    cd_start = central_headers[0][0]
    
    # Calculate CD size: last central header end - first central header
    last_cd_start, last_cd_name, last_cd_nl, last_cd_el, last_cd_cl, last_cd_lo = central_headers[-1]
    cd_end = last_cd_start + 46 + last_cd_nl + last_cd_el + last_cd_cl
    cd_size = cd_end - cd_start
    
    print(f'\nLocal 0 at: {first_local}')
    print(f'CD at: {cd_start} (size: {cd_size}, ends at: {cd_end})')
    
    # Build EOCD
    n_files = len(central_headers)
    eocd = struct.pack('<I', 0x06054b50)  # PK\x05\x06
    eocd += struct.pack('<H', 0)  # disk 0
    eocd += struct.pack('<H', 0)  # CD disk 0
    eocd += struct.pack('<H', n_files)  # entries on disk
    eocd += struct.pack('<H', n_files)  # total entries
    eocd += struct.pack('<I', cd_size)  # CD size
    eocd += struct.pack('<I', cd_start)  # CD offset
    eocd += struct.pack('<H', 0)  # no comment
    
    print(f'EOCD (22 bytes): {eocd.hex()}')
    
    # Build valid ZIP: truncated data + EOCD
    valid = decoded[:cd_end] + eocd
    with open('calc-load_valid.xlsx', 'wb') as f:
        f.write(valid)
    print(f'Written: {len(valid)} bytes')
    
    # Validate
    try:
        with zipfile.ZipFile('calc-load_valid.xlsx') as zf:
            print(f'\nValid ZIP! Contents:')
            for name in zf.namelist():
                info = zf.getinfo(name)
                data = zf.read(name)
                print(f'  {name}: {info.file_size} bytes -> {len(data)} read')
    except Exception as e:
        print(f'Invalid ZIP: {e}')
else:
    print('Could not find both local and central headers')
