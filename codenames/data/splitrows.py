import sys

for line in sys.stdin:
    if not line:
        continue
    for w in line.split(','):
        if w:
            print(w.strip())
