from dic import Dic
import numpy as np

class _List(Dic):
    def __init__(self):
        Dic.__init__(self)
        self.space = 10
        self.peradd = 5
        self.datas = np.array([], dtype=np.uint16)
        self.datas = np.resize(self.datas, self.space)

    def done(self):
        self.dump()
        #resize space according to size
        self.datas = np.resize( self.datas, self.size() )
        self.space = np.size(self.datas)

class Datas:
    '''
    data contained in a node
    '''
    def __init__(self):
        self.dic = None
        self.list = _List()

    def setDic(self, dic):
        self.dic = dic

    def add(self, feature):
        self.list.add(feature)

    def addFeatures(self, features):
        for feature in features:
            i = self.dic.find(feature)
            print '>>> dic: %d', i
            self.list.add(i)
        self.list.done()

    def done(self):
        self.list.done()

    def getDatas(self):
        return self.list.datas

    def show(self):
        self.list.show()

if __name__ == '__main__':
    from dic import Dic
    dic = Dic()
    li = range(1, 20)
    for i in li:
        dic.add(i)
    dic.done()
    dic.show()
    datas = Datas()
    datas.setDic(dic)
    f = [1, 1, 5, 3]
    print 'f:', f
    datas.addFeatures(f)
    datas.show()
