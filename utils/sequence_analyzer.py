#!/usr/bin/python3

import sys

log_file = sys.argv[1]

last_seq = 10000000000000

def get_sequence(sequences = []):
    global last_seq
    s = []
    log = [ line for line in open(log_file) if 'ANALYZE' in line]
    for line in log:
        x = line.split('ANALYZE@')
        count = int(x[1])
        seq_num = int(x[2])
        s.append(seq_num)
    s.sort()
    for seq_num in s:
        missing = seq_num - last_seq - 1
        if missing > 0:
            sequences.extend([0] * missing)
            sequences.append(seq_num)
        else:
            sequences.append(seq_num)
        last_seq = seq_num
    return sequences

def get_missing_seq(sequences):
    missing = []
    prev = 0
    for s in sequences:
        if s == 0 and prev != 0 :
            missing.append(prev + 1)
        prev = s
    return missing

s = get_sequence()
m = get_missing_seq(s)
#print(s)
print(m)