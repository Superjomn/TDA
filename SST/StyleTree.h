/*
 * StyleTree.h
 *
 *  Created on: Nov 9, 2012
 *      Author: chunwei
 */

#ifndef STYLETREE_H_
#define STYLETREE_H_
#include "Type.h"
#include <iostream>
#include <vector>
using namespace std;

/* specify the pos of child tag in the construction 
 * of a Style Tree using a stack.
 * if childtag is the FIRST child then gettop of stack
 * as it's parent and init it's brother as -1 and push
 * it to the stack
 * if childtag is MID then pop the stack as it's brother, 
 * gettop of stack as it's parent, and push itself to stack
 * if childtag is END, then pop the stack as 
 * it's brother, pop stack as it's parent 
 */
typedef enum ChildTagPos{
	FIRST, MID, END
}ChildTagPos; 

class StyleTree {
private:
	vector<Node> nodelist;	
	Stack<Index> stack;
public:
	StyleTree();
    bool registerChildTag(Hash hashtag, Index father);
    Index searchChild(Hash childhash, Index father, Index &lastBrother);
    Index addChildTag(Hash hashdata, Index father, Index lastBrother);
	virtual ~StyleTree();
};

#endif /* STYLETREE_H_ */
