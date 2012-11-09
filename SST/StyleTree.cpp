/*
 * StyleTree.cpp
 *
 *  Created on: Nov 9, 2012
 *      Author: chunwei
 */

#include "StyleTree.h"

StyleTree::StyleTree() {
	// TODO Auto-generated constructor stub
}

bool StyleTree::initAddChild()
{
	if (stack.size==0)
	{
		return true;
	}
	return false;
}

/* specify the pos of child tag in the construction 
 * of a Style Tree using a stack.
 * if childtag is the FIRST child then gettop of stack
 * as it's parent and init it's brother as 0 and push
 * it to the stack
 * if childtag is MID then pop the stack as it's brother, 
 * gettop of stack as it's parent, and push itself to stack
 * if childtag is END, then pop the stack as 
 * it's brother, pop stack as it's parent 
 */
Index StyleTree::addNewChildTag(Hash hashtag, ChildTagPos pos)
{
	Index tem;
	Index cur;
	bool res;
	Node node;
	//set hash
	node.hash = hashtag;
	//init child
	node.child = 0;		// always connect to latest child
	//set brother
	node.brother = 0;	// 0 is body, means no brother

	switch(pos)
	{
		case FIRST:
		{
			//add to nodelist
			nodelist.push_back(node);
			cur = nodelist.size() - 1;
			//connect to parent
			//get parent
			res = stack.getTop(tem);
			if (!res) throw runtime_error("getTop: stack is empty");
			else{
				const Node *father = &nodelist.at(tem);
				father->child = cur;
			}
			//push itself to stack
			stack.push(cur);
		}
		case MID:
		{
			//add to nodelist
			nodelist.push_back(node);
			cur = nodelist.size() - 1;
			//get brother
			res = stack.pop(tem);
			if (!res) throw runtime_error("can't get brother, pop: stack is empty!");
			node.brother = 

		}
		// set brother
		res = stack.pop(tem);
		if (!res) throw runtime_error("Pop: stack is empty");
		else node.brother = tem;	
		res = stack.getTop(tem);
		// connect to parent's child
		if (!res) throw runtime_error("Pop: stack is empty");
		else
		{
			const Node *father = &nodelist.at(tem);
			//father->child = 
		}
		
		Node node;
	}
}

StyleTree::~StyleTree() {
	// TODO Auto-generated destructor stub
}

