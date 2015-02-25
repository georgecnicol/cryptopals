#!/usr/bin/python3.4
# George Nicol
# cryptopals: set 1 challenge 2
# Feb 5, 2015
# sure there is an easier way, but the challenge said work
# with raw bytes.

import sys, string
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
    xorA+=line.strip(string.whitespace)

# grab contents of file and slice off \n
for line in open(args.path[1]):
    xorB+=line.strip(string.whitespace)

# must be same length to XOR for this version
# could do something different with zip()
if len(xorA) != len(xorB):
    print("contents of files differ in length: aborted")
    sys.exit(-1)

# resulting list of xor
for position in range(len(xorA)):
    #xor the things position by position, cast as hex, and slice off the leading hex text, append the results
    answer+=(hex(int(xorA[position], 16) ^ int(xorB[position], 16)))[2:] # .upper() if you want


print(answer)

