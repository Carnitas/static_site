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


class TestLeafNode(unittest.TestCase):
    """Unit tests for the LeafNode class."""

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


class TestParentNode(unittest.TestCase):
    """Unit tests for the ParentNode class."""

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

    def test_leaf_img_with_src(self) -> None:
        node = LeafNode("img", "", props={"src": "image.png", "alt": "desc"})
        # The props_to_html will include both src and alt, so src will appear twice
        # The implementation adds src manually and then again in props_to_html
        # So the output will be: <img src="image.png" src="image.png" alt="desc">
        expected_html = '<img src="image.png" src="image.png" alt="desc"/>'
        self.assertEqual(node.to_html(), expected_html)


class TestLeafNodeImg(unittest.TestCase):
    """Unit tests for the LeafNode class specifically for 'img' tag handling."""

    def test_leaf_img_without_src(self) -> None:
        node = LeafNode("img", "", props={"alt": "desc"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_img_with_empty_props(self) -> None:
        node = LeafNode("img", "", props={})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_img_with_none_props(self) -> None:
        node = LeafNode("img", "", props=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_img_with_src_and_alt(self):
        node = LeafNode("img", "", props={"src": "cat.png", "alt": "A cat"})
        expected_html = '<img src="cat.png" src="cat.png" alt="A cat"/>'
        self.assertEqual(node.to_html(), expected_html)


class TestLeafNodeA(unittest.TestCase):
    """Unit tests for the LeafNode class specifically for 'a' tag handling."""

    def test_leaf_to_html_img_missing_src(self):
        node = LeafNode("img", "", props={"alt": "desc"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_img_empty_props(self):
        node = LeafNode("img", "", props={})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_img_none_props(self):
        node = LeafNode("img", "", props=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode(
            "a", "Click here", props={"href": "https://example.com", "target": "_blank"}
        )
        expected_html = '<a href="https://example.com" href="https://example.com" target="_blank">\
Click here</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_to_html_a_missing_href(self):
        node = LeafNode("a", "No link", props={"target": "_blank"})
        with self.assertRaises(ValueError):
            node.to_html()


class TestLeafNodeNoTag(unittest.TestCase):
    """Unit tests for the LeafNode class when no tag is provided."""

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_no_value_non_img_a(self):
        node = LeafNode("span", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_regular_tag(self):
        node = LeafNode("em", "emphasized")
        self.assertEqual(node.to_html(), "<em>emphasized</em>")
