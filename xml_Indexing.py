import xml.etree.ElementTree as ET
import numpy as np
import csv
from collections import defaultdict , ChainMap
import threading
import time
import multiprocessing
from os import getpid
from joblib import Parallel, delayed
from math import ceil

map = {}
BitMap = {}

MAX_THREADS = 1

def parseXML(file_name):

    # XML Namespace Document for Akoma Ntoso Version 1.0
    url = '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}'

    tree = ET.ElementTree(file=file_name)
    root = tree.getroot() # (debate)
    title = ''
    speakerTable = {}
    debateTopics = {}

    # Children Tags of parent root (debate):                       (         debate         )
    # child 1 = meta        | index = 0                           /       /         \        \
    # child 2 = coverPage   | index = 1                         meta  coverPage  preface  debateBody
    # child 3 = preface     | index = 2
    # child 4 = debateBody  | index = 3

    rootNodeIndex = 0 #base node index = 0 as there is one parent for many children
    childIndex= 3 

    #----------------To get debate topics-------------------#
    # For loop iteration to find the debate topics in the xml
    # At the root node along child 3 (debateBody)
    for child in root[rootNodeIndex][childIndex]: # debateSection
        for opening in child.findall(child.tag): 
            #Find <heading> tag in each of the debateSection children
            for heading in opening.findall(url+'heading'): 
                peopleArray = []
                # Return the text between the <heading> tag = name of the debate
                title = heading.text
                #print(title)
                #----------------To get parliament speaker---------------#
                for speech in opening.findall(url+'speech'): # <speech> tag
                    for from_ in speech: # <from> & <p> tag
                        # In between the from tag find <person> tag
                        for person in from_.findall(url+'person'):
                            # Return the text between the <person> tag = name 
                            # of parliament speaker
                            speaker = person.text
                            peopleArray.append(speaker)
                    peopleArray = list(dict.fromkeys(peopleArray)) #removes any duplications
                
                # Appends speakers and debates to their respective lists, if they are in the people Array
                if peopleArray:
                    for person in peopleArray: #Key-value pairings
                        debateTopics.setdefault(title, []).append(person) #returns the default values for missing keys
                        speakerTable.setdefault(person, []).append(title) #returns the default values for missing keys
                
    # Removes any topic duplications
    for keys in debateTopics:
        debateTopics[keys] = list(dict.fromkeys(debateTopics[keys]))

    return debateTopics, speakerTable


# Writes the list to a CSV file with the given file_name
def writeToCSVFile(debateTopics, file_name):

    # specifying the fields for csv file 
    fields = file_name.split('-')

    # writing to csv file 
    with open(file_name + '.csv', 'w') as csvfile:

        # creating a csv dict writer object 
        csvWriter = csv.writer(csvfile) 
  
        # writing data field names
        csvWriter.writerow(fields)
  
        # writing data rows 
        csvWriter.writerows(debateTopics.items())


def BitMapIndexing(start, end):
    key = BitMap['widthKeys'][start: end]
    for key, val in zip(key, range(start, end)):
        for elem in BitMap['dictTop'][key]:
            length = BitMap['heightKeys'].index(elem)
            map[length][val] = 1



def createBitMap(top, side):

    # Obtaining the sizes for the Bit Map using the size of the dictionary
    # results of the xml parser
    width = len(top)
    height = len(side)
    dimensions = (height, width)

    # Creating initial map which is populated by zeroes
    global map
    map = np.zeros(dimensions)

    # Obtaining the keys from the results of the xml parser
    widthKeys = list(top.keys())
    heightKeys = list(side.keys())
    
    # Creating Bit Map Dictionary
    global BitMap
    BitMap = { 'heightKeys': heightKeys, 'dictTop': top, 'widthKeys': widthKeys }


    
if __name__ == "__main__":
    debates, speakers = parseXML('SenateHansard1979vol2.xml')
    writeToCSVFile(debates, 'debatesBySpeakers') # Indexing used to find the debates in which two speakers participated in
    writeToCSVFile(speakers, 'speakersInDebates')# Indexing used to find all the speakers that participated in two specific debates
    createBitMap(debates, speakers)

    # Parallelisation of Bit Map Indexing using Threads
    threads = list()
    start = 0 
    threadWidth = ceil(len(debates)/MAX_THREADS) #Divide Map into partitions for the threads

    for threadIndex in range(MAX_THREADS):
        startTime = time.time()
        end = start + threadWidth
        thread = threading.Thread(target=BitMapIndexing, args=(start, end))
        threads.append(thread)
        thread.start()
        start = end # new start is the end of the last partition
        
    for index, thread in enumerate(threads):
        thread.join()

    endTime = time.time()
    print("Processing Time: " , endTime - startTime, " seconds")
    print(map)
