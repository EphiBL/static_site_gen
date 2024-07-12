import unittest
from sitegen_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links
# import sitegen_utils
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
        nodes = [ TextNode("Normal *italic* normal **bold** normal", "text") ]
        result = split_nodes_delimiter(nodes, "**", "bold")
        result2 = split_nodes_delimiter(result, "*", "italic")
        expected = [
            TextNode("Normal ", "text"),
            TextNode("italic", "italic"),
            TextNode(" normal ", "text"),
            TextNode("bold", "bold"),
            TextNode(" normal", "text")
        ]
        self.assertEqual(result2, expected)

    def test_split_nodes_delimiter_mixed(self):
        nodes = [TextNode("This is **bold** and *italic* text", "text")]
        result = split_nodes_delimiter(nodes, "**", "bold")
        result2 = split_nodes_delimiter(result, "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text")
        ]
        self.assertEqual(result2, expected)

    def test_split_nodes_delimiter_double(self):
        nodes = [TextNode("This is **bold** and **bold** text", "text")]
        result = split_nodes_delimiter(nodes, "**", "bold")
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text")
        ]
        self.assertEqual(result, expected)

class TestLinkImageExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is an ![image](https://example.com/image.jpg) in text."
        result = extract_markdown_images(text)
        expected = [("image", "https://example.com/image.jpg")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "This is a [link](https://example.com) in text."
        result = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_and_images(self):
        text = "This is a [link](https://example.com) and an ![image](https://example.com/image.jpg) in the same text."
        link_result = extract_markdown_links(text)
        image_result = extract_markdown_images(text)
        expected_links = [("link", "https://example.com")]
        expected_images = [("image", "https://example.com/image.jpg")]
        self.assertEqual(link_result, expected_links)
        self.assertEqual(image_result, expected_images)
        
        # Additional test to ensure links are not picked up as images and vice versa
        self.assertNotIn(("image", "https://example.com/image.jpg"), link_result)
        self.assertNotIn(("link", "https://example.com"), image_result)

    def test_extract_markdown_images_before_links(self):
        text = "This is an ![image](https://example.com/image.jpg) and a [link](https://example.com) in the same text."
        image_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        expected_images = [("image", "https://example.com/image.jpg")]
        expected_links = [("link", "https://example.com")]
        self.assertEqual(image_result, expected_images)
        self.assertEqual(link_result, expected_links)
        
        # Additional test to ensure images are not picked up as links and vice versa
        self.assertNotIn(("link", "https://example.com"), image_result)
        self.assertNotIn(("image", "https://example.com/image.jpg"), link_result)

class TestSplitNodesLinksImages(unittest.TestCase):
    basic_img_node = [TextNode("This is an ![image](https://example.com/image.jpg) in text.", "text")]
    basic_link_node = [TextNode("This is a [link](https://example.com) in text.", "text")]
    double_img_node = [TextNode("This is an ![image](https://example.com/image.jpg) in text, with another ![image2](https://google.com/image.jpg) as well", "text")]
    double_link_node = [TextNode("This is a [link](https://example.com) in text, with another [link2](https://google.com) as well", "text")]

    def test_split_nodes_images(self):
        result = split_nodes_images(self.basic_img_node)
        expected = [
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" in text.", "text")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_links(self):
        result = split_nodes_links(self.basic_link_node)
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" in text.", "text")
        ]
        self.assertEqual(result, expected)

    def test_concurrent_split_link_image(self):
        nodes = self.basic_link_node + self.basic_img_node
        result1 = split_nodes_links(nodes)
        result2 = split_nodes_images(result1)
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" in text.", "text"),
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" in text.", "text"),
        ]
        self.assertEqual(result2, expected)

    def test_concurrent_split_link_image_reversed(self):
        nodes = self.basic_link_node + self.basic_img_node
        result1 = split_nodes_images(nodes)
        result2 = split_nodes_links(result1)
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" in text.", "text"),
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" in text.", "text"),
        ]
        self.assertEqual(result2, expected)
    
    def test_concurrent_split_link_images_alt_order(self):
        nodes = self.basic_img_node + self.basic_link_node
        result1 = split_nodes_images(nodes)
        result2 = split_nodes_links(result1)
        expected = [
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" in text.", "text"),
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" in text.", "text"),
        ]
        self.assertEqual(result2, expected)

    def test_concurrent_split_link_images_alt_order_reversed(self):
        nodes = self.basic_img_node + self.basic_link_node
        result1 = split_nodes_links(nodes)
        result2 = split_nodes_images(result1)
        expected = [
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" in text.", "text"),
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" in text.", "text"),
        ]
        self.assertEqual(result2, expected)

    def test_split_nodes_images_doubled(self):
        result = split_nodes_images(self.double_img_node)
        expected = [
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" in text, with another ", "text"),
            TextNode("image2", "image", "https://google.com/image.jpg"),
            TextNode(" as well", "text")
        ]

    def test_split_nodes_links_doubled(self):
        result = split_nodes_links(self.double_link_node)
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" in text, with another ", "text"),
            TextNode("link2", "link", "https://google.com"),
            TextNode(" as well", "text")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_links_images_doubled(self):
        nodes = self.double_link_node + self.double_img_node
        result1 = split_nodes_links(nodes)
        result2 = split_nodes_images(result1)
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" in text, with another ", "text"),
            TextNode("link2", "link", "https://google.com"),
            TextNode(" as well", "text"),
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" in text, with another ", "text"),
            TextNode("image2", "image", "https://google.com/image.jpg"),
            TextNode(" as well", "text")
        ]
        self.assertEqual(result2, expected)


if __name__ == "__main__":
    unittest.main()


