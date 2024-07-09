from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, props, tag=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes require a value")
        elif self.tag == None:
            return self.value
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            props = super().props_to_html()
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode: {self.tag}, {self.value}, {self.children}, {self.props}"
    