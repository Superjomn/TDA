# distutils: language = c++
# distutils: sources = "StyleTree.cpp"

cdef extern from "StyleTree.h" namespace "styletree":
    cdef cppclass StyleTree:
        StyleTree() except +
        bint registerChildTag(long, unsigned int)
        void showNodeList()

cdef class pyStuleTree:
    '''
    python wrapper class
    '''
    cdef StyleTree *thisptr
    def __cinit__(self):
        self.thisptr = new StyleTree()
    def __dealloc__(self):
        del self.thisptr
    def registerChildTag(self, _hash, index):
        return self.thisptr.registerChildTag(_hash, index)
    def showNodeList(self):
        self.thisptr.showNodeList()
        
        
