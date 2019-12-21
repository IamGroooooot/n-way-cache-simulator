# 20182705 고주형
# Computer Architecture Project 2019
# N-Way Asscociative Cache Simulator
# 32-bit Address
# LRU policy

import math # for log
import sys  # for getting cmd argument

# function for checking if number is power of 2 (ex) 1, 2, 4, ...
# if argument is not power of two then prints error message and exit program
def IsPowerOfTwo(number):
    # in case of "not power of two or not one"
	if not (number == 1 or (number != 0 and number%2 == 0)):
        # print error message
		print("<"+number+"> is invalid argument value. it must be power of two")
		exit()
		
# parse input text that is read from input text file
def ParseInputText(rawText):
    # split rawText's lines by \n
    memSequences = rawText.splitlines()

    # check input format
    try:
        _hex = ""
        for _hex in memSequences:
            int(_hex, 16)
    except:
        # if it is not hex-number exit program
        print("(" + _hex + ")" + " <- This memory squence has wrong format." )
        print("Check input text file. It must only contain hex numbers.")
        exit()

    return memSequences

# parse given inputString
# returns number of set, number of blocks in a set, number of word in a block
# it also checks if the given argument or command is correct
def ParseCommand(inputString, mode=0):
    # split inputstring to tokens
    if(mode == 0):
        # if cmd mode
        inputTokens = inputString
    else:
        # if program input mode
        inputTokens = inputString.split(" ")

    # checks if the correct number of argument is given
    if len(inputTokens) == 0:
        print("no input is given.")
        exit()
    elif len(inputTokens) < 8:
        print("more argument is needed, did you put input file name?")
        exit()
    elif(len(inputTokens) > 8):
    	print("too much argument.")
    	exit()
    else:
        # check if the first command is "cache_simulator"
        if inputTokens[0] !=  "cache_simulator":
            print("wrong command, check if you typed cache_simualator correctly.")
            exit()
        else:
            # if all inputs are correct save remaining tokens into cmdList
            cmdList = inputTokens[1:]
            
    # initialize variable to use
    _set=0          # for -s argument value
    _block=0        # for -n argument value
    _word=0         # for -m argument value
    option = ""     # for checking argument 
    file = ""       # for input file name argument value

    # iterate all elements in the cmdList and parse it
    for idx, cmd in enumerate(cmdList):
        # when idx%2==1; its value(cmd) is number of option
        if idx%2 == 1:
            # convert cmd string into int type
            cmdNumber = int(cmd)
            # save value into corresponding option's valiable
            if option == "-s":
                # check if the value is power of two
                IsPowerOfTwo(cmdNumber)
                _set = cmdNumber
            elif option == "-n":
                # check if the value is power of two
                IsPowerOfTwo(cmdNumber)
                _block = cmdNumber
            elif option == "-m":
                # check if the value is power of two
                IsPowerOfTwo(cmdNumber)
                _word = cmdNumber
            elif option !="":
                file = cmd

            # initialize option
            option=""
        else:
            # when idx%2==0; its value(cmd) is type of argument
            # check if it is correct argument option
            if cmd == "-s" or cmd == "-n" or cmd == "-m":
                option = cmd
            # if unkwon option is found print error and exit program
            elif cmd.startswith("-"):
                print("unknown argument option ("+cmd+").")
                exit()
            else:
            # in case of input file name save it to file variable
                file = cmd
    # return tuple of parsed values
    return (_set, _block, _word, file)

# converts binary string to int
def BinaryStringToInt(bString):
    return int(bString, 2)

# converts int to binary string
def IntToBinaryString(myInt):
    return bin(myInt)

# converts hex string to int
def HexStringToInt(hString):
    return int(hString, 16)

# converts int to hex string
def IntToHexString(myInt):
    return hex(myInt, 16)

# Get File Object that points to given fileName
def GetFileObject(fileName):
    # check if file exists
    try:
        fileIO = open(inputFileName, "r")
    except:
        # if not exists exit program with error message
        print("There is no such file: "+"\""+inputFileName+"\"")
        exit()
    # return opened file object
    return fileIO

# Save outputString to file
def SaveOutputString(filename, outputString):
    # if there is dot in the file name
    # like A.in set saveFile name into A.out 
    if "." in filename:
        filename = filename[:filename.find(".")] + ".out"
    else:
        # else just put .out at the end of opened fileName
        filename += ".out"

    # open to save
    fileIO = open(filename, "w")
    # write *.out file
    fileIO.write(outputString)
    # close fileIO
    fileIO.close()


    

# this is Block's data class
class Data:
    tag = 0 # tag data
    memoryData = 0 # memoryData: it wouldn't be used but I put this to be more realistic
    recentlyUsedTime = 0 # for LRU implementation

    # constructor
    # it initializes value
    def __init__(self, tag=0, memData=0):
        self.tag = tag
        self.memoryData = memData
        self.recentlyUsedTime = 0

    # compare Tag with parameter
    def CompareTag(self, _tag):
        if self.tag == _tag:
            return True
        else:
            return False
    
    # update time
    def RecentlyUsed(self):
        self.recentlyUsedTime = 0

    # update time
    def UpdateTime(self, t = 1):
        self.recentlyUsedTime = t

    # convert this object's data to string
    def ToString(self):
        return "Tag: " + str(self.tag) + ", Memory Data: " + str(self.memoryData)

# cache class
class Cache:
    BYTEOFFSET_MASK = 0
    WORDOFFSET_MASK = 0
    SETINDEX_MASK = 0
    TAG_MASK = 0
    WORDOFFSET_SHIFT = 0
    SETINDEX_SHIFT = 0
    TAG_SHIFT = 0

    # Cache Table: Dictionary(cache_index(KEY), data(VALUE))
    blocks_InSet = 0
    sets_InCache = 0
    words_InBlock = 0

    table = {}
    hit = 0
    miss = 0

    # constructor 
    def __init__(self, sets, blocks, words):
        self.table = {}
        self.hit = 0
        self.miss = 0
        self.blocks_InSet = blocks
        self.sets_InCache = sets
        self.words_InBlock = words
        self.BYTEOFFSET_MASK = 0
        self.WORDOFFSET_MASK = 0
        self.SETINDEX_MASK = 0
        self.TAG_MASK = 0        
        self.WORDOFFSET_SHIFT = 0
        self.SETINDEX_SHIFT = 0
        self.TAG_SHIFT = 0
        # after initializing member variable construct MASK bit and calculate shift amount
        self.ConstructMasks()

        # insert empty sets in a cache in table
        for i in range(0, sets):
            self.table.update({i : {}})

    # construct bit mask for ease of extracting tag, set_index, word_offset, byte_offset 
    def ConstructMasks(self):
        # 4byte is fixed so just make mask for it.
        # so, last two bit is make of byte offset
        self.BYTEOFFSET_MASK = BinaryStringToInt("11")

        # mask of word offset is number of log_2(words_InBlock) bit 
        # from the end of BYTEOFFSET_MASK bit's end
        wordBitCount = round(math.log2(words_InBlock))
        wordMaskString = "1"*wordBitCount
        wordMaskString += "00"
        self.WORDOFFSET_MASK = BinaryStringToInt(wordMaskString)
        # assign how much I needed to SHIFT after masking to get word offset
        self.WORDOFFSET_SHIFT = 2

        # mask of set index is bumber of log_2(sets_InCache) bit 
        # from the end of WORDOFFSET_MASK bit's end
        setIndexBitCount = round(math.log2(sets_InCache))
        setMaskString = "1"*setIndexBitCount
        setMaskString += "0"*wordBitCount

        setMaskString += "00"
        self.SETINDEX_MASK = BinaryStringToInt(setMaskString)
        # assign how much I need to SHIFT after masking to get set index
        self.SETINDEX_SHIFT = 2 + wordBitCount

        # tag mask is the rest of other masks
        tagMaskString = "1"*(32 - (wordBitCount + setIndexBitCount + 2))
        tagMaskString += "0"*setIndexBitCount
        tagMaskString += "0"*wordBitCount
        tagMaskString += "00"
        self.TAG_MASK = BinaryStringToInt(tagMaskString)
        # assign how much I need to SHIFT after masking to get tag
        self.TAG_SHIFT = 2 + wordBitCount + setIndexBitCount


    # finds block by block address in hex-number-string
    def FindBy(self, address):
        addressInt = HexStringToInt(address)

        # extract set index
        setIndex = (addressInt & self.SETINDEX_MASK) >> self.SETINDEX_SHIFT

        # extract tag
        tag = (addressInt & self.TAG_MASK) >> self.TAG_SHIFT
        # get table by set index
        targetSetTable = self.table.get(setIndex)

        exists = False
        # from that table search all index and find if it is hit or miss
        # by key which is tag
        for _tag, _val in targetSetTable.items():
            if _tag == tag:
                exists = True

        # if the tag exists
        if exists:
            # count hit
            self.hit = self.hit + 1

            # get data and set recentlyUsed Time to zero which means I just Accessed it
            blockData = targetSetTable[tag]
            blockData.RecentlyUsed()
            
            print(address + " | HIT")
            return address + " | hit\n"

        else:
            # count miss
            self.miss = self.miss + 1

            # in here I expect to access memory and get data
            retrievedData = 0 # do AccessMemory(address)

            # insert block
            self.InsertBlock(setIndex, tag, retrievedData)

            print(address + " | MISS")
            return address + " | miss\n"

        # Update Time for LRU implementation
        for _, setTable in self.table.items():
            for _, blockData in setTable:
                # update(plus one) recentlyUsedTime
                blockData.UpdateTime()

    # inserts Block in the correspoding set table and if the table is full do LRU replacement
    def InsertBlock(self, setIndex, tag, data=0):
        # get setTable by setIndex
        targetSetTable = self.table.get(setIndex)

        # check if the setTable is full
        # when not full
        if len(targetSetTable) < self.blocks_InSet:
            targetSetTable.update({ tag : Data(tag, data)})
        else: # when set table is full do Replacement by LRU
            # pop Least Recently Used one
            targetSetTable.pop(self.FindLRUBlock(targetSetTable))
            # insert block that i just missed
            targetSetTable.update({ tag : Data(tag, data)})
            
    # find the least recently used block in the given set Table
    # which is the Block that has largest LRUtime value
    # I updated(plus one) Block Data's LRUtime whenever cache has accessed by block address
    def FindLRUBlock(self, setTable):
        # Least Recently Used one's tag
        LRUTag = -1
        # least Recently Used Time this should be biggest among setTable entries
        LRUtime = -1

        # key is tag and value is Data instance
        for _key, _val in setTable.items():
            if LRUtime < _val.recentlyUsedTime:
                LRUtime = _val.recentlyUsedTime
                LRUTag = _key

        return LRUTag
    # it formats string of total outcome
    def ToString(self):
        # convert all cache data to string and return
        return "---------------------------------\n"\
        + ">> number of cache hits: " \
        + str(self.hit) \
        + "\n>> number of cache misses: " \
        + str(self.miss) + "\n"\
        + "---------------------------------\n"\


# variables to use in cache simulator
sets_InCache = 2 # s
blocks_InSet = 1 # n
words_InBlock = 1 # m
inputFileName = ""
outputString = ""
memoryAccessSequences = []

# read command from CMD
inputCommandList = sys.argv
# if argument is given cut first element
if(len(inputCommandList)>1):
    inputCommandList = inputCommandList[1:]
    sets_InCache, blocks_InSet, words_InBlock, inputFileName = ParseCommand(inputCommandList, 0)
else:
    # when no argument is given by cmd and just runed
    inputString = input()
    sets_InCache, blocks_InSet, words_InBlock, inputFileName = ParseCommand(inputString, 1)

# construct n-way cache based on given command
cache = Cache(sets_InCache, blocks_InSet, words_InBlock)

# read input text file
fileObject = GetFileObject(inputFileName)
# parse all text string into memoryAccessSequences
memoryAccessSequences = ParseInputText(fileObject.read())
# close the opened file
fileObject.close()

# simulate cache with given sequence which is memoryAccessSequences
for blockAddress in memoryAccessSequences:
    # save output whether it is hit or not
    outputString += cache.FindBy(blockAddress)

# save total output string
outputString += cache.ToString()

# print output
print(cache.ToString())

# save output string into file
SaveOutputString(inputFileName, outputString)