"""
This is the main script for Alice Question Generation System

(Evania Lina Fasya - 2017 - https://github.com/evania)

"""

from bllipparser import RerankingParser
import StanfordDependencies
import csv
import re
from lxml import etree as ET
import os, sys


"""
Dependency parsing 
"""
def getTokenWord(tokenText):
    tokenText = tokenText
    tokenAttribute = re.search("form='[^\']+", tokenText)
    if tokenAttribute is None:
        tokenAttribute = tokenAttribute = re.search('form="[^\"]+', tokenText)
    tokenAttributePrint = tokenAttribute.group(0)
    tokenText = re.split('=', tokenAttributePrint)[1]
    tokenTextPrint = re.split("'", tokenText)[1] 
    return tokenTextPrint

def getTokenIndex(tokenText):
    tokenText = tokenText
    tokenAttribute = re.search('index=[0-9]+', tokenText)
    tokenAttributePrint = tokenAttribute.group(0)
    tokenIndex = re.split('=', tokenAttributePrint)[1]
    return tokenIndex

def getTokenCpos(tokenText):
    tokenText = tokenText
    tokenAttribute = re.search("cpos='[^\']+", tokenText)
    if tokenAttribute is None:
        tokenAttribute = tokenAttribute = re.search('form="[^\"]+', tokenText)
    tokenAttributePrint = tokenAttribute.group(0)
    tokenCpos = re.split('=', tokenAttributePrint)[1]
    tokenCposPrint = re.split("'", tokenCpos)[1] 
    return tokenCposPrint

def getTokenPos(tokenText):
    tokenText = tokenText
    tokenAttribute = re.search("pos='[^\']+", tokenText)
    if tokenAttribute is None:
        tokenAttribute = tokenAttribute = re.search('form="[^\"]+', tokenText)
    tokenAttributePrint = tokenAttribute.group(0)
    tokenPos = re.split('=', tokenAttributePrint)[1]
    tokenPosPrint = re.split("'", tokenPos)[1]
    return tokenPosPrint

def getTokenHead(tokenText):
    tokenText = tokenText
    tokenAttribute = re.search('head=[0-9]+', tokenText)
    tokenAttributePrint = tokenAttribute.group(0)
    tokenHead = re.split('=', tokenAttributePrint)[1]
    return tokenHead

def getTokenDeprel(tokenText):
    tokenText = tokenText
    tokenAttribute = re.search("deprel='[^\']+", tokenText)
    tokenAttributePrint = tokenAttribute.group(0)
    tokenDeprel = re.split('=', tokenAttributePrint)[1]
    tokenDeprelPrint = re.split("'", tokenDeprel)[1]
    return tokenDeprelPrint

def getDependency(dependencyInput):
    parsedtext = rrp.simple_parse(dependencyInput)
    # Parse the PENN TreeBank format text using Stanford Dependency Parsing
    sd = StanfordDependencies.get_instance(backend='subprocess')
    sent = sd.convert_tree(parsedtext)
    return sent




"""
Semantic role labelling 
"""

def getSRL():
    workPath = os.getcwd()
    srlInputFile = workPath+'/senna/output.txt'
    with open(srlInputFile) as f:
        slines = f.readlines()
    sentenceListSRL = []
    forSRobj = []
    srlCounter = 1
    for l in slines:
        row = re.split(r'\t+', l)
        if row[0] != '\n':
            srlword = str(row[0]).strip()
            mainverb = str(row[1]).strip()
            srlresult = []
            try:
                srlresult.append(str(row[2]).strip())
            except:
                foo='bar'
            column = 3
            while (len(row) != 0) and (column < len(row)):
                srlresult.append(str(row[column]).strip())
                column = column + 1
            forSRobj.append([srlCounter, srlword, mainverb, srlresult])
            srlCounter = srlCounter + 1
        else:
            sentenceListSRL.append(forSRobj)
            forSRobj = []
            srlCounter = 1
    return sentenceListSRL





"""
Semantic Representation
"""

class SemanticRepresentation:
    
    def __init__(self):
        self.wordid = 0
        # The following variables are for Dependency Parsing Result
        self.depword = ''
        self.tokenindex = ''
        self.cpos = ''
        self.pos = ''
        self.tokenhead = ''
        self.deprel = ''
        # The following variable(s) are for Semantic Role Labelling Result
        self.srlword = ''
        self.srlmainverb = ''
        self.srlresult = []

def writeSemanticRepresentation(aSentence):
    for aSemObj in aSentence:
        w = ET.SubElement(sentence, 'word')
        w.set('wordid', str(aSemObj.wordid))
        d = ET.SubElement(w, 'dependency')
        depwordXML = ET.SubElement(d, 'depword')
        depwordXML.text = aSemObj.depword
        tokenIndexXML = ET.SubElement(d, 'index')
        tokenIndexXML.text = aSemObj.tokenindex
        cposXML = ET.SubElement(d, 'cpos')
        cposXML.text = aSemObj.cpos
        posXML = ET.SubElement(d, 'pos')
        posXML.text = aSemObj.pos
        headXML = ET.SubElement(d, 'head')
        headXML.text = aSemObj.tokenhead
        deprelXML = ET.SubElement(d, 'deprel')
        deprelXML.text = aSemObj.deprel
        srl = ET.SubElement(w, 'srl')
        srlwordXML = ET.SubElement(srl, 'srlword')
        srlwordXML.text = aSemObj.srlword
        srlmainverbXML = ET.SubElement(srl, 'srlmainverb')
        srlmainverbXML.text = aSemObj.srlmainverb
        column = 0
        while len(aSemObj.srlresult) > column: # while there are more than 1 column of the SRL result
            srlresultXML = ET.SubElement(srl, 'srlresult')
            srlresultXML.set('column', str(column+1))
            srlresultXML.text = aSemObj.srlresult[column]
            column = column + 1
            
        



"""
Question Generation
"""

def readSemRep():
    QGtree = ET.parse('semantic_representation.xml')
    QGroot = QGtree.getroot()
    sentenceList = []
    for sentence in QGroot.findall('sentence'):
        semObjectList = []
        #srlword = ''
        #srlmainverb = ''
        #srlresult = ''
        for word in sentence.findall('word'):
            semObject = SemanticRepresentation()
            srl = word.find('srl')
            dependency = word.find('dependency')
            semObject.wordid = word.get('wordid')
            semObject.depword = (dependency.find('depword')).text
            semObject.tokenindex = (dependency.find('index')).text
            semObject.cpos = (dependency.find('cpos')).text
            semObject.pos = (dependency.find('pos')).text
            semObject.tokenhead = (dependency.find('head')).text
            semObject.deprel = (dependency.find('deprel')).text
            semObject.srlword = (srl.find('srlword')).text
            semObject.srlmainverb = (srl.find('srlmainverb')).text
            #srlresultdict = {}
            for srlresult in srl.findall('srlresult'):
                semObject.srlresult.append(srlresult.text)
            semObjectList.append(semObject)
        sentenceList.append(semObjectList)
    return sentenceList

def getV(vList):
    vs = []
    bieWords = ''
    verb = ''
    for a in vList:
        #s = re.search('([Ss])-[Vv]', a[2])
        bie = re.search('([BIE]|[bie])-[Vv]', a[2])
        if bie is not None:
            bieWords = bieWords + a[1] + ' '
            bie_group = bie.group(0)
            bie_0 = re.split('-', bie_group)[0]
            bie_1 = re.split('-', bie_group)[1]
            if bie_0 == 'E' or bie_0 == 'e':
                vs.append([bie_1, bieWords])
                bieWords = ''
        else:
            just_v = re.search('[^Cc]-[Vv]', a[2])
            if just_v is not None:
                vs.append(['S-V', a[1]])
    for x in vs:
        verb = verb + x[1] + ' '
    return verb

def getArgs(argsList):
    args = []
    bieWords = ''
    for a in argsList: # [srl.wordid, srl.srlword, srl.srlresult[column]]
        s = re.search('([Ss])-[Aa][0-9]', a[2])
        bie = re.search('([BIE]|[bie])-[Aa][0-9]', a[2])
        if s is not None:
            s_group = s.group(0)
            s_arg = re.split('-', s_group)[1]
            args.append([s_arg, a[1]])
        if bie is not None:
            bieWords = bieWords + a[1] + ' '
            bie_group = bie.group(0)
            bie_0 = re.split('-', bie_group)[0]
            bie_1 = re.split('-', bie_group)[1]
            if bie_0 == 'E' or bie_0 == 'e':
                args.append([bie_1, bieWords])
                bieWords = ''
    return args

def getArgMs(argMsList):
    argMs = []
    for a in argMsList: # [srl.wordid, srl.srlword, srl.srlresult[column]]
        bie = re.search('([BIE]|[bie])-[Aa][Mm]-(ADV|adv|LOC|loc|MNR|mnr|TMP|tmp)', a[2])
        if bie is not None:
            argMs.append(a[1])
    return argMs

def checkTemplateWithDP(semObjectList):
    #Subj = ''
    #SubjDet = ''
    subjWordsList = []
    punct = ''
    xcompWordsList = []
    ccompWordsList = []
    dobjWordsList = []
    nmodWordsList = []
    V = ''
    Dobj = ''
    DobjDet = ''
    NmodAdvMod = ''
    NmodWords = ''
    Cc = ''
    ConjWordsList = []
    question=answer=''
    conjTemplate = 0
    for d in semObjectList:
        if int(d.tokenhead) == 0:
            rootIndex = int(d.tokenindex)
            V = d.depword
    for d in semObjectList:
        if int(d.tokenhead) == rootIndex:
            if d.deprel == 'conj':
                conjTemplate = 1
    if conjTemplate == 1:
        for d in semObjectList:
            dDeprel = d.deprel
            dHead = d.tokenhead
            try:
                if int(dHead) == rootIndex:
                    '''
                    if d.deprel == 'nsubj':
                        Subj = d.depword
                        SubjIndex = int(d.tokenindex)
                        for dsubj in semObjectList:
                            if int(dsubj.tokenhead) == SubjIndex:
                                if dsubj.deprel == 'det':
                                    SubjDet = dsubj.depword
                    '''
                    if d.deprel == 'nsubj' or d.deprel == 'nsubjpass':
                        #Subj = d.depword
                        SubjIndex = int(d.tokenindex)
                        SubjWords = ''
                        subjIndexList = [SubjIndex]
                        subjIndexListReady = checkChild(SubjIndex, semObjectList, subjIndexList)
                        for i in sorted(subjIndexListReady): #starts at 9
                            for o in semObjectList: #starts at 1
                                if int(o.tokenindex) == i:
                                    SubjWords = SubjWords + o.depword + ' '
                        subjWordsList.append(SubjWords)
                    if d.deprel == 'punct':
                        punct = d.depword
                    if d.deprel == 'advmod':
                        advmod_root = d.depword
                    if d.deprel == 'ccomp':
                        ccompIndex = int(d.tokenindex)
                        ccompWords = ''
                        ccompIndexList = [ccompIndex]
                        ccompIndexListReady = checkChild(ccompIndex, semObjectList, ccompIndexList)
                        for i in sorted(ccompIndexListReady): #starts at 9
                            for o in semObjectList: #starts at 1
                                if int(o.tokenindex) == i:
                                    ccompWords = ccompWords + o.depword + ' '
                        ccompWordsList.append(ccompWords)
                    if d.deprel == 'xcomp':
                        xcompIndex = int(d.tokenindex)
                        xcompWords = ''
                        xcompIndexList = [xcompIndex]
                        xcompIndexListReady = checkChild(xcompIndex, semObjectList, xcompIndexList)
                        for i in sorted(xcompIndexListReady): #starts at 9
                            for o in semObjectList: #starts at 1
                                if int(o.tokenindex) == i:
                                    xcompWords = xcompWords + o.depword + ' '
                        xcompWordsList.append(xcompWords)
                    '''
                    if d.deprel == 'dobj':
                        Dobj = d.depword
                        DobjIndex = int(d.tokenindex)
                        for ddobj in semObjectList:
                            if int(ddobj.tokenhead) == DobjIndex:
                                if ddobj.deprel == 'det':
                                    DobjDet = ddobj.depword
                    '''
                    if d.deprel == 'dobj':
                        dobjIndex = int(d.tokenindex)
                        dobjWords = ''
                        dobjIndexList = [dobjIndex]
                        dobjIndexListReady = checkChild(dobjIndex, semObjectList, dobjIndexList)
                        for i in sorted(dobjIndexListReady): #starts at 9
                            for o in semObjectList: #starts at 1
                                if int(o.tokenindex) == i:
                                    dobjWords = dobjWords + o.depword + ' '
                        dobjWordsList.append(dobjWords)
                    '''
                    if d.deprel == 'nmod':
                        NmodIndex = int(d.tokenindex)
                        for dnmod in semObjectList:
                            if int(dnmod.tokenhead) == NmodIndex or int(dnmod.tokenindex) == NmodIndex:
                                NmodWords = NmodWords + dnmod.depword + ' '
                            if int(dnmod.tokenhead) == rootIndex:
                                if dnmod.deprel == 'advmod':
                                    NmodAdvMod = dnmod.depword
                    '''
                    if d.deprel == 'nmod':
                        nmodIndex = int(d.tokenindex)
                        nmodWords = ''
                        nmodIndexList = [nmodIndex]
                        nmodIndexListReady = checkChild(nmodIndex, semObjectList, nmodIndexList)
                        for i in sorted(nmodIndexListReady):
                            for o in semObjectList:
                                if int(o.tokenindex) ==i:
                                    nmodWords = nmodWords + o.depword + ' '
                        nmodWordsList.append(nmodWords)
                
                    if d.deprel == 'cc':
                        Cc = d.depword
                    if d.deprel == 'conj':
                        ConjIndex = int(d.tokenindex)
                        ConjWords = ''
                        indexList = [ConjIndex]
                        indexListReady = checkChild(ConjIndex, semObjectList, indexList)
                        for i in sorted(indexListReady): #starts at 9
                            for o in semObjectList: #starts at 1
                                if int(o.tokenindex) == i:
                                    ConjWords = ConjWords + o.depword + ' '
                        ConjWordsList.append(ConjWords)
            except:
                foo = 'bar'
        
        Conjs = ''
        Subjs = ''
        Xcomps = ''
        Ccomps = ''
        Dobjs = ''
        Nmods = ''
        try:
            for c in ConjWordsList:
                Conjs = Conjs + c + ' '
            for s in subjWordsList:
                Subjs = Subjs + s + ' '
            for x in xcompWordsList:
                Xcomps = Xcomps + x + ' '
            for c in ccompWordsList:
                Ccomps = Ccomps + c + ' '
            for x in dobjWordsList:
                Dobjs = Dobjs + x + ' '
            for n in nmodWordsList:
                Nmods = Nmods + n + ' '
        except:
            foo='bar'
        
        if Xcomps != '' and Ccomps != '':
            question =  'What happens when ' + Subjs + V +  ' ' + Xcomps + Dobjs + Nmods+ '?'
            answer = Subjs + V +  ' ' + Xcomps + Dobjs + Nmods + ' ' + Cc + ' ' + Conjs
            followUpStrategy = '. Then something happens when ' + Subjs + V + ' ' + Xcomps + Dobjs + Nmods + '...'
        else:
            #question =  'What happens when ' + SubjDet + ' ' + Subj + ' ' + V + ' ' + DobjDet + ' ' + Dobj + ' ' + NmodAdvMod + ' '+ NmodWords + '?'
            question =  'What happens when ' + Subjs + V  + ' ' + Ccomps + Xcomps + Dobjs +Nmods + '?'
            #answer = SubjDet + ' ' + Subj + ' ' + V + ' ' + DobjDet + ' ' + Dobj + ' ' + NmodAdvMod + ' '+ NmodWords + ' ' + Cc + ' ' + Conjs
            answer = Subjs + V + ' ' + Ccomps + Xcomps + Dobjs + Nmods+ ' ' + Cc + ' ' + Conjs
            followUpStrategy = '. Then something happens when ' + Subjs + V + ' ' + Ccomps + Xcomps + Dobjs + Nmods + '...'
        return question, answer, 'DCNJ', 'DCNJ1', followUpStrategy

def checkChild(markedIndex, semObj, indexList):
    for o in semObj:
        if int(o.tokenhead) == markedIndex:
            indexList.append(int(o.tokenindex))
            checkChild(int(o.tokenindex), semObj, indexList) # recursion
    return indexList
        
def checkWordsInArgM(inputWord):
    firstWordtoDel = 0
    if len(inputWord) > 0:
        whi = re.search('[W|w]hile', inputWord[0])
        into = re.search('[I|i]nto', inputWord[0])
        to = re.search('[T|t]o', inputWord[0])
        aas = re.match('[A|a]s', inputWord[0])
        if (whi is not None) or (into is not None) or (to is not None) or (aas is not None):
            firstWordtoDel = 1
        #if inputWord[0] == 'While' or inputWord[0] == 'while':
        #    firstWordtoDel = 1
        #if inputWord[0] == 'Into' or inputWord[0] == 'into':
        #    firstWordtoDel = 1
        #if inputWord[0] == 'To' or inputWord[0] == 'to':
        #    firstWordtoDel = 1
    return firstWordtoDel

def getSubjectivePronoun(objectivePronoun):
    pronounSubjective = ''
    her = re.search('([Hh]er)', objectivePronoun)
    him = re.search('[Hh]im', objectivePronoun)
    if her is not None:
        pronounSubjective = 'she'
    elif him is not None:
        pronounSubjective = 'he'
    else:
        pronounSubjective = objectivePronoun
    return pronounSubjective

def getObjectivePronoun(subjectivePronoun):
    pronounObjective = ''
    she = re.match('([Ss]he)', subjectivePronoun)
    he = re.match('[Hh]e', subjectivePronoun)
    if she is not None:
        pronounObjective = 'her'
    elif he is not None:
        pronounObjective = 'him'
    else:
        pronounObjective = subjectivePronoun
    return pronounObjective
        
def checkTemplate(srlObjectList):
    columnLen = len((srlObjectList[0]).srlresult)
    column = 0
    qa = []
    for column in range(columnLen):
        question=answer=''
        V = ''
        vList = []
        argument = []
        qWord = ''
        aux = 'does'
        modifierAdverbials = []
        modifierLocatives = []
        modifierManner = []
        modifierTemporal = []
        modifierModals = []
        modifierOrdered = ''
        ArgM_ADV = ''
        ArgM_LOC = ''
        ArgM_MNR = ''
        ArgM_TMP = ''
        ArgM_MOD = ''
        for srl in srlObjectList:
            if srl.srlresult[column] != 'O': # only take the existing srl result
                checkVerb = re.search('-[Vv]', srl.srlresult[column])
                checkArgs = re.search('-[Aa][0-9]', srl.srlresult[column])
                checkArgMs_ADV = re.search('-[Aa][Dd][Vv]', srl.srlresult[column])
                checkArgMs_LOC = re.search('-[Ll][Oo][Cc]', srl.srlresult[column])
                checkArgMs_MNR = re.search('-[Mm][Nn][Rr]', srl.srlresult[column])
                checkArgMs_TMP = re.search('-[Tt][Mm][Pp]', srl.srlresult[column])
                checkArgMs_MOD = re.search('-[Mm][Oo][Dd]', srl.srlresult[column])                
                if checkVerb is not None:
                    vList.append([srl.wordid, srl.srlword, srl.srlresult[column]])
                    #V = srl.srlword
                if checkArgs is not None:
                    argument.append([srl.wordid, srl.srlword, srl.srlresult[column]])
                if checkArgMs_ADV is not None:
                    modifierAdverbials.append([srl.wordid, srl.srlword, srl.srlresult[column]])
                    #qWord = 'When'
                if checkArgMs_LOC is not None:
                    modifierLocatives.append([srl.wordid, srl.srlword, srl.srlresult[column]])
                    #qWord = 'Where'
                if checkArgMs_MNR is not None:
                    modifierManner.append([srl.wordid, srl.srlword, srl.srlresult[column]])
                    #qWord = 'How'
                if checkArgMs_TMP is not None:
                    modifierTemporal.append([srl.wordid, srl.srlword, srl.srlresult[column]])
                    #qWord = 'When'
                if checkArgMs_MOD is not None:
                    modifierModals.append([srl.wordid, srl.srlword, srl.srlresult[column]])
                    #qWord = 'When'
        argumentOrdered = []
        if len(vList) > 0:
            if len(vList) > 1:
                V = getV(vList)
            if len(vList) ==1:
                V = str(vList[0][1])
            if len(argument) > 1:
                argumentOrdered = getArgs(argument) # a list consists of argument number + argument words
                if len(modifierAdverbials) > 0:
                    modifierOrderedAdverbials = getArgMs(modifierAdverbials)
                    # some kind of syntax / discourse cues improvements (on the next few lines): #
                    ArgM_ADV_firstWord = '' #
                    ArgM_ADV_restOfWords = '' #
                    firstWordtoDel_ADV = checkWordsInArgM(modifierOrderedAdverbials) #
                    if firstWordtoDel_ADV == 1: #
                        ArgM_ADV_firstWord = modifierOrderedAdverbials[0] #
                        count = 0 #
                        for n in modifierOrderedAdverbials: #
                            if count >= 1: #
                                ArgM_ADV_restOfWords = ArgM_ADV_restOfWords + n + ' ' #
                            count = count + 1 #
                    for m in modifierOrderedAdverbials:
                        ArgM_ADV = ArgM_ADV + m + ' '
                if len(modifierLocatives) > 0:
                    modifierOrderedLocatives = getArgMs(modifierLocatives)
                    for m in modifierOrderedLocatives:
                        ArgM_LOC = ArgM_LOC + m + ' '
                if len(modifierManner) > 0:
                    modifierOrderedManner = getArgMs(modifierManner)
                    for m in modifierOrderedManner:
                        ArgM_MNR = ArgM_MNR + m + ' '
                if len(modifierTemporal) > 0:
                    modifierOrderedTemporal = getArgMs(modifierTemporal) # a list of the modifier words
                    ArgM_TMP_firstWord = ''
                    ArgM_TMP_restOfWords = ''
                    firstWordtoDel_TMP = checkWordsInArgM(modifierOrderedTemporal)
                    if firstWordtoDel_TMP == 1:
                        ArgM_TMP_firstWord = modifierOrderedTemporal[0]
                        count = 0
                        for n in modifierOrderedTemporal:
                            if count >= 1:
                                ArgM_TMP_restOfWords = ArgM_TMP_restOfWords + n + ' '
                            count = count + 1
                    for m in modifierOrderedTemporal:
                        ArgM_TMP = ArgM_TMP + m + ' '
                if len(modifierModals) > 0:
                    ArgM_MOD = modifierModals[0][1]
        try:
            A0 = ''
            A1 = ''
            A2 = ''
            A3 = ''
            i = 0
            question = ''
            answer = ''
            if len(argumentOrdered) > 1: # a list consists of a list; argument number + argument words
                # making sure that the argumentOrdered is ordered using the following loop: #
                for passnum in range(len(argumentOrdered)-1,0,-1): #
                    for i in range(passnum): #
                        if int(argumentOrdered[i][0][1]) > int(argumentOrdered[i+1][0][1]): #
                            temp = argumentOrdered[i] #
                            argumentOrdered[i] = argumentOrdered[i+1] #
                            argumentOrdered[i+1] = temp #
                countArg = 0
                doubleSameArgs = 0
                for ao in argumentOrdered:
                    if countArg > 0:
                        if ao[0] == prevArg:
                            doubleSameArgs = 1
                    prevArg = ao[0]
                    countArg = countArg + 1
                if doubleSameArgs == 0: # there should be no same arguments in a clause, there should be only 1 A0, 1 A1, 1 A2, etc.
                    nextArgument = ''
                    if len(argumentOrdered) > 2:
                        nextArgument = argumentOrdered[2][1]
                    tmp_helper = ''
                    tmp_helper_qword = 'Whom '
                    if argumentOrdered[0][0] != 'A0':
                        if argumentOrdered[1][0] != 'A1':
                            wit = re.search('[W|w]ith', argumentOrdered[1][1])
                            into = re.search('[I|i]nto', argumentOrdered[1][1])
                            to = re.search('\b[T|t]o', argumentOrdered[1][1])
                            if wit is not None:
                                tmp_helper = 'with'
                            if into is not None:
                                tmp_helper = 'into'
                                tmp_helper_qword = 'Where '
                            if to is not None:
                                tmp_helper = 'to'
                                tmp_helper_qword = 'What '
                    if ArgM_TMP != '':
                        qaCategory = 'MTMP'
                        #if ArgM_TMP_firstWord == '':
                        #    ArgM_TMP_firstWord
                        #ArgM_TMP_firstWord
                        objPronoun = getObjectivePronoun(argumentOrdered[0][1])
                        qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' do ' + ArgM_TMP +'?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] + ' ' + ArgM_TMP, qaCategory, 'MTMP1', '. Then something happens ' + ArgM_TMP + '...'])
                        qa.append(['Who ' + V + ' ' + argumentOrdered[1][1] + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] + ' ' + ArgM_TMP, qaCategory, 'MTMP2', '. Then something happens ' + ArgM_TMP + '...'])
                        qa.append([tmp_helper_qword + aux + ' ' + argumentOrdered[0][1] + ' ' + V + ' ' + tmp_helper + ' ' + ArgM_TMP + '?', argumentOrdered[0][1] + ' ' + ArgM_MOD + ' ' + V + ' ' + argumentOrdered[1][1] + ' ' + ArgM_TMP, qaCategory, 'MTMP3', '. Then something happens ' + ArgM_TMP + '...'])
                        qa.append(['What happens ' + ArgM_TMP + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'MTMP4', '. Then something happens ' + ArgM_TMP + '...'])
                        qa.append(['When ' + aux + ' ' + argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] + '?', ArgM_TMP, qaCategory, 'MTMP5', '. Then something happens ' + ArgM_TMP + '...'])
                    elif ArgM_MNR != '':
                        qaCategory = 'MMNR'
                        sbjPronoun = getSubjectivePronoun(argumentOrdered[0][1]) #make sure that subj Pronoun is used (based on err analysis, there's a case when the subj is 'her')
                        #qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' do to ' + argumentOrdered[1][1] + ' ' + ArgM_MNR +'?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'MMNR1'])
                        qa.append(['Who ' + ArgM_MOD +' '+ V + ' ' +  argumentOrdered[1][1] + ' ' + ArgM_MNR + '?', argumentOrdered[0][1] + ' ' + aux, qaCategory, 'MMNR2'])
                        #qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' ' + V + ' ' + ArgM_MNR + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'MMNR3'])
                        #qa.append(['What happens to ' + argumentOrdered[0][1] + ' ' + ArgM_MNR + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'MMNR4'])
                        with_MNR = re.match('[Ww]ith', ArgM_MNR)
                        if with_MNR is None:
                            qa.append(['How ' + aux + ' ' + sbjPronoun + ' ' + ArgM_MOD +' '+ V + ' ' + argumentOrdered[1][1] + '?', ArgM_MNR, qaCategory, 'MMNR5'])
                    elif ArgM_LOC != '':
                        qaCategory = 'MLOC'
                        objPronoun = getObjectivePronoun(argumentOrdered[0][1])
                        preposition_LOC = re.match('([Oo]n)|([Aa]t)|([Ii]n)', ArgM_LOC)
                        if preposition_LOC is None:
                            ArgM_LOC = 'in ' + ArgM_LOC
                        qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' do ' + ArgM_LOC +'?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'MLOC1', '. Then something happens ' + ArgM_LOC + '...'])
                        qa.append(['Who ' + V + ' ' + argumentOrdered[1][1] + ' ' + ArgM_LOC + '?', argumentOrdered[0][1] + ' ' + aux, qaCategory, 'MLOC2', '. Then something happens ' + ArgM_LOC + '...'])
                        qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' ' + V + ' ' + ArgM_LOC + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'MLOC3', '. Then something happens ' + ArgM_LOC + '...'])
                        qa.append(['What happens ' + ArgM_LOC + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'MLOC4', '. Then something happens ' + ArgM_LOC + '...'])
                        qa.append(['Where ' + aux + ' ' + argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] + '?', ArgM_LOC, qaCategory, 'MLOC5', '. Then something happens ' + ArgM_LOC + '...'])
                    elif ArgM_ADV != '':
                        qaCategory = 'MADV'
                        # some kind of syntax / discourse cues improvements (on the next few lines): #
                        if ArgM_ADV_firstWord == '': #
                            ArgM_ADV_firstWord = 'when' #
                            ArgM_ADV_restOfWords = ArgM_ADV #
                        if ArgM_ADV_restOfWords != '':
                            sheSubject = re.match('she', ArgM_ADV_restOfWords)
                            heSubject = re.match('she', ArgM_ADV_restOfWords)
                            itSubject = re.match('it', ArgM_ADV_restOfWords)
                            if (sheSubject is not None) or (heSubject is not None) or (itSubject is not None):
                                theSubject = ''
                            else:
                                theSubject = argumentOrdered[0][1] + ' is'
                            
                        objPronoun = getObjectivePronoun(argumentOrdered[0][1])
                        qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' do ' + ArgM_ADV_firstWord + ' ' + ArgM_ADV_restOfWords +'?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] +' '+ nextArgument, qaCategory, 'MADV1', '. Then something happens to ' + objPronoun +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '...'])
                        qa.append(['Who ' + V + ' ' + argumentOrdered[1][1] +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] +' '+ nextArgument, qaCategory, 'MADV2', '. Then something happens to ' + objPronoun +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '...'])
                        qa.append(['What is it that ' + argumentOrdered[0][1] + ' ' + V +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] +' '+ nextArgument, qaCategory, 'MADV3', '. Then something happens to ' + objPronoun +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '...'])
                        qa.append(['What happens to ' + objPronoun +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1] +' '+ nextArgument, qaCategory, 'MADV4', '. Then something happens to ' + objPronoun +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '...'])
                        qa.append(['When ' + aux + ' ' + argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1]  +' '+ nextArgument+ '?', ArgM_ADV_firstWord + ' ' + theSubject +' '+  ArgM_ADV_restOfWords, qaCategory, 'MADV5', '. Then something happens to ' + objPronoun +' '+ ArgM_ADV_firstWord +' '+ ArgM_ADV_restOfWords + '...'])
                    else:
                        qaCategory = 'ARGU'
                        sbjPronoun = getSubjectivePronoun(argumentOrdered[0][1])
                        objPronoun = getObjectivePronoun(argumentOrdered[1][1])
                        subjPassive = re.match('by ', argumentOrdered[0][1])
                        if subjPassive is None:
                            subjc = sbjPronoun
                        else:
                            subjc = argumentOrdered[0][1].replace("by ", "")
                        #qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' do?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'ARGU1'])
                        qa.append(['Who ' + ArgM_MOD + ' ' + V + ' ' + objPronoun +' '+ nextArgument +'?', subjc + ' ' + aux, qaCategory, 'ARGU2'])
                        #qa.append(['What ' + aux + ' ' + argumentOrdered[0][1] + ' ' + V + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'ARGU3'])
                        #qa.append(['What happens to ' + argumentOrdered[0][1] + '?', argumentOrdered[0][1] + ' ' + V + ' ' + argumentOrdered[1][1], qaCategory, 'ARGU4'])
                    
        except:
            foo = 'bar'
    return qa
    
def writeQA(sentenceQAList):
    #print 'sentenceQAList', sentenceQAList
    for aPair in sentenceQAList:
        qa = ET.SubElement(sentence, 'qa')
        qa.set('category', aPair[2])
        qa.set('template', aPair[3])
        question = ET.SubElement(qa, 'question')
        question.text = aPair[0]
        answer = ET.SubElement(qa, 'answer')
        answer.text = aPair[1]
        

###################################### Running the program ########################################


"""
Create the Semantic Representation
"""

sentenceList = [] # a list for the SemanticRepresentation objects

workPath = os.getcwd()
dependencyInputFile = workPath+'/senna/input.txt'
with open(dependencyInputFile) as f:
    dlines = f.readlines()
#Load model to parse PENN TreeBank
print 'Loading parsing model...'
# only for the first run (uncomment the following line):
# rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)
# when it is not the first run:
rrp = RerankingParser.from_unified_model_dir('/Users/evania/.local/share/bllipparser/WSJ-PTB3')
# Load model to parse PENN TreeBank - is finished
#Now try to parse the text:
print 'Parsing the dependency for the sentence(s)...'
len_dlines = len(dlines)
count_dlines = 1

for l in dlines:
    if l != '\n': # if not an empty line
        theDependencyResult = getDependency(l)
        theID = 0
        semList = []
        for token in theDependencyResult:
            #print token
            stringToken = str(token)
            sem = SemanticRepresentation()
            sem.wordid = theID
            sem.depword = getTokenWord(stringToken)
            sem.tokenindex = getTokenIndex(stringToken)
            sem.cpos = getTokenCpos(stringToken)
            sem.pos = getTokenPos(stringToken)
            sem.tokenhead = getTokenHead(stringToken)
            sem.deprel = getTokenDeprel(stringToken)
            semList.append(sem)
            theID = theID + 1
        sentenceList.append(semList)
        print 'Parsing', count_dlines, 'out of', len_dlines
        count_dlines = count_dlines + 1

print 'Getting the semantic role labels...'
sentenceListSRL = getSRL()


for aSentence in sentenceListSRL:
    for obj in aSentence:
        if obj[1] != '-':
            a = re.search("'[S|s]", obj[1]) # to handle apostrophes e.g. Alice's 
            b = re.search("\(", obj[1]) # to handle brackets e.g. (a word) 
            c = re.search("\)", obj[1])
            #d = re.search("-([A-Z]|[a-z])", srl.word) # to handle dashes e.g. Sam-the-cat
            if a is not None:
                obj[1] = obj[1].replace("'", "")
            if b is not None:
                obj[1] = '-LRB-'
            if c is not None:
                obj[1] = '-RRB-'


i = 0
if len(sentenceList) == len(sentenceListSRL):
    while i < len(sentenceList):
        for sr in sentenceList[i]:
            for fsro in sentenceListSRL[i]:
                #print 'fsro[0] == int(sr.tokenindex) and fsro[1] == sr.depword', fsro[0], sr.tokenindex, fsro[1], sr.depword
                if fsro[0] == int(sr.tokenindex) and fsro[1] == sr.depword:
                    if fsro[1] == '-LRB-':
                        sr.srlword = '('
                    elif fsro[1] == '-RRB-':
                        sr.srlword = ')'
                    else:
                        sr.srlword = sr.depword
                    sr.srlmainverb = fsro[2]
                    sr.srlresult = fsro[3]
        i = i + 1
'''
# To Test:
for sr in sentenceList:
    for semList in sr:
        print semList.tokenindex, semList.depword, semList.cpos, semList.pos, semList.tokenhead, semList.deprel, semList.srlword, semList.srlmainverb, semList.srlresult
'''
  
SRroot = ET.Element('sentences')
SRroot.set('version', '1.0')

    
try:
    print 'Creating Semantic Representations...'
    for aSentence in sentenceList:
        sentence = ET.SubElement(SRroot, 'sentence')
        writeSemanticRepresentation(aSentence)
except:
    print 'Failed to write the semantic representation XML'

xml = ET.tostring(SRroot,encoding='utf8', pretty_print=True)
fp = open("semantic_representation.xml", "w")
fp.write(xml)
fp.close()



"""
Generate the questions
"""

print 'Matching the question and answer templates...'

sentenceListForQA = readSemRep() # the returned value is a list of SRL Objects
sentenceQAList = []
QAroot = ET.Element('sentences')
QAroot.set('version', '1.0')

listOfAllGeneratedQA = []
for i in range(len(sentenceListForQA)):
    sentenceText = ''
    for word in sentenceListForQA[i]:
        if word.srlword != None:
            sentenceText = sentenceText + word.srlword + ' '
    sentenceQAList = checkTemplate(sentenceListForQA[i])
    checkDP = checkTemplateWithDP(sentenceListForQA[i])
    if checkDP is not None:
        sentenceQAList.append(checkDP)
    listOfAllGeneratedQA.append(sentenceQAList)
    try:
        sentence = ET.SubElement(QAroot, 'sentence')
        sentence.set('word', sentenceText)
        writeQA(sentenceQAList)
    except:
        print 'Failed to write the QA XML for:', sentenceText

xml = ET.tostring(QAroot,encoding='utf8', pretty_print=True)
fp = open("generated_qa.xml", "w")
fp.write(xml)
fp.close()
print 'Question and answer pairs are successfully generated.'



"""
Creating Follow-up Question Strategy for the Answers for QAMatcher Evaluation // 2017-07-20
(to exlude the following part just make everything in comments -- the main program above will still work)
"""

QAroot2 = ET.Element('sentences')
QAroot2.set('version', '1.0')

answer = ''
#MLOC_exists = 0
#MTMP_exists = 0
#MADV_exists = 0
#DCNJ_exists = 0
listOfFollowUpClues = []

for j in range(len(listOfAllGeneratedQA)):
    followUpClues = ''
    if j > 0:
        if len(listOfAllGeneratedQA[j]) > 0:
            for qa in listOfAllGeneratedQA[j]:
                if qa[2] == 'MLOC':
                    #DCNJ_exists = 1
                    followUpClues = qa[4]
                elif qa[2] == 'MTMP':
                    #MADV_exists = 1
                    followUpClues = qa[4]
                elif qa[2] == 'MADV':
                    #MTMP_exists = 1
                    followUpClues = qa[4]
                elif qa[2] == 'DCNJ':
                    #MLOC_exists = 1
                    followUpClues = qa[4]
                else:
                    followUpClues = ''
            #print "MLOC_exists", MLOC_exists, "MTMP_exists", MTMP_exists, "MADV_exists", MADV_exists, "DCNJ_exists", DCNJ_exists
        else:
            followUpClues = ''
    else:
        followUpClues = ''
    listOfFollowUpClues.append([j, followUpClues])


newListOfAllGeneratedQA = []
for a in range(len(listOfAllGeneratedQA)):
    for f in range(len(listOfFollowUpClues)):
        if f == a+1:
            newListOfGeneratedQA = []
            for qa in listOfAllGeneratedQA[a]:
                newListOfGeneratedQA.append([qa[0], qa[1] + listOfFollowUpClues[f][1], qa[2], qa[3]])
            newListOfAllGeneratedQA.append(newListOfGeneratedQA)
        
    if a == len(listOfFollowUpClues)-1:
        newListOfGeneratedQA = []
        for qa in listOfAllGeneratedQA[a]:
            #print "qa", qa
            newListOfGeneratedQA.append([qa[0], qa[1], qa[2], qa[3]])
        newListOfAllGeneratedQA.append(newListOfGeneratedQA)
            

for i in range(len(newListOfAllGeneratedQA)):
    sentenceText = ''
    for word in sentenceListForQA[i]:
        if word.srlword != None:
            sentenceText = sentenceText + word.srlword + ' '
    try:
        sentence = ET.SubElement(QAroot2, 'sentence')
        sentence.set('word', sentenceText)
        writeQA(newListOfAllGeneratedQA[i])
    except:
        print 'Failed to write the QA XML for:', sentenceText
        
xml2 = ET.tostring(QAroot2,encoding='utf8', pretty_print=True)
fp = open("generated_qa_with_follow_up_strategies.xml", "w")
fp.write(xml2)
fp.close()
print 'Follow-up question strategy is implemented.'
print ''
