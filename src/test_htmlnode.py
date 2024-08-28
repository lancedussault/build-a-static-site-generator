import unittest

from htmlnode import HTMLNode


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
       

if __name__ == "__main__":
    unittest.main()