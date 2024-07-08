
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False

    def to_html(self):
        raise NotImplementedError("to_html has not been implemented")

    def props_to_html(self):
        html = ''
        for k, v in self.props.items():
            stripped_k = k.strip('"')
            html = html + f' {stripped_k}="{v}"'
        return html

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
