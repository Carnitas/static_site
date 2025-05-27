import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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
        node2 = TextNode("This is a different text node", TextType.TEXT, url=None)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode(
            "This is a different text node", TextType.TEXT, url="https://example.com"
        )
        self.assertNotEqual(node, node2)

    def test_repr(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, url="https://example.com")
        expected_repr = (
            "TextNode"
            "('This is a text node', TextType.BOLD, "
            "'https://example.com')"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_text_to_html_text(self) -> None:
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_bold(self) -> None:
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")

    def test_text_to_html_italic(self) -> None:
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_text_to_html_code(self) -> None:
        node = TextNode("This is a code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block")

    def test_text_to_html_link(self) -> None:
        node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_text_to_html_empty_link(self) -> None:
        node = TextNode("This is an empty link", TextType.LINK, url="")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_to_html_images(self) -> None:
        node = TextNode(
            "This is an image", TextType.IMAGE, url="https://example.com/image.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is an image")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props.get("alt"), "This is an image")

    def test_text_to_html_empty_image(self) -> None:
        node = TextNode("This is an empty image", TextType.IMAGE, url="")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_to_html_unknown_type(self) -> None:
        node = TextNode("This is an unknown type", "unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
