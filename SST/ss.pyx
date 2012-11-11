# distutils: language = c++
# distutils: sources = "StyleTree.cpp"

ctypedef unsigned int Index
ctypedef long Hash

cdef extern from "StyleTree.h":
    cdef cppclass StyleTree:
        bint registerChildTag(Hash, Index)
        Index searchChild(Hash, Index, Index &)
        Index addChildTag(Hash, Index, Index)

        
        
