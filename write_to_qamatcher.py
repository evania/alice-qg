"""
This is the script to convert the generated QA from Alice QG to QAMatcher's input format

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

def writeQAmatcher(qa, dialog_id):
    dialog = ET.SubElement(QAroot, 'dialog')
    dialog.set('id', str(dialog_id))
    answer_list = ET.SubElement(dialog, 'answerlist')
    answer_one = ET.SubElement(answer_list, 'answer')
    answer_one.set('type', 'uncertain')
    answer_one.text = qa.answer
    answer_two = ET.SubElement(answer_list, 'answer')
    answer_two.set('type', 'certain')
    answer_two.text = qa.answer
    question_list = ET.SubElement(dialog, 'questionlist')
    question = ET.SubElement(question_list, 'question')
    question.text = qa.question
    


"""
Running the program
"""

#qaAnalysis = readQA('generated_qa.xml') # when using QA pairs without follow-up question strategy
qaAnalysis = readQA('generated_qa_with_follow_up_strategies.xml') # using follow-up question strategy

QAroot = ET.Element('qa_root')

dialog_id = 1

for qa in qaAnalysis:
    writeQAmatcher(qa, dialog_id)
    dialog_id = dialog_id + 1

xml = ET.tostring(QAroot,encoding='utf8', pretty_print=True)
fp = open("vragen.xml", "w")
fp.write(xml)
fp.close
