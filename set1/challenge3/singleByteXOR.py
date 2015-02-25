#!/usr/bin/python3.4
# George Nicol
# cryptopals: set 1 challenge 3
# Feb 24, 2015


# accepts an incoming file as an argument
# file assumed to be straight hex
# 1) determines most common value in hex (bytewise)
# 2) solves for X where X is the value that when Xor'd with
#    the most common byte yields e.
# 3) decodes incoming file accordingly and displays to stdout
#    asking for confirmation.
# 4) if not accepted repeat steps 2 and 3 with E t T a A o O i I n N
# 5) upon accept output file generated called "results" and Xor value displayed.


import sys
import argparse

# ---------------------------------------------------------------------
# my own error class to throw around

class AllDone(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# ---------------------------------------------------------------------
# returns bool based on user response - simple yes or no will do
def satisfied(decodedAnswer):
    print(decodedAnswer)
    answer = input("Does this look correct? (y/n): ")
    if (answer.upper() == "Y"):
        return True
    return False

# ---------------------------------------------------------------------
# finds the most common element in the file which is then matched to a letter
def findMostCommon(incomingText):
    incomingText=incomingText[0:-1]                 # always that pesky \n
    mySetOfValues={}
    asciiVal=''
    # grab 2 numbers and convert to hex
    for i in range(0,len(incomingText),2):          # take a byte at a time
        asciiVal=int(incomingText[i:i+2], 16)       # take a byte at a time
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
def decodeFile(xorValue, path):
    decodedString=''
    for line in open(path):
        line=line[0:-1]                                                 # always that pesky \n
        for i in range(0,len(line),2):                                  # go by twos because that's a byte
            decodedString+=(chr((int(line[i:i+2], 16)) ^ xorValue))     # cast it right, I miss C right about now
    return decodedString


# ---------------------------------------------------------------------
# parse dem args

parser = argparse.ArgumentParser(description="read in args, get file names for incoming data")

parser.add_argument('-f', dest='path', action='store', default=list(), nargs=1, required=True, help="path to file containing data to XOR")

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

listOfLetters=[0x20,0x65,0x45,0x74,0x54,0x61,0x41,0x6f,0x4f,0x69,0x49,0x6e,0x4e]
mostCommonLetter=''
xorValue=0x00
resultString=''


try:
    # get the files open
    inFile = open(args.path[0])
    outFile = open("results.txt",'w')

    # look through the file and find the most commonly occuring 'symbol'
    incomingText=inFile.read()
    mostCommonLetter = findMostCommon(incomingText)
#    print("most common letter is {0}".format(mostCommonLetter))  # debugging, didn't hit like I thought
    inFile.close()

    # iterate through most common list decoding, spit out the results to look at manually and ask for approval
    for letterToTry in listOfLetters:
        xorValue = findXorValue(mostCommonLetter, letterToTry)
        resultString = decodeFile(xorValue, args.path[0])
        if (satisfied(resultString)):
            outFile.write(resultString)
            outFile.close()
            raise AllDone(xorValue)         # break out of loop by throwing exception. meh.

    print("Failure to decode.")
    outFile.close()

except AllDone as e:
    print("Look in results.txt; xor value was {0}".format(e.value))

except OSError as e:
    print("{0} not found.\n".format(args.path[0]))
