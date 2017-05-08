#Max Girard Independent Study Spring 2017
#This program takes a text file and
#puts the reference information into a csv file
#and an XML file 


#import the package to use regular expressions
import re

#import the package to export data into a csv file
import csv

#import the package for xml
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

#import time to make directions appear less rapidly
import time

#printout directions on how this program works
print("This program parses text files to extract references from the ")
print("end of journal articles.")
time.sleep(2)
print("You will be propmted to enter the name of the file you wish to parse.")
print("Make sure this file is in the same folder as this Python Code.")
time.sleep(2)
print("Enter the name of the file WITHOUT the .txt ending.")
print("For example, if the file is called file.txt")
print("enter file when promted to enter the file name.")
time.sleep(3)

#input statement to get the name of the file to parse
fileName=input("Enter the name of the text file you wish to use.")

# open a file for writing
Author_data = open(fileName+'.csv', 'w')

# create the csv writer object
csvwriter = csv.writer(Author_data)

#open the file to parse
myfile = open('ajhe_a_00056.txt', 'r', encoding="utf8")

#create an array that will store info to be transferred to csv
bibInfo = ['','','','','','','','','','','','','','']

#create an array for the column names of the csv file
bib_head = []

#create the column names for the csv file
bib_head.append('forename')
bib_head.append('first name')
bib_head.append('middle name')
bib_head.append('title of article')
bib_head.append('journal article is from')
bib_head.append('volume')
bib_head.append('issue number')
bib_head.append('page range')
bib_head.append('status')
bib_head.append('date published')
bib_head.append('author affiliation')
bib_head.append('author email')
bib_head.append('author phone')
bib_head.append('doi')

#add these to the head of the csv file
csvwriter.writerow(bib_head)

#make a counter so that references with multiple authors will still
#be able to have the article information in the CSV file
counter=0

#make a very general format that will apply to every reference
genPattern='[a-zA-Z]{1}[a-zA-Z :.,()]+.\s\d{4}.\s\W{1}[a-zA-Z :]+.\W{1}\s?[a-zA-Z :]+\s?\d+\s?\W{1}\d+\W{1}\s?:\s?\d+\W{1}\d+'

#find the first author listed where the author has lastName,FirstName MiddleInitial.,
#authorNames= (re.findall(r'\D*\,\s\D*\s\D*\.\,', 'text'))
top=Element('references')
comment=Comment('reference for an article')
top.append(comment)


textOfFile=''
for line in myfile:
    data=line.rstrip()
    textOfFile=textOfFile+data

pattern=(re.findall(genPattern, textOfFile))

#run through each recorded reference and extract the relevant information
i=0
while i<len(pattern):
    entry=pattern[i]
    #print(entry)
    i=i+1
    
    #this will get the authors of the article
    authors=(re.findall(r'[A-Z]{1}[a-zA-Z :.,()]+.\s', entry))
    bibInfo[0]=authors[0]
    #this will get the publication date of the referenced article
    datePub=(re.findall(r'\d{4}', entry))
    bibInfo[9]=datePub[0]
    #this will get the title of the article
    title=(re.search(r' [a-zA-Z :.-]+', entry))
    bibInfo[3]=title[0]
    #this will get the name of the journal
    journalLong=(re.findall(r'\W{1}\s?[a-zA-Z :?]+\s\d+', entry))
    if journalLong[0]!="":
        journal=(re.findall(r'\s?[a-zA-Z :?]+', journalLong[0]))
    bibInfo[4]=journal[0]
    #print(bibInfo[4])
    #this will get the page range of the referenced article
    pageRange=(re.findall(r'\d+\W\d+', entry))
    bibInfo[7]=pageRange[0]
    #this will get the volume number of the referenced article
    volume=(re.findall(r'\s\d*\s', entry))
    bibInfo[5]=volume[0]
    #this will get the issue number of the refernced article
    issueNumber=(re.findall(r'\(\d*\)', entry))
    bibInfo[6]=issueNumber[0]

    #add tags around the different parts of the reference
    reference=SubElement(top, 'reference')
    authorsXML=SubElement(reference,'authors')
    authorsXML.text=authors[0]
    pubDateXML=SubElement(reference, 'date')
    pubDateXML.text=datePub[0]
    articleXML=SubElement(reference, 'article')
    #articleXML.text=title[0]
    journalXML=SubElement(reference,'from' )
    journalXML.text=journal[0]
    pageRangeXML=SubElement(reference, 'pages')
    pageRangeXML.text=pageRange[0]
    volumeXML=SubElement(reference, 'volume')
    volumeXML.text=volume[0]
    issueXML=SubElement(reference, 'issue')
    issueXML.text=issueNumber[0]
    #this code is adapted from https://pymotw.com/2/xml/etree/ElementTree/create.html
    xmlstr = ElementTree.tostring(top, encoding='utf8', method='xml')
    #this piece is based off an example I saw at http://stackoverflow.com/questions/3605680/creating-a-simple-xml-file-using-python
    tree=ET.ElementTree(top)
    tree.write(fileName+".xml")
    


    #for loop to throw stuff in to csv
    for p in range(len(bib_head)):
        bib_head[p]=bibInfo[p]
    #write out the row
    csvwriter.writerow(bib_head)
        
    #to clear out the information of each reference
    for t in range(len(bibInfo)):
        bibInfo[t]=""
        bib_head[t]=""
#let the user know the data has been put into the XML and CSV files
print("The files "+fileName+".csv and "+fileName+".xml hav been created.")
print("They are located in the same folder as the original text file.")
#close the files
Author_data.close()
myfile.close()

