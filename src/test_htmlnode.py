import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    """Unit tests for the HTMLNode class."""

    def test_repr(self) -> None:
        """Test that the __repr__ method returns a string representation of the HTMLNode."""
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "greeting"})
        expected_repr = (
            "HTMLNode(tag='div', value='Hello, World!', "
            "children=[], props={'class': 'greeting'})"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self) -> None:
        """Test that props_to_html converts props to HTML attributes correctly."""
        node = HTMLNode(
            tag="div", props={"href": "https://example.com", "target": "_blank"}
        )
        expected_html = 'href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_empty(self) -> None:
        """Test that props_to_html returns an empty string when props is empty."""
        node = HTMLNode(tag="div", props={})
        expected_html = ""
        self.assertEqual(node.props_to_html(), expected_html)

    def test_to_html_not_implemented(self) -> None:
        """Test that to_html raises NotImplementedError."""
        node = HTMLNode(tag="div")
        with self.assertRaises(NotImplementedError):
            node.to_html()
