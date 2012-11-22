import  numpy as np 

def trim(text):
    if type(text) == type(''):
        return text.lstrip().rstrip()
    return text

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
            #print 'size - space: %d - %d'% (self.size(), self.space)
            self.datas = np.resize(self.datas, self.space)

    def add(self, data):
        '''
        just add to array
        '''
        #check space
        data = hash(data)
        self.needAddSpace()
        self.index += 1
        self.datas[self.index] = data

    def tofile(self, filename='features.dic'):
        self.datas.tofile(filename)
        #save some meta data
        data =  "%d#%d" % (self.index, self.space)
        #print 'dic save:', data
        open('sizeof_' + filename, 'w').write( data )

    def fromfile(self, filename='features.dic'):
        self.datas = np.fromfile(filename, dtype=np.int32)
        res = open('sizeof_' + filename).read()
        (self.index, self.space) = [int(i) for i in res.split('#')]

    def show(self):
        print 'size - space : %d - %d' % (self.size(), self.space)
        print 'data: ', self.datas

    def __str__(self):
        return str(self.datas)

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
        #print '.. finding %s' % word
        data = hash(trim(word))
        #print '.. data hash: %s' % data
        return np.where( self.datas == data )[0][0]
        

    def add(self, data):
        data = trim(data)
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
    
