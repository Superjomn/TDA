/*
 * Stack.cpp
 *
 *  Created on: Nov 9, 2012
 *      Author: chunwei
 */

#include "Stack.h"

template <class T> Stack::Stack() {
	// TODO Auto-generated constructor stub
	cout<<">> Stack construct"<<endl;
}

template <class T> unsigned int Stack::size()
{
	return datas.size();
}

template <class T> bool Stack::pop(T &data)
{
	if (datas.size() > 0) 
	{
		data = datas.pop_back();
		return true;
	}
	else return false;
}

template <class T> bool Stack::getTop(T &top) {
	Index size = datas.size();
	if (size > 0) 
	{
		top = datas.back(); 
		return true;
	}
	else return false;
}

template <class T> void Stack::push(const T &data)
{
	datas.push_back(data);
}

template <class T> Stack::~Stack() {
	// TODO Auto-generated destructor stub
}

