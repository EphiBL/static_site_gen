from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag provided to ParentNode")
        elif self.children == None:
            raise ValueError("No children on ParentNode")
        else:
            children_html = ''
            if self.props == None:
                parent_props = ""
            else:
                parent_props = super().props_to_html()
            parent_open = f"<{self.tag}{parent_props}>"
            parent_close = f"</{self.tag}>"

            for node in self.children:
                children_html = children_html + node.to_html()

            return f"{parent_open}{children_html}{parent_close}"

                




