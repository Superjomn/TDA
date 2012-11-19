import  numpy as np 
class _CArray:
    def __init__(self):
        self.space = 500
        self.peradd = 300
        self.index = -1
        self.datas = np.array([], dtype=np.int32)
        self.datas = np.resize(self.datas, self.space)
        
    def size(self):
        return self.index + 1

    def setSize(self, n):
        assert n >= 0, "n < 0 : %d" % n
        self.index = n-1

    def needAddSpace(self):
        '''
        check space
        '''
        if self.size() == self.space:
            self.space += self.peradd
            print 'size - space: %d - %d'% (self.size(), self.space)
            self.datas = np.resize(self.datas, self.space)

    def add(self, data):
        '''
        just add to array
        '''
        #check space
        self.needAddSpace()
        self.index += 1
        self.datas[self.index] = data

    def toFile(self, filename='features.dic'):
        self.datas.tofile(filename)

    def show(self):
        print 'size - space : %d - %d' % (self.size(), self.space)
        print 'data: ', self.datas

class Dic(_CArray):
    def __init__(self):
        _CArray.__init__(self)
        self.accu = 0
        self.Accu = 1000

    def accumulate(self):
        '''
        add a accumulator to decide when to dump the array
        '''
        self.accu += 1
        if self.accu == self.Accu:
            self.dump()

    def find(self, word):
        data = hash(word)
        return np.where( self.datas == data )[0][0]
        

    def add(self, data):
        _CArray.add(self, data)
        self.accumulate()

    def dump(self):
        '''
        remove dumplicate
        '''
        uniques = np.unique(self.datas[:self.size()])
        size = np.size(uniques)
        print 'dump size: %s' % size
        self.setSize(size)
        self.datas[:size] = uniques

    def done(self):
        '''
        last dump and sort
        '''
        self.dump()
        self.datas[:self.size()].sort()

if __name__ == '__main__':
    '''
    A = _CArray()
    for i in range(100):
        A.add(i)
    '''
    from random import randint
    dic = Dic()
    for i in range(100):
        dic.add( randint(0, 100))
    dic.done()
    print 'size:', dic.size()
    print dic.datas
    
