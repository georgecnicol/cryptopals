#!/usr/bin/python3.4
# George Nicol
# cryptopals: set 1 challenge 2
# Feb 5, 2012
# sure there is an easier way, but the challenge said work
# with raw bytes.

import sys
import argparse


#---------------------
# set up parsing for fun

parser = argparse.ArgumentParser(description="read in args, get file names for incoming data")

parser.add_argument('-f', dest='path', action='store', default=list(), nargs=2, required=True, help="two paths to files containing data to XOR")

args, unknown = parser.parse_known_args()


#---------------------
# vars

xorA=''         # contents of files given
xorB=''
answer=''       # xor results made into a string



# grab contents of file and slice off \n
for line in open(args.path[0]):
    xorA=line
    xorA=xorA[0:-1]

# grab contents of file and slice off \n
for line in open(args.path[1]):
    xorB=line
    xorB=xorB[0:-1]

# must be same length to XOR for this version
# could do something different with zip()
if len(xorA) != len(xorB):
    print("contents of files differ in length: aborted")
    sys.exit(-1)

# resulting list of xor
for position in range(len(xorA)):
    answer+=(hex(int(xorA[position], 16) ^ int(xorB[position], 16)))[2:] # .upper() if you want


print(answer)

