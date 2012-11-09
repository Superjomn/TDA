/*
 * Stack.h
 *
 *  Created on: Nov 9, 2012
 *      Author: chunwei
 */

#ifndef STACK_H_
#define STACK_H_
#include "Type.h"
#include <iostream>
#include <vector>
using namespace std;

template <class T>
class Stack {
private:
	vector<T> datas;
public:
	Stack();
	unsigned int size();
	bool pop(T &data);
	bool getTop(T &top);
	void push(const T &data);
	virtual ~Stack();
};

#endif /* STACK_H_ */
