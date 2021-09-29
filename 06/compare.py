import sys


if len(sys.argv) != 3:
    raise AttributeError('compare needs 2 args!')

inpf, outf = sys.argv[1:]

check = True
i = -1

for a, b in zip(open(inpf, 'r').readlines(), open(outf, 'r').readlines()):
    i += 1
    check &= a == b
    if not check: 
        print(f'error @ {i}, a = {a}, b = {b}')
        break

print(check)
