import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_none_props(self):
       node = HTMLNode()
       self.assertEqual(node.props_to_html(), "")
        
    def test_few_props(self):
        node = HTMLNode("a", "Click Here", None, {"href": "https://www.google.com", 
    "target": "_blank"}, )
        self.assertEqual(node.props_to_html(), f' href="https://www.google.com" target="_blank"')
        
    def test_special_chars(self):
        node = HTMLNode("div", None, None, {"data-info": 'He said, "Hello!"', "class": "example"})
        expected = ' data-info="He said, "Hello!"" class="example"'
        self.assertEqual(node.props_to_html(), expected)

    def test_value_only(self):
        node = LeafNode(None, "I'm just a lil old value")
        self.assertEqual(node.to_html(), "I'm just a lil old value")

    def test_value_and_tag(self):
        node = LeafNode("p", "I'm a paragraph")
        self.assertEqual(node.to_html(), "<p>I'm a paragraph</p>")

    def test_value_tag_prop(self):
        node = LeafNode("a", "Click here", {"href": "https://www.fake-site.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.fake-site.com">Click here</a>')

    def test_multiple_props(self):
        node = LeafNode("a", "Open in new tab", {"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com" target="_blank">Open in new tab</a>')
       
if __name__ == "__main__":
    unittest.main()