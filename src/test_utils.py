import unittest
from sitegen_utils import split_nodes_delimiter
from textnode import TextNode


def test_text_node_to_html_node():
    pass


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("This is `code` text", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" text", "text")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_basic_bold(self):
        nodes = [TextNode("This is **bold** text", "text")]
        result = split_nodes_delimiter(nodes, "**", "bold")
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_basic_italic(self):
        nodes = [TextNode("This is *italic* text", "text")]
        result = split_nodes_delimiter(nodes, "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_change(self):
        nodes = [TextNode("This is text", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        self.assertEqual(result, nodes)

    def test_split_nodes_delimiter_nested(self):
        nodes = [
            TextNode("This is `code` text", "text"),
            TextNode("This **is bold** text", "text"),
            TextNode("This is plain text", "text"),
            TextNode("This is italic *text*", "text")
        ]
        result1 = split_nodes_delimiter(nodes, "`", "code")
        result2 = split_nodes_delimiter(result1, "**", "bold")
        result3 = split_nodes_delimiter(result2, "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" text", "text"),
            TextNode("This ", "text"),
            TextNode("is bold", "bold"),
            TextNode(" text", "text"),
            TextNode("This is plain text", "text"),
            TextNode("This is italic ", "text"),
            TextNode("text", "italic")
        ]
        self.assertEqual(result3, expected)

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("Normal *italic* normal **bold** normal", "text")
        result = split_nodes_delimiter([node], "*", "italic")
        expected = [
            TextNode("Normal ", "text"),
            TextNode("italic", "italic"),
            TextNode(" normal **bold** normal", "text"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_mixed(self):
        node = TextNode("This is **bold** and *italic* text", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and *italic* text", "text"),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()


