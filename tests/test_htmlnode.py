import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self) -> None:
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self) -> None:
        node = LeafNode("div", "This is a div.")
        self.assertEqual(node.to_html(), "<div>This is a div.</div>")

    def test_leaf_to_html_bold(self) -> None:
        node = LeafNode("strong", "Bold text")
        self.assertEqual(node.to_html(), "<strong>Bold text</strong>")

    def test_leaf_no_value(self) -> None:
        node = LeafNode("span", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_tag(self) -> None:
        node = LeafNode("", "No tag")
        self.assertEqual(node.to_html(), "No tag")

    def test_parent_no_children(self) -> None:
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_tag(self) -> None:
        node = ParentNode("", [LeafNode("span", "No tag parent")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self) -> None:
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self) -> None:
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
