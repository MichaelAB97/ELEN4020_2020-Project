import xml.etree.ElementTree as ET
import numpy as np
import csv
from collections import defaultdict , ChainMap
from math import ceil
import threading
import time

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
                    peopleArray = removeDuplicate(peopleArray) #removes any duplications

                if not peopleArray:
                    continue
                else:
                    for person in peopleArray:
                        debateTopics.setdefault(title, []).append(person) #
                        speakerTable.setdefault(person, []).append(title) #returns the default values for missing keys

    for keys in debateTopics:
        debateTopics[keys] = removeDuplicate(debateTopics[keys])

    return debateTopics, speakerTable


def removeDuplicate(peopleList):
    return list(dict.fromkeys(peopleList))


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


# This function makes uses of the built-in mapping data structure functionality in python
# to group multiple dictionaries to a single mapping. So when a chain search is done on
# this map, it will return the values of the first key.
def createChainMap(dict_1, dict_2):
    chain = ChainMap(dict_1, dict_2)
    return chain

def chainSearch(chainMap, searchQuery_1, searchQuery_2):
    allSpeakersinDebates = []

    resultArray_1 = chainMap.get(searchQuery_1)
    resultArray_2 = chainMap.get(searchQuery_2)

    allSpeakersinDebates.append(resultArray_1)
    allSpeakersinDebates.append(resultArray_2)
    
    return allSpeakersinDebates
    

if __name__ == "__main__":
    debates, speakers = parseXML('SenateHansard1979vol2.xml')
    writeToCSVFile(debates, 'debatesBySpeakers') 
    writeToCSVFile(speakers, 'speakersInDebates')
    cMap = createChainMap(debates, speakers)
    writeToCSVFile(cMap, 'chainMap')
    #print(cMap)
    #createMap(debates, speakers)
    
    f = open("map.txt", "w")
    f.write(str(cMap))
    f.close()

    #Indexing used to find all the speakers that participated in two specific debates
    result_1 = chainSearch(cMap, 'ESTIMATE OF EXPENDITURE, 1979-’80', 'ALLEGED OMISSION OF WORDS FROM OFFICIAL REPORT OF SENATE DEBATES (HANSARD)')
    print(result_1)
    print("============================" *4)
    # Indexing used to find the debates in which two speakers participated in
    result_2 = chainSearch(cMap, 'L. E. D. WINCHESTER', 'MINISTER OF LABOUR')
    print(*result_2)

