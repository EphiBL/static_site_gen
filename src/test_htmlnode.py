import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('<a>', 'content in the tag', None,)
        node2 = HTMLNode('<p>', 'content in the tag')
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        props = {
            "href" : "https://www.google.com",
            "target" : "_blank"
        }
        target =  ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(None, None, None, props)
        self.assertEqual(target, node.props_to_html())
    
    def test_props_to_html2(self):
        props = {
            "data" : "https://www.github.com/EphiBL/static_site_gen",
            "border" : "5"
        }
        target = ' data="https://www.github.com/EphiBL/static_site_gen" border="5"'

        node = HTMLNode(None, None, None, props)
        self.assertEqual(target, node.props_to_html())

    def test_eq(self):
        props_1 = {
            "target" : "_blank"
        }
        node = HTMLNode('<a>', 'yabbadabbadoo', None, props_1)
        node2 = HTMLNode('<a>', 'yabbadabbadoo', None, props_1)
        self.assertEqual(node, node2)




    
if __name__ == "__main__":
    unittest.main()