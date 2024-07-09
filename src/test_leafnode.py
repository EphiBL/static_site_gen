import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_with_props(self):
        target = '<a href="https://www.google.com">Click me!</a>'
        props = { "href" : "https://www.google.com" }
        node = LeafNode("Click me!", props, "a")
        self.assertEqual(node.to_html(), target)

    def test_no_props(self):
        target = '<p>This is a paragraph of text.</p>'
        node = LeafNode("This is a paragraph of text.", None, "p")
        self.assertEqual(node.to_html(), target)

