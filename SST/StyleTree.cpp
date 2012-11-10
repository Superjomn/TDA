/*
 * StyleTree.cpp
 *
 *  Created on: Nov 9, 2012
 *      Author: chunwei
 */

#include "StyleTree.h"

/*#################################################
 * structure of StyleTree:
 * a static linked list:
 * <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
 * array:
 * hash     child   brother  imp  count
 * ---------------------------------------
 *  hash = hash(tagname)
 *  child always link to the latest added child 
 *  brother always link to the last brother found
 *  imp is finally calculated value using count
 *#################################################*/

StyleTree::StyleTree() {
	// TODO Auto-generated constructor stub
}

bool registerChildTag(Hash hashtag, Index father)
/*
 * given father node, if find the matching child, then add it's count
 * if cannot find the matching one, then create a new child.
 */
{
    Index lastBrother;
    Index child;
    if ( child = searchChild( hashtag, father, lastBrother) )
    {
        nodelist[child].count ++;
    }
    else
    {
        addChildTag(hashtag, father, lastBrother);
    }
}

Index searchChild(Hash childhash, Index father, Index &lastBrother)
{
    Index child;
    Index brother;
    Index lastBrother;
    // first child
    child = nodelist[father].child;
    if (child ==0) // means no child yet
    {
        return false;
    }// end if
    else
    {
        if (nodelist[child].hash == childhash)
        { /* the mach one*/ }
        else
        {
            brother = nodelist[child].brother;
        }// end else
        while(brother != 0)
        { // search the nodelist using the first child's brother
            if (nodelist[brother].hash == childhash)
            {
                child = brother;
            }// end if
            lastBrother = brother;
            brother = nodelist[brother].brother; // to get the last brother
        }// end while
    }// end else
    return child;
}

Index addChildTag(Hash hashdata, Index father, Index lastBrother)
{
    // init new node
    Node node;
    node.hash = hashdata;
    node.child = 0;
    node.brother = lastBrother;
    node.count = 1;
    node.imp = 0;
    nodelist.push_back(node);
    // set father node
    // children is a reversed linked list
    nodelist[father].child = nodelist.size() - 1;
}


StyleTree::~StyleTree() {
	// TODO Auto-generated destructor stub
}

