import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_dif2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_dif3(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
