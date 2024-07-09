import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_simple(self):
        children = [
            LeafNode('Gaba', None, 'p'),
            LeafNode('gool', { "href" : "https//www.google.com"}, 'a'),
            LeafNode('Yabba', None, 'p'),
            LeafNode('dabba', None, 'p'),
            LeafNode('doo', None, 'p'),
        ]
        node = ParentNode(children, 'body', None)
        target = '<body><p>Gaba</p><a href="https//www.google.com">gool</a><p>Yabba</p><p>dabba</p><p>doo</p></body>'
        self.assertEqual(node.to_html(), target)
    
    def test_nested(self):
        nested_leaves= [
            LeafNode('Gaba', None, 'p'),
            LeafNode('gool', { "href" : "https//www.google.com"}, 'a'),
        ]
        nested_prop = { 'class' : 'main-content'}
        nested_children = [
            ParentNode(nested_leaves, 'body', nested_prop),
            LeafNode('Yabba', None, 'p'),
            LeafNode('dabba', None, 'p'),
            LeafNode('doo', None, 'p'),
        ]
        prop = { 'id' : 'content-wrapper'}
        children = [
            LeafNode('Gaba', None, 'p'),
            ParentNode(nested_children, 'div', prop)
        ]

        node = ParentNode(children, 'html', None)
        target = '<html><p>Gaba</p><div id="content-wrapper"><body class="main-content"><p>Gaba</p><a href="https//www.google.com">gool</a></body><p>Yabba</p><p>dabba</p><p>doo</p></div></html>'
        self.assertEqual(node.to_html(), target)
    


