import unittest

from textnode import  (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Some text", "bold")
        node2 = TextNode("Some other text that's different", "bold")
        message = "Yo! These two strings are not equal!!!"
        self.assertNotEqual(node, node2, message)

    def test_url(self):
        node = TextNode("Some text", "bold", "https://www.boot.dev")
        node2 = TextNode("Some text", "bold", "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("Some text", "bold", "https://www.boot.dev")
        self.assertEqual("TextNode(Some text, bold, https://www.boot.dev)", repr(node))



class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("Some text", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Some text")

    def test_img(self):
        node = TextNode("Kitty cat", text_type_image, "https://kittycat.edu")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://kittycat.edu", "alt": "Kitty cat"})

    def test_link(self):
        node = TextNode("Click here", text_type_link, "https://yourmom.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://yourmom.com"})


if __name__ == "__main__":
    unittest.main()
