import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    """Unit tests for the TextNode class."""

    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

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


if __name__ == "__main__":
    unittest.main()
