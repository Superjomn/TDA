from dic import Dic
import numpy as np

class _List(Dic):
    '''
    a container of list data
    '''
    def __init__(self):
        Dic.__init__(self)
        self.space = 10
        self.peradd = 5
        self.datas = np.array([], dtype=np.uint16)
        self.datas = np.resize(self.datas, self.space)

    def close(self):
        self.done()
        self.datas = np.resize(self.datas, self.size())


class Datas:
    '''
    data contained in a node
    single node's dic
    '''
    def __init__(self, dic):
        self.dic = dic
        assert self.dic.size() != 0 , "dicsize = 0"
        self.list = _List()

    def add(self, feature):
        self.list.add(feature)

    def addFeatures(self, features):
        for feature in features:
            try:
                print 'addFeatures: find %s' % feature 
                i = self.dic.find(feature)
                print '>>> dic: %d' % i
                print 'list add' 
                self.list.add(i)
            except:
                print "!!!! wrong finding !!!!!"
        self.done()
        print 'list: ', self.list.datas

    def hasData(self):
        return bool(self.list.datas)

    def done(self):
        self.list.close()

    def size(self):
        return self.list.size()

    def getDatas(self):
        return self.list.datas

    def show(self):
        self.list.show()

    def __getitem__(self, i):
        return self.list.datas[i]

    def __str__(self):
        return str(self.list)

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
