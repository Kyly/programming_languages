#!/usr/bin/env python

import re
import os

alpha = "abcdefghijklmnopqrstuvwxyz"

def clearOutputFolder():
    for f in os.listdir("output/"):
        os.unlink("output/" + f)
        
def splitFile(filename, n):
    """Splits a file filename into multiple files, each of maximum
       n lines. Output files are saved as output/filename-00,
       output/filename-01, and so on."""
    in_file = open(filename)
    line = in_file.readline()
    count = 0
    while line <> "":
        if count < 10: num = "0"+str(count)
        else: num = str(count)
        f = open("output/"+filename+"-"+num,"w")
        for i in range(n):
            if line == "": break
            f.write(line)
            line = in_file.readline()
        f.close()
        count += 1
    return count
            
            

def map1(inKey, inVal):
    """inKey is a list of two strings, the originating input file name
       and line number. inVal is a list of one string that contains the
       text from the specified line. This function returns a list of
       pairs such that the first element in the pair is a list of five
       consecutive words from the input file and the second element is
       a list of three strings (the string "1" to represent a count of
       occurrences of this sequence, the originating input file, and
       the line number."""
    filename, linenum = inKey[0], inKey[1]
    s = inVal[0].lower().strip()
    s = re.sub("['\"]", "", s)
    s = re.sub("[^A-Za-z0-9']", " ", s)
    words = [w for w in s.split(" ") if w != ""]
    result = []
    for i in range(4, len(words)):
        temp = [words[c] for c in range(i-4,i+1) if words[c][0].isalpha()]
        if len(temp) == 5: result.append((temp,["1",filename,linenum]))
    return result

def reduce1(inKey, inVals):
    """Counts the number of times a five word sequence (represented by
       a 5 string list) appears. inVals is a list of one or more elements
       like outVal from map1"""
    outVal = [str(len(inVals)), inVals[0][1], inVals[0][2]]
    for val in inVals:
        if val[1] < outVal[1]: outVal[1], outVal[2] = val[1], val[2]
        elif val[1] == outVal[1] and int(outVal[2]) > int(val[2]):
            outVal[1], outVal[2] = val[1], val[2]
    return outVal
    
def map2(inKey, inVal):
    """Returns a list of a single tuple including a list of the first
       element in inKey and a list of the remaining elements in inKey
       concatenated with the elements in inVal"""
    return [([inKey[0]],inKey[1:]+inVal)]
    
def reduce2(inKey, inVals):
    """Returns the list in inVal that has the largest count."""
    outVal = inVals[0]
    for val in inVals:
        if int(val[4]) > int(outVal[4]): outVal = val
        elif int(val[4]) == int(outVal[4]):
            if val[5] < outVal[5]: outVal = val
            elif val[5] == outVal[5] and int(outVal[6]) > int(val[6]):
                outVal = val
    return outVal
