#!/usr/bin/python3.4
# George Nicol
# cryptopals: set 1 challenge 4
# March 26, 2015
#
# Sometimes you need to use a cannon.
#
# accepts an incoming file as an argument, file assumed to be straight hex
# 1) makes the conversion of all strings based on that xor'd character
# 2) attempts to determine if resulting string is gargabe by pattern matching for common
#       words. If any of the common words are in the resulting string, both the original
#       and the result are written (to an output file).
#
# This would be decent for regular text, the more the better (like a letter) and terribad for passwords


import sys, string
import argparse
import re

# ---------------------------------------------------------------------
# my own error class to throw around

class AllDone(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


# ---------------------------------------------------------------------
#  decodes the line
def decodeLine(xorValue, hexString):
    decodedString=''
    hexString=hexString.strip(string.whitespace)                        # always that pesky \n
    for i in range(0,len(hexString),2):                                 # go by twos because that's a byte
        decodedString+=(chr((int(hexString[i:i+2], 16)) ^ xorValue))    # cast it right, I miss C right about now
    return decodedString


# ---------------------------------------------------------------------
# parse dem args

parser = argparse.ArgumentParser(description="read in args, get file names for incoming data")

parser.add_argument('-f', dest='path', action='store', default=list(), nargs=1, required=True, help="path to file containing data to XOR and character (ascii text) to try as most common")

args, unknown = parser.parse_known_args()

grepValue1=re.compile("the")
grepValue2=re.compile("and")
grepValue3=re.compile("that")
resultString=''

try:
    #outFile = open("results.txt",'w')
    # brute force with the list from above
    for xorValue in range (0x00,0xff):
        inFile = open(args.path[0], 'r')
        for lineOfCoded in inFile:
            if (len(lineOfCoded) != 0): # empty line
                # decode it with the number you are on
                resultString = decodeLine(xorValue, lineOfCoded)
                # begin automated checks of results for english language (ratehr than gibberish)
                # maybe we can use the strip thing too but in this example we try an alternate route
                # but basically grepping out for common words.
                # When I used grep on the command line before the pipe broke on the non-printable characters
                # in the string ... grep would probably work now if you  stripped out the whitespace
                # and would likely be faster...
                #if resultString.strip(string.whitespace).isprintable():
                #    print("key: {0} .. results: {1} ... orig {2}".format(chr(xorValue), resultString, lineOfCoded))
                    #outFile.write(resultString)
                if grepValue1.search(resultString):
                    print("key: {0} .. results: {1} ... orig {2}".format(chr(xorValue), resultString, lineOfCoded))
                if grepValue2.search(resultString):
                    print("key: {0} .. results: {1} ... orig {2}".format(chr(xorValue), resultString, lineOfCoded))
                if grepValue3.search(resultString):
                    print("key: {0} .. results: {1} ... orig {2}".format(chr(xorValue), resultString, lineOfCoded))

        inFile.close()
    outFile.close()


except AllDone as e:
    print("Look in results.txt; xor value was {0}".format(e.value))

except OSError as e:
    print("{0} not found.\n".format(args.path[0]))
