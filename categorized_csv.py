"""
This is the script to convert the generated QA from Alice QG to
separated CSV files based on the QA categories - useful for error analysis

(Evania Lina Fasya - 2017 - https://github.com/evania)

"""

import csv
import re
from lxml import etree as ET


"""
Functions
"""

class QApair:
    def __init__(self):
        self.sentence = ''
        self.category = ''
        self.template = ''
        self.question = ''
        self.answer = ''
    
def readQA(inputFile):
    QAtree = ET.parse(inputFile)
    QAroot = QAtree.getroot()
    qaList = []
    for sentence in QAroot.findall('sentence'):
        #semObjectList = []
        sentenceWord = sentence.get('word')
        for qa in sentence.findall('qa'):
            obj = QApair()
            obj.sentence = sentenceWord
            obj.category = qa.get('category')
            obj.template = qa.get('template')
            obj.question = (qa.find('question')).text
            obj.answer = (qa.find('answer')).text
            qaList.append(obj)
    return qaList

def writeCsv(qaList, cat):
    file = open("err_analysis_"+cat+".csv", "wb")
    for qa in qaList:
        #json.dump(p,sys.stdout)
        file.write(qa.template)
        file.write(",")
        file.write('"'+qa.question+'"')
        file.write(",")
        file.write('"'+qa.answer+'"')
        file.write(",")
        file.write('"'+qa.sentence+'"')
        file.write("\n")



"""
Running the program
"""

qaAnalysis = readQA('generated_qa.xml')

cat_MTMP = []
cat_MMNR = []
cat_MLOC = []
cat_MADV = []
cat_ARGU = []
cat_DCNJ  = []

for qa in qaAnalysis:
    MTMP = re.search("MTMP", qa.category)
    MMNR = re.search("MMNR", qa.category)
    MLOC = re.search("MLOC", qa.category)
    MADV = re.search("MADV", qa.category)
    ARGU = re.search("ARGU", qa.category)
    DCNJ = re.search("DCNJ", qa.category)
    if MTMP is not None:
        cat_MTMP.append(qa)
    if MMNR is not None:
        cat_MMNR.append(qa)
    if MLOC is not None:
        cat_MLOC.append(qa)
    if MADV is not None:
        cat_MADV.append(qa)
    if ARGU is not None:
        cat_ARGU.append(qa)
    if DCNJ is not None:
        cat_DCNJ.append(qa)
    #print 'sentence:', qa.sentence
    #print 'question:', qa.question
    #print 'answer  :', qa.answer
    #print 'category:', qa.category
    #print 'template:', qa.template
    #print ''

writeCsv(cat_MTMP, 'MTMP')
writeCsv(cat_MMNR, 'MMNR')
writeCsv(cat_MLOC, 'MLOC')
writeCsv(cat_MADV, 'MADV')
writeCsv(cat_ARGU, 'ARGU')
writeCsv(cat_DCNJ, 'DCNJ')
