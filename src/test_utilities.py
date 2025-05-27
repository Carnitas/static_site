import unittest

from textnode import TextNode, TextType
from utilities import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)


class TestUtilities(unittest.TestCase):
    """Unit tests for utility functions in the static site generator."""

    def test_split_nodes_delimiter(self) -> None:
        """
        Test the split_nodes_delimiter function.
        """
        old_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("Another `example` of splitting", TextType.TEXT),
        ]
        delimiter = "`"
        text_type = TextType.CODE

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        assert len(new_nodes) == 6
        assert new_nodes[0] == TextNode("This is text with a", text_type)
        assert new_nodes[1] == TextNode("code block", text_type)
        assert new_nodes[2] == TextNode("word", text_type)
        assert new_nodes[3] == TextNode("Another", text_type)
        assert new_nodes[4] == TextNode("example", text_type)
        assert new_nodes[5] == TextNode("of splitting", text_type)

    def test_empty_parts(self) -> None:
        """
        Test that empty parts are not included in the new nodes.
        """
        old_nodes = [TextNode("This is text with a ` ` missing part", TextType.TEXT)]
        delimiter = "`"
        text_type = TextType.CODE

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        assert len(new_nodes) == 2
        assert new_nodes[0] == TextNode("This is text with a", text_type)
        # assert new_nodes[1] == TextNode(" ", text_type)  # This should be empty
        assert new_nodes[1] == TextNode("missing part", text_type)

    def test_extract_markdown_images(self) -> None:
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self) -> None:
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
