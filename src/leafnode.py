from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, props, tag=None):
        super().__init__(self.tag, self.value, None, self.props)

    def to_html(self):
        html = ''
        if self.value == None:
            raise ValueError("All leaf nodes require a value")
        elif self.tag == None:
            return self.value
        else:
            split_tag = self.tag.split()
            html = f"{self.tag}{self.value}"

        return html