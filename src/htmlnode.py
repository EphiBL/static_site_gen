
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html has not been implemented")

    def props_to_html(self):
        raise NotImplementedError("props_to_html not been implemented")

    # def __repr__(self):
