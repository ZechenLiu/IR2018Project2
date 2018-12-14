import numpy
from numpy import *
from nltk.corpus import stopwords
def loadDataSet():
    # 词条切分后的文档集合，列表每一行代表一个文档
    postingList = []
    with open('positive_trainingSet', 'r', encoding='ISO-8859-1') as f:
        for line in f.readlines():
            postingList.append(line.strip().split())
    with open('negative_trainingSet', 'r', encoding='ISO-8859-1') as f:
        for line in f.readlines():
            postingList.append(line.strip().split())
    #去停用词
    list_stopWords = list(set(stopwords.words('english')))
    for l in postingList:
        length = len(l)
        x = 0
        while x < length:
            if l[x].lower() in list_stopWords:
                # l.remove(l[x])
                del l[x]
                x -= 1
                length -= 1
            x += 1
    for i in postingList:
        print(i)

    return postingList

# 统计所有文档中出现的词条列表
def createVocabList(dataSet):
    # 新建一个存放词条的集合
    vocabSet = set([])
    # 遍历文档集合中的每一篇文档
    for document in dataSet:
        # 将文档列表转为集合的形式，保证每个词条的唯一性
        # 然后与vocabSet取并集，向vocabSet中添加没有出现
        # 的新的词条
        vocabSet = vocabSet | set(document)
    # 再将集合转化为列表，便于接下来的处理
    return list(vocabSet)

def main():
    listOPosts = loadDataSet()
    # 统计所有文档中出现的词条，存入词条列表
    myVocabList = createVocabList(listOPosts)
    for i in myVocabList:
        print(i)
    numpy.save("myVocabList.npy", myVocabList)
    numpy.save("listOPosts.npy", listOPosts)
if __name__=='__main__':
    main()
