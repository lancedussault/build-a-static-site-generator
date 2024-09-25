import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ], None)

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nested_parent_nodes(self):
        inner_node = ParentNode("div", [LeafNode("span", "Inner text")], None)
        outer_node = ParentNode("section", [
            LeafNode("h1", "Title"),
            inner_node,
            LeafNode("p", "Paragraph")
        ], None)
        expected_html = "<section><h1>Title</h1><div><span>Inner text</span></div><p>Paragraph</p></section>"
        self.assertEqual(outer_node.to_html(), expected_html)

    def test_parent_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [], None).to_html()
        self.assertTrue("What makes a Parent node? Children!" in str(context.exception))

    def test_parent_no_tag(self):
        node = ParentNode(None, [
                LeafNode("h1", "Title", None),
                LeafNode("p", "Paragraph", None)
            ], None)
        
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("Parent nodes must have a tag!" in str(context.exception))
       
if __name__ == "__main__":
    unittest.main()