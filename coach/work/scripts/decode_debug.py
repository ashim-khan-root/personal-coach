import base64

with open('calc-load.xlsx', 'r') as f:
    s = f.read()

check_minus = '-' in s
check_underscore = '_' in s
check_plus = '+' in s
check_slash = '/' in s

print('Contains -:', check_minus)
print('Contains _:', check_underscore)
print('Contains +:', check_plus)
print('Contains /:', check_slash)

# Try URL-safe decoding
try:
    d = base64.urlsafe_b64decode(s)
    print('URL-safe decode:', len(d), 'bytes')
except Exception as e:
    print('URL-safe failed:', e)

# Try stripping = and re-padding
test = s.rstrip('=')
padding = 4 - (len(test) % 4)
if padding == 4:
    padding = 0
test_fixed = test + '=' * padding
print('Rstrip + re-pad:', len(test_fixed), 'mod 4:', len(test_fixed) % 4)
try:
    d = base64.b64decode(test_fixed)
    print('Decoded:', len(d), 'bytes')
except Exception as e:
    print('Failed:', e)

# What if the last group is just wrong and needs to be removed?
# Try removing the last 5 chars and re-padding
for n in range(1, 11):
    test2 = s[:-n]
    test2 = test2.rstrip('=')
    padding = 4 - (len(test2) % 4)
    if padding == 4:
        padding = 0
    test2 = test2 + '=' * padding
    try:
        d = base64.b64decode(test2)
        import zipfile
        with zipfile.ZipFile(open('calc-load_try_'+str(n)+'.xlsx', 'wb')) as zf:
            pass
        with zipfile.ZipFile('calc-load_try_'+str(n)+'.xlsx') as zf:
            print('Remove', n, 'chars: valid ZIP,', len(d), 'bytes, contents:', zf.namelist())
    except zipfile.BadZipFile:
        pass
    except Exception as e:
        pass

# No valid ZIP found? Let me just create a minimal xlsx
