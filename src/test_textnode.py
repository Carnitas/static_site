import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    """Unit tests for the TextNode class."""

    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

    def test_eq_not_implemented(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertNotEqual(node, "This is a string, not a TextNode")

    def test_not_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a different text node", TextType.NORMAL, url=None)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode(
            "This is a different text node", TextType.NORMAL, url="https://example.com"
        )
        self.assertNotEqual(node, node2)
    
    def test_repr(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url="https://example.com")
        expected_repr = "TextNode(text='This is a text node', text_type=<TextType.BOLD: 'bold'>, url='https://example.com')"
        self.assertEqual(repr(node), expected_repr)
