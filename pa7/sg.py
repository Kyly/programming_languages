#!/usr/bin/env python

import ff

alpha = "abcdefghijklmnopqrstuvwxyz"

def openOutputFiles(pre):
    return dict([(a,open(pre + "-" + a, "a")) for a in alpha])
    
def closeAllFiles(d):
    for x in d:
        d[x].flush()
        d[x].close()

def writeKeyAndVal(f, key, val):
    f.write("#".join(key))
    f.write("###")
    f.write("#".join(val))
    f.write("\n")

def readKeyAndVal(filename, s):
    toks = s.strip().split("###")
    try:
        keys = toks[0].split("#")
        vals = toks[1].split("#")
        return keys, vals
    except:
        raise Exception("corrupted file: " + filename)

def mapWorkerPhase1(corpusFilename, chunkNum, chunkSize):
    # open 26 files for writing
    outFileDict = openOutputFiles("output/map1")
    # call map on each line of input and write out results
    inFile = open("output/%s-%.2d" % (corpusFilename, chunkNum))
    lineno = 1 + chunkNum * chunkSize
    for s in inFile:
        inKey, inVal = [corpusFilename, str(lineno)], [s.strip()]
        for (outKey, outVal) in ff.map1(inKey, inVal):
            writeKeyAndVal(outFileDict[outKey[0][0]], outKey, outVal)
        lineno += 1
    # close all files
    inFile.close()
    closeAllFiles(outFileDict)
    
def mapWorkerPhase2(c):
    # open 26 files for writing
    outFileDict = openOutputFiles("output/map2")
    # call map on each line of input and write out results
    fn = "output/reduce1-" + c
    inFile = open(fn)
    for s in inFile:
        inKey, inVal = readKeyAndVal(fn, s)
        for (outKey, outVal) in ff.map2(inKey, inVal):
            writeKeyAndVal(outFileDict[outKey[0][0]], outKey, outVal)
    # close all files
    inFile.close()
    closeAllFiles(outFileDict)
        
def reduceWorker(oneOrTwo, c, reducer):
    # open 26 files for writing
    outFileDict = openOutputFiles("output/reduce" + oneOrTwo)
    # read in file, cluster list of values for each word, call reducer, write out
    d = {}
    fn = "-".join(["output/map" + oneOrTwo, c])
    inFile = open(fn)
    for s in inFile:
        inKey, inVal = readKeyAndVal(fn, s)
        inKey = tuple(inKey)
        if inKey in d:
            d[inKey].append(inVal)
        else:
            d[inKey] = [inVal]
    for inKey in d:
        inVals = d[inKey]
        outVal = reducer(list(inKey), inVals)
        writeKeyAndVal(outFileDict[inKey[0][0]], inKey, outVal)
    # close all files
    inFile.close()
    closeAllFiles(outFileDict)
    
def reduceWorkerPhase1(c): reduceWorker("1", c, ff.reduce1)
    
def reduceWorkerPhase2(c): reduceWorker("2", c, ff.reduce2)
        
def runBothPhases(chunkSize, inputFiles):
    ff.clearOutputFolder()    
    for corpusFilename in inputFiles:
        numChunks = ff.splitFile(corpusFilename, chunkSize)
        # phase 1 map
        for i in range(numChunks): mapWorkerPhase1(corpusFilename, i, chunkSize)
    # phase 1 reduce
    for c in alpha: reduceWorkerPhase1(c)
    # phase 2 map
    for c in alpha: mapWorkerPhase2(c)
    # phase 2 reduce
    for c in alpha: reduceWorkerPhase2(c)

def mostCommonFragment(w):
    fn = "output/reduce2-" + w[0]
    f = open(fn)
    for s in f:
        keys, vals = readKeyAndVal(fn, s)
        if keys[0] == w:
            f.close()
            return vals
    f.close()
    return None
        
def genSentence(w, c):
    """Generates a sentence starting with word w made up of c fragments."""
    if w[0].isalpha() <> True: return None
    w = w.lower()
    sen = w
    for i1 in range(c):
        l = mostCommonFragment(w)
        if l == None: return None   #if a word cannot be found
        for i in range(4):
            sen += " "+l[i]
        w = l[3]
    return sen

