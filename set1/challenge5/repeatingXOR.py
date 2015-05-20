#!/usr/bin/python
# George Nicol
# cryptopals: set 1 challenge
# May 20, 2015
#
# Requires file and key as input, (en/de)codes file accordingly based on
# cycling through provided key byte by byte.
#
# wants ascii as input, willl encode to hex and then encrypt using key.
# results -> stdout


import binascii as binA
import sys, string
import argparse
import re

# ---------------------------------------------------------------------
# my own error class to throw around

class BadArgs(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)



# ---------------------------------------------------------------------
# usage
def usage():
  print("usage: repeatingXOR.py [-h] [-f PATH] [-t TEXT] -k KEY [-e] [-d]")




# ---------------------------------------------------------------------
# parse dem args

parser = argparse.ArgumentParser(description="read args, get mode, file name & key.")
parser.add_argument('-f', dest='path', action='store', nargs=1, help="path to file to en/decode")
parser.add_argument('-t', dest='text', action='store', nargs=1, help="text to en/decode")
parser.add_argument('-k', dest='key', action='store', nargs=1, required=True, help="key in ascii to en/de-code with")
parser.add_argument('-e', action='store_true', help="encode")
parser.add_argument('-d', action='store_true', help="decode")


args, unknown = parser.parse_known_args()
decodedString=''

try:
  # verify correct amount of args
  if args.e is False and args.d is False:
    raise BadArgs("Indicate decode or encode")
  if args.e is True and args.d is True:
    raise BadArgs("Can't both decode and encode")
  if args.path is None and args.text is None:
    raise BadArgs("Need path or text to decode")
  if args.path is not None and args.text is not None:
    raise BadArgs("Not both path and text")


  if args.text is not None:
    args.text=args.text[0]

  # put the text in
  if args.path is not None:
    f = open(args.path[0], 'r')
    args.text= f.read()
    f.close()

  # get stats on the key length so we can cycle through it using mod
  # and set up vars for coming ops
  # convert the text into hex
  args.text=args.text.strip(string.whitespace)
  args.text = binA.hexlify(args.text)
  args.key  = binA.hexlify(args.key[0])
  keyLength = len(args.key)
  textCount = 0

  # the meat of it all
  for i in args.text:
    xorValue=int(args.key[textCount%keyLength],16)
    decodedString+=hex(int(i, 16) ^ xorValue)[2]     # cast it right, I miss C right about now
    textCount+=1

  print(decodedString)

except BadArgs as e:
  usage()
  print("{0}".format(e.value))

except OSError as e:
  print("{0} not found.\n".format(args.path[0]))
