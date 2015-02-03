#! /usr/bin/python3.4
# George Nicol
# February 2, 2015


# read from a file converting all characters within the file from hex (treats them as hex)
# to base64.


# assumes file consists entirely of hex [0-9A-Fa-f]
# decode the given string from hex to ascii
# encode the decoded string to base64

import sys
import base64           # for alternate version


# ensure file provided
argc=len(sys.argv)
if argc != 2:
    exit (1)



# this works but doesn't operate on raw bytes.
# which is a requirement of the game.
val=""
try:
    # get the contents of the file into a string
    # have to skip the appended '\n'
    for line in open(sys.argv[1]):
        val=line.upper()
        val=val[0:-1]

    base64str=base64.b16decode(val)
    newBase=base64.b64encode(base64str)

    #strip off the b' ' stuff for formatting
    newBase=str(newBase)[2:-1]

    # save the results
    print(newBase)
    with open('results.txt','w') as f:
        f.write(str(newBase))
        f.write('\n')
    f.close()


except IOError as e:
    print(e)



