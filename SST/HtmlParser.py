class HtmlParser:
    def parse(self):
        self.pq = pq(html)
        # get body
        body = self.pq('body')
        stack.push (body, 0)
        # interation
        fatherid = 0
        while not stack.empty():
            node = stack.pop()
            tag = gettag(node)
            if tag:
                fatherid = styletree.registerChildTag(tag)
            else:
                styletree.registerNode(node)
            children = node.children()
            for child in children:
                tag = gettag(child)
                if tag:
                    styletree.registerChildTag(tag, fatherid)
                    stack.push(child, fatherid)
                else:
                    styletree.registerNode(child, fatherid)



