import numpy as np
from math import *
import openpyxl
from nltk.corpus import stopwords


def TrainMultinomialNB():
    myVocabList = np.load('myVocabList.npy')
    myVocabList = list(myVocabList)
    listOPosts = np.load('listOPosts.npy')
    # testtY = [0] * len(myVocabList)
    # testtN = [0] * len(myVocabList)
    positiveList = []
    for i in  range(int(len(listOPosts)/2)):
        for t in listOPosts[i]:
            positiveList.append(t)
    # for t in myVocabList:
    #     for i in positiveList:
    #         if t == i:
    #             testtY[myVocabList.index(t)] += 1
    # np.save("testtY.npy", testtY)
    #
    negativeList = []
    for i in range(int(len(listOPosts)/2),int(len(listOPosts))):
        for t in listOPosts[i]:
            negativeList.append(t)
    # for t in myVocabList:
    #     for i in negativeList:
    #         if t==i:
    #             testtN[myVocabList.index(t)] += 1
    # np.save("testtN.npy", testtN)
    testtY = np.load('testtY.npy')
    testtN = np.load('testtN.npy')
    condprob = np.zeros([len(myVocabList), 2])
    for t in myVocabList:
        condprob[myVocabList.index(t)][0] = float(log((testtY[myVocabList.index(t)]+4.6)/(len(positiveList)+len(myVocabList)*4.6)))
        condprob[myVocabList.index(t)][1] = float(log((testtN[myVocabList.index(t)]+4.6)/(len(negativeList)+len(myVocabList)*4.6)))

    print(condprob)
    return myVocabList,condprob
def ApplyMultinomialNB(myVocabList,condprob):
    testSet = openpyxl.load_workbook('testSet-1000.xlsx')
    sheet = testSet.get_sheet_by_name("Sheet1")
    #去停用词
    list_stopWords = list(set(stopwords.words('english')))
    testEntrys = []
    for i in sheet["B"]:
        testEntrys.append(str(i.value).split())
    testEntrys.pop(0)
    for l in testEntrys:
        length = len(l)
        x = 0
        while x < length:
            if l[x].lower() in list_stopWords:
                # l.remove(l[x])
                del l[x]
                x -= 1
                length -= 1
            x += 1
    #W <- ExtractTokensFromDoc(V,d)
    for l in  testEntrys:
        length = len(l)
        x = 0
        while x < length:
            if l[x].lower() not in [item.lower() for item in myVocabList]:
                # l.remove(l[x])
                del l[x]
                x -= 1
                length -= 1
            x += 1
    #测试集中由人工标注的每篇文档的类标签
    testclassVec = []
    for i in sheet["C"]:
        if str(i.value) == 'Y':
            testclassVec.append(0)
        if str(i.value) == 'N':
            testclassVec.append(1)

    count = 0
    myVocabList = [item.lower() for item in myVocabList]
    for i in range(len(testEntrys)):
        score1 = float(log(1/2))
        score2 = float(log(1/2))
        #
        if len(testEntrys[i]) == 1 or len(testEntrys[i]) == 2:
            a = 1
        else:
        #
            for t in testEntrys[i]:
                if '(' not in t or ')' not in t or ',' not in t or ':' not in t or '-' not in i or '?' not in t or '.' not in t or '“' not in t or '”' not in t or '–' not in t or '0' not in t or '1' not in t or '2' not in t or '3' not in t or '4' not in t or '5' not in t or '6' not in t or '7' not in t or '8' not in t or '9' not in t:
                    score1 += condprob[myVocabList.index(t.lower())][0]
                    score2 += condprob[myVocabList.index(t.lower())][1]
            if score1 <= score2:
                a = 1
            else:
                a = 0
        if a == testclassVec[i]:
            count += 1
        else:
            print(i)
            print(testEntrys[i])
    print(count)
    print(float(count/len(testEntrys)))



myVocabList,condprob =  TrainMultinomialNB()
ApplyMultinomialNB(myVocabList,condprob)

