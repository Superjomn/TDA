#ifndef TYPE_H_
#define TYPE_H_
typedef unsigned int Index;
typedef long Hash;
typedef unsigned short Count;
typedef float Imp;

struct Node{
	/*
	 * if child=0 means no child
	 * and it is a leaf node
	 * 'child' is always connect to latest child in Style Tree
	 * it is a back-link list
	 */
	Index child;
	/*
	 * if brother=0 then it means no brother
	 * 'brother' is always connect to latest brother
	 * and it is a back-link list
	 */
	Index brother;
	Hash hash;
	Count count;
	Imp imp;
};

#endif /* TYPE_H_ */
