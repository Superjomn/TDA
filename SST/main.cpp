#include <iostream>
#include "StyleTree.h"
using namespace std;
using namespace styletree;

int main()
{
    StyleTree* styletree = new StyleTree();
    styletree->registerChildTag(23, 0);
    cout<<"hello world"<<endl;
    return 0;
}
