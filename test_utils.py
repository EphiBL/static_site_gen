import unittest
from textnode import TextNode
from sitegen_utils import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is **bold** and *italic* text", "text")
        delimiter = "**"
        text_type = "bold"
        result = split_nodes_delimiter([node], delimiter, text_type)
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and *italic* text", "text"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("Normal *italic* normal **bold** normal", "text")
        delimiter = "*"
        text_type = "italic"
        result = split_nodes_delimiter([node], delimiter, text_type)
        expected = [
            TextNode("Normal ", "text"),
            TextNode("italic", "italic"),
            TextNode(" normal **bold** normal", "text"),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
