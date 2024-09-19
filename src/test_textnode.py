import unittest

from textnode import TextNode


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



if __name__ == "__main__":
    unittest.main()
