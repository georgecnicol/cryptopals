#! /usr/bin/python3.4
# George Nicol
# February 2, 2015

# read from a file converting all characters within the file from hex (treats them as hex)
# to base64, assumes file consists entirely of hex [0-9A-Fa-f]

import sys


# ensure file provided
argc=len(sys.argv)
if argc != 2:
    exit (1)



# pack portions of the raw data into 12 bit chunks
# 3 digits x 4 bits/digit = 12 bits
def convertString(incoming):
    hexTriplet=int(0)
    for char in incoming:
        hexTriplet += int(char, 16)
        hexTriplet = hexTriplet << 4
    hexTriplet = hexTriplet >> 4        # one shift too many in loop
    return hexTriplet


# of the 12 bits, take 6 (lsb portion) of it and make a value
def makeBase64Lower(incomingHex):
    maskLower=0x03F
    lowerVal=incomingHex & maskLower
    return lowerVal


# of the 12 bits, take 6 (msb portion) of it and make a value
def makeBase64Upper(incomingHex):
    upperVal = incomingHex >> 6
    return upperVal


# now that we have the unpacked 2 digit (0-63) representation, we can decode via array.
def changeToBase64(incoming):
    alpahbet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    translatedChar=alpahbet[incoming]
    return translatedChar


try:
    # variables
    rawData=''              # raw hex digits in a string
    temp=''                 # a subportion of the above of at most 3 packed hex digits  (0-F)   4 bits/digit x 3 digits = 12 bits
    base64List=[]           # list of integers corresponding to unpacked base64         (0-63)  6 bits/digit X 2 digits = 12 bits
    finalString=''          # the base64 completed conversion as an ascii string
    count=0

    # get the raw data and throw out that trailing \n
    for line in open(sys.argv[1]):
        val = line.upper()
        rawData += val[0:-1]

    # repackage it as base64, note that we cycle through
    # the input by groups of three. Any remainders are handled
    # further down.
    for char in rawData:
        count+=1
        modVal=count%3
        temp+=char
        if (modVal==0):
            hexValue=convertString(temp)
            base64List.append(makeBase64Upper(hexValue))
            base64List.append(makeBase64Lower(hexValue))
            temp=''

    # account for not a multiple of three
    # Only translate the top portion beacuse there
    # weren't enough characters to make a bottom
    # portion. Need to add an = sign
    # even though we add 00 that is merely for the
    # purpose of sizing the input - we truncate
    # the excess by not including a bottom.
    if(modVal==1):
        temp+="00"
        hexValue=convertString(temp)
        base64List.append(makeBase64Upper(hexValue))

    # there were enough to make a bottom, but there
    # are extra zeros, which will be accounted for
    # with the == signs
    if(modVal==2):
        temp+="0"
        hexValue=convertString(temp)
        base64List.append(makeBase64Upper(hexValue))
        base64List.append(makeBase64Lower(hexValue))


    # decode our numbers (0-63) into characters...
    for num in base64List:
        finalString+=changeToBase64(num)

    # format according to specifications indicating how
    # many additional zeroes are on the end of the base64
    # string. This flag indicates for going the other direction
    if(modVal==1):
        finalString+="="
    if(modVal==2):
        finalString+="=="

    # display/ save answer as desired...
    print(finalString)
    with open('results.txt','w') as f:
        f.write(finalString)
        f.write('\n')
    f.close()

except IOError as e:
    print(e)

