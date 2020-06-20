import xml.etree.ElementTree as ET
import numpy
import csv

def parseXML(file_name):

    # XML Namespace Document for Akoma Ntoso Version 1.0
    url = '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}'

    tree = ET.ElementTree(file=file_name)
    root = tree.getroot() # (debate)
    title = ''
    speakerTable = []
    debateTopics = []

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
                # Return the text between the <heading> tag = name of the debate
                title = heading.text
                debateTopics.append(title)
                #print(title)
                #----------------To get parliament speaker---------------#
                for speech in opening.findall(url+'speech'): # <speech> tag
                    for from_ in speech: # <from> & <p> tag
                        # In between the from tag find <person> tag
                        for person in from_.findall(url+'person'):
                            # Return the text between the <person> tag = name 
                            # of parliament speaker
                            speaker = person.text
                            speakerTable.append(speaker)


    print("Topics Number = ", len(debateTopics))
    print("Speaker Number = ", len(speakerTable))
    return debateTopics, speaker


def writeToCSVFile(debateTopics, file_name):
    # specifying the fields for csv file 
    fields = file_name.split('-')

    # writing to csv file 
    with open(file_name, 'w') as csvfile:

        # creating a csv dict writer object 
        csvWriter = csv.writer(csvfile) 
  
        # writing data field names
        csvWriter.writerow(fields)
  
        # writing data rows 
        csvWriter.writerows(debateTopics.items())



if __name__ == "__main__":
    parseXML('SenateHansard1979vol2.xml')