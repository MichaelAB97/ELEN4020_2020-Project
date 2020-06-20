import xml.etree.ElementTree as ET

def parseXML(file_name):

    # XML Namespace Document for Akoma Ntoso Version 1.0
    url = '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}'

    tree = ET.ElementTree(file=file_name)
    root = tree.getroot() # (debate)
    title = ''

    # Children Tags of parent root (debate):
    # child 1 = meta        | index = 0
    # child 2 = coverPage   | index = 1
    # child 3 = preface     | index = 2
    # child 4 = debateBody  | index = 3

    rootNodeIndex = 0 #base node index = 0 as there is one parent for many children
    childIndex= 3 

    # For loop iteration to find the debate topics in the xml
    # At the root node along child 3 (debateBody)
    for child in root[rootNodeIndex][childIndex]: # debateSection
        for opening in child.findall(child.tag): 
            #Find <heading> tag in each of the debateSection children
            for heading in opening.findall(url+'heading'): 
                # Return the text between the <heading> tag = name of the debate
                title = heading.text 
                print(title)

    return title


if __name__ == "__main__":
    parseXML('SenateHansard1979vol2.xml')