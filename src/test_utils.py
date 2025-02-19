import unittest
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_text_nodes, block_to_block_type, markdown_to_html_node
import utils
from textnode import TextNode
from parentnode import ParentNode
from leafnode import LeafNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("This is `code` text", "text")]
        result = utils.split_nodes_delimiter(nodes, "`", "code")
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

    ## This is not supported
    # def test_split_nodes_delimiter_italic_first(self):
    #     nodes = [ TextNode("Normal *italic* normal **bold** normal", "text") ]
    #     result = split_nodes_delimiter(nodes, "*", "italic")
    #     result2 = split_nodes_delimiter(result, "**", "bold")
    #     expected = [
    #         TextNode("Normal ", "text"),
    #         TextNode("italic", "italic"),
    #         TextNode(" normal ", "text"),
    #         TextNode("bold", "bold"),
    #         TextNode(" normal", "text")
    #     ]
    #     print(f'result2 = {result2}')
    #     self.assertEqual(result2, expected)

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


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes_basic(self):
        text = "This is **bold** and *italic* text with `code` and a [link](https://example.com) and an ![image](https://example.com/image.jpg)."
        result = utils.text_to_text_nodes(text)
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text with ", "text"),
            TextNode("code", "code"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(".", "text")
        ]
        self.assertEqual(result, expected)

    def test_empty_formatting(self):
        text = "This has empty ** ** formatting."
        result = utils.text_to_text_nodes(text)
        expected = [
            TextNode("This has empty ", "text"),
            TextNode(" formatting.", "text")
        ]
        self.assertEqual(result, expected)

    def test_url_in_link_text(self):
        text = "Here's a [link with a URL](https://example.com/page?param=value) in it."
        result = utils.text_to_text_nodes(text)
        expected = [
            TextNode("Here's a ", "text"),
            TextNode("link with a URL", "link", "https://example.com/page?param=value"),
            TextNode(" in it.", "text")
        ]
        self.assertEqual(result, expected)

    def test_multiple_empty_formatting(self):
        text = "This has **multiple** empty **** formatting ** ** elements."
        result = utils.text_to_text_nodes(text)
        expected = [
            TextNode("This has ", "text"),
            TextNode("multiple", "bold"),
            TextNode(" empty ", "text"),
            TextNode(" formatting ", "text"),
            TextNode(" elements.", "text")
        ]
        self.assertEqual(result, expected)

    def test_empty_formatting_at_start_and_end(self):
        text = "**  **This has empty formatting at start and end.*  *"
        result = utils.text_to_text_nodes(text)
        expected = [
            TextNode("This has empty formatting at start and end.", "text"),
        ]
        self.assertEqual(result, expected)

    def test_empty_code_and_link_formatting(self):
        text = "Empty `  ` code and [  ](https://example.com) link."
        result = utils.text_to_text_nodes(text)
        expected = [
            TextNode("Empty ", "text"),
            TextNode("  ", "code"),
            TextNode(" code and ", "text"),
            TextNode("", "link", "https://example.com"),
            TextNode(" link.", "text")
        ]
        self.assertEqual(result, expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        result = utils.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_basic(self):
        markdown = "### This is a H3"
        result = block_to_block_type(markdown)
        expected = 'H3'
        self.assertEqual(result, expected)

    def test_block_to_block_type_other_type(self):
        markdown = "This is a paragraph"
        result = block_to_block_type(markdown)
        expected = 'paragraph'
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        markdown = "1. First item"
        result = block_to_block_type(markdown)
        expected = 'ordered_list'
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list_2(self):
        markdown = "2. Second item"
        result = block_to_block_type(markdown)
        expected = 'ordered_list'
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list_multiple(self):
        markdown ="""1. item
2. item
3. item
"""
        result = block_to_block_type(markdown)
        expected ='ordered_list'
        self.assertEqual(result, expected)

    def test_block_to_block_type_unclosed_codeblock(self):
        markdown = "```print('Hello, World!')"
        with self.assertRaises(ValueError):
            block_to_block_type(markdown)

    def test_block_to_block_type_unordered_list(self):
        markdown = "- Bullet point"
        result = block_to_block_type(markdown)
        expected = 'unordered_list'
        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        markdown = "> This is a quote"
        result = block_to_block_type(markdown)
        expected = 'quote'
        self.assertEqual(result, expected)

    def test_block_to_block_type_code_block(self):
        markdown = "```print('Hello, World!')```"
        result = block_to_block_type(markdown)
        expected = 'code'
        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_levels(self):
        for i in range(1, 7):
            markdown = "#" * i + f" H{i} Heading"
            result = block_to_block_type(markdown)
            expected = f'H{i}'
            self.assertEqual(result, expected)

    def test_block_to_block_type_excessive_heading(self):
        markdown = "####### This should be H6"
        result = block_to_block_type(markdown)
        expected = 'H6'
        self.assertEqual(result, expected)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_code_basic(self):
        markdown ="""
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            [
                ParentNode([LeafNode("This is a heading", None)], "h1"),
                ParentNode([
                    LeafNode("This is a paragraph of text. It has some ", None),
                    LeafNode("bold", None, "b"),
                    LeafNode(" and ", None),
                    LeafNode("italic", None, "i"),
                    LeafNode(" words inside of it.", None)
                ], "p"),
                ParentNode([
                    ParentNode([LeafNode("This is the first list item in a list block", None)], "li"),
                    ParentNode([LeafNode("This is a list item", None)], "li"),
                    ParentNode([LeafNode("This is another list item", None)], "li")
                ], "ul")
            ]
        , 'div')
        self.assertEqual(result, expected)

    def test_markdown_to_html_code_inline_in_lists(self):
        markdown ="""
### This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list *item* in a list block
* This is a **list** item
* This is `another` list item
"""
        result = markdown_to_html_node(markdown)
        expected= ParentNode(
                [
                    ParentNode([LeafNode("This is a heading", None)], "h3"),
                    ParentNode([
                        LeafNode("This is a paragraph of text. It has some ", None),
                        LeafNode("bold", None, "b"),
                        LeafNode(" and ", None),
                        LeafNode("italic", None, "i"),
                        LeafNode(" words inside of it.", None)
                    ], "p"),
                    ParentNode([
                        ParentNode([
                            LeafNode("This is the first list ", None),
                            LeafNode("item", None, "i"),
                            LeafNode(" in a list block", None)
                            ], "li"),
                        ParentNode([
                            LeafNode("This is a ", None),
                            LeafNode("list", None, "b"),
                            LeafNode(" item", None)
                            ], "li"),
                        ParentNode([
                            LeafNode("This is ", None),
                            LeafNode("another", None, "code"),
                            LeafNode(" list item", None)
                            ], "li")
                    ], "ul")
                ]
            , 'div')
        self.assertEqual(result, expected)

    def test_markdown_to_html_node_ordered_list(self):
        markdown = """
1. test
2. **bold**
3. split **bold** test
4. split *italic* test
"""
        result = markdown_to_html_node(markdown)
        expected= ParentNode(
                [
                    ParentNode([
                        ParentNode([
                            LeafNode("test", None),
                            ], "li"),
                        ParentNode([
                            LeafNode("bold", None, "b"),
                            ], "li"),
                        ParentNode([
                            LeafNode("split ", None),
                            LeafNode("bold", None, "b"),
                            LeafNode(" test", None)
                            ], "li"),
                        ParentNode([
                            LeafNode("split ", None),
                            LeafNode("italic", None, "i"),
                            LeafNode(" test", None)
                            ], "li"),
                    ], "ol")
                ]
            , 'div')
        self.assertEqual(result, expected)

#     def test_md_to_html_node_breakdown_1(self):
#         markdown ="""
# **I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)"""
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode([
#             ParentNode([
#                 LeafNode("I like Tolkien", None, "b"),
#                 LeafNode(". Read my ", None),
#                 ParentNode([LeafNode("first post here", None)], "a"),
#                 LeafNode(" (sorry the link doesn't work yet)", None)
#             ], "p"),
#         ], 'div')
#         print(f'Result: {result}')
#         print(f'Expected: {expected}')
#         self.assertEqual(result, expected)

#     def test_markdown_to_html_node_final(self):
#         markdown = """
# # Tolkien Fan Club

# **I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

# > All that is gold does not glitter

# ## Reasons I like Tolkien

# * You can spend years studying the legendarium and still not understand its depths
# * It can be enjoyed by children and adults alike
# * Disney *didn't ruin it*
# * It created an entirely new genre of fantasy

# ## My favorite characters (in order)

# 1. Gandalf
# 2. Bilbo
# 3. Sam
# 4. Glorfindel
# 5. Galadriel
# 6. Elrond
# 7. Thorin
# 8. Sauron
# 9. Aragorn

# Here's what `elflang` looks like (the perfect coding language):

# ```
# func main(){
#     fmt.Println("Hello, World!")
# }
# ```
# """
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode(
#         [
#             ParentNode([LeafNode("Tolkien Fan Club", None)], "h1"),
#             ParentNode([
#                 LeafNode("I like Tolkien", None, "b"),
#                 LeafNode(". Read my ", None),
#                 ParentNode([LeafNode("first post here", None)], "a"),
#                 LeafNode(" (sorry the link doesn't work yet)", None)
#             ], "p"),
#             ParentNode([LeafNode("All that is gold does not glitter", None)], "blockquote"),
#             ParentNode([LeafNode("Reasons I like Tolkien", None)], "h2"),
#             ParentNode([
#                 ParentNode([LeafNode("You can spend years studying the legendarium and still not understand its depths", None)], "li"),
#                 ParentNode([LeafNode("It can be enjoyed by children and adults alike", None)], "li"),
#                 ParentNode([LeafNode("Disney ", None), LeafNode("didn't ruin it", None, "")], "li"),
#                 ParentNode([LeafNode("It created an entirely new genre of fantasy", None)], "li")
#             ], "ul"),
#             ParentNode([LeafNode("My favorite characters (in order)", None)], "h2"),
#             ParentNode([
#                 ParentNode([LeafNode("Gandalf", None)], "li"),
#                 ParentNode([LeafNode("Bilbo", None)], "li"),
#                 ParentNode([LeafNode("Sam", None)], "li"),
#                 ParentNode([LeafNode("Glorfindel", None)], "li"),
#                 ParentNode([LeafNode("Galadriel", None)], "li"),
#                 ParentNode([LeafNode("Elrond", None)], "li"),
#                 ParentNode([LeafNode("Thorin", None)], "li"),
#                 ParentNode([LeafNode("Sauron", None)], "li"),
#                 ParentNode([LeafNode("Aragorn", None)], "li")
#             ], "ol"),
#             ParentNode([
#                 LeafNode("Here's what ", None),
#                 LeafNode("elflang", None, "code"),
#                 LeafNode(" looks like (the perfect coding language):", None)
#             ], "p"),
#             ParentNode([LeafNode("func main(){\n    fmt.Println(\"Hello, World!\")\n}", None)], "pre")
#         ],
#         "div"
#         ) 
#         print(f'Expected: {expected}')
#         print(f'Result: {result}')
#         self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()


