from typing import NamedTuple
import os

class Sequence(NamedTuple):
    name: str
    sequence: str


# read in FASTA file (will read in any number of sequences)
def readFASTA(filename, names = True):
    sequenceList = []
    print("Reading in FASTA file...")
    f = open(filename, 'r')
    lines = f.readlines()
    
    readingSequence = False
    name = ""
    seq = ""
    for line in lines:
        line = line.strip('\n')
        if line != "":
            if (line[0] == '>'):
                if (readingSequence == True):
                    if(names == True):
                        sequenceList.append(Sequence(name, seq))  # finishes the current sequence
                        seq = ""    # resets the sequence to be blank
                    else:
                        sequenceList.append(seq)  # finishes the current sequence
                        seq = ""    # resets the sequence to be blank
                else:
                    readingSequence = True
                
                name = line.strip('> ')
                
            else:
                seq += line
    
    if(names == True):
        # after the end of file is reached, it will add that last sequence
        sequenceList.append(Sequence(name, seq))
    else:
        sequenceList.append(seq)
    
    f.close()
    return sequenceList


def readMultiFASTA(folderName, names = True):
    # print(os.listdir("ZIP"))
    seqList = []
    for fasta in os.listdir(folderName):
        # print(fasta)
        seqList = seqList + readFASTA(f"{folderName}\\{fasta}", names=names)
    return seqList


def writeMultiFASTA(folderName):
    seqList = readMultiFASTA(folderName=folderName)
    f = open("multiFASTA.fasta", "w")
    for seq in seqList:
        f.write(f"> {seq[0]}\n")
        f.write(f"{seq[1]}\n")


# code for testing writing and converting folder to one big FASTA file
writeMultiFASTA("ZIP")