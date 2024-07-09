from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag provided to ParentNode")
        if self.children == None:
            raise ValueError("No children on ParentNode")