#!/usr/local/bin/python3.4
# George Nicol
# cryptopals: set 1 challenge 4
# March 26, 2015
#
# This version trys to be smart by examining only a list of the most common letters
#
# accepts an incoming file as an argument, file assumed to be straight hex
# 1) makes the conversion of all strings based on that xor'd character
# 2) attempts to determine if resulting string is gargabe by seeing if it is a printable string
#       and the successful results are written (to an output file).
# 3) recall most common characters are: _space_ e E t T a A o O i I n N


import sys, string
import argparse

# ---------------------------------------------------------------------
# my own error class to throw around

class AllDone(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


# ---------------------------------------------------------------------
# finds the most common element in the file which is then matched to a letter
def findMostCommon(incomingText):
    incomingText=incomingText.strip(string.whitespace)  # always that pesky \n
    mySetOfValues={}
    asciiVal=''
    # grab 2 numbers and convert to hex
    for i in range(0,len(incomingText),2):              # take a byte at a time
        asciiVal=int(incomingText[i:i+2], 16)           # take a byte at a time
        mySetOfValues[asciiVal] = mySetOfValues.get(asciiVal, 0) + 1 # get the key and value in the dictionary
        asciiVal=''
    return(max(mySetOfValues, key=mySetOfValues.get))   # return the key with the biggest value - it has occured the most!


# ---------------------------------------------------------------------
# this is its own function where you pass it lowerE then upperE, etc...
def findXorValue(mostCommonLetter, passedInLetter):
    xorResult=0
    for xorValue in range(0x00,0xff):
        xorResult = mostCommonLetter ^ xorValue
        if xorResult == passedInLetter:
            return xorValue                         # return the value that you found not that result of the testing


# ---------------------------------------------------------------------
#  decodes the file
def decodeLine(xorValue, hexString):
    decodedString=''
    hexString=hexString.strip(string.whitespace)                    # always that pesky \n
    for i in range(0,len(hexString),2):                                  # go by twos because that's a byte
        decodedString+=(chr((int(hexString[i:i+2], 16)) ^ xorValue))     # cast it right, I miss C right about now
    return decodedString


# ---------------------------------------------------------------------
# parse dem args

parser = argparse.ArgumentParser(description="read in args, get file names for incoming data")

parser.add_argument('-f', dest='path', action='store', default=list(), nargs=1, required=True, help="path to file containing data to XOR and character (ascii text) to try as most common")

args, unknown = parser.parse_known_args()


# ---------------------------------------------------------------------
# ascii values for __ e E t T a A o O i I n N
# space_=0x20
# lowerE=0x65
# upperE=0x45
# lowerT=0x74
# upperT=0x54
# lowerA=0x61
# upperA=0x41
# lowerO=0x6f
# upperO=0x4f
# lowerI=0x69
# upperI=0x49
# lowerN=0x6e
# upperN=0x4e
# period=0x2e
# s = 0x73
# S = 0x53
# h = 0x68
# H = 0x48
# r = 0x72
# R = 0x52

listOfLetters=[0x20,0x65,0x45,0x74,0x54,0x61,0x41,0x6f,0x4f,0x69,0x49] # expand as needed,0x6e,0x4e,0x2e,0x73,0x53,0x68,0x48,0x72,0x52]
mostCommonLetter=''
xorValue=0x00
resultString=''
letterToTry=''

try:
    #outFile = open("results.txt",'w')
    # "brute force" with the list from above
    for letterToTry in  listOfLetters:
        inFile = open(args.path[0], 'r')
        for lineOfCoded in inFile:
            if (len(lineOfCoded) != 0): # empty line
                # look through the file line by line and find the most commonly occuring 'symbol'
                mostCommonLetter = findMostCommon(lineOfCoded)

                # decode it with given letter (argument)
                xorValue = findXorValue(mostCommonLetter, letterToTry)
                resultString = decodeLine(xorValue, lineOfCoded)

                # begin automated checks of results for english language (ratehr than gibberish)
                # this can still trip up if there is weird blank space embedded in the thing
                # which on the first pass, it was embedded at the end
                # you can see on some of the other entries there are tabs and other weirdness that come up
                # but if you are expecting reasonable formatting behavior, this is not terrible
                if resultString.strip(string.whitespace).isprintable():
                    print("key: {0} .. results: {1} ... orig {2}".format(chr(letterToTry), resultString, lineOfCoded))
                    # put it in a file if you want
                    #outFile.write(resultString)

        inFile.close()
    #outFile.close()



except AllDone as e:
    print("Look in results.txt; xor value was {0}".format(e.value))

except OSError as e:
    print("{0} not found.\n".format(args.path[0]))
