import unittest

from src.inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
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
        assert new_nodes[0] == TextNode("This is text with a ", TextType.TEXT)
        assert new_nodes[1] == TextNode("code block", TextType.CODE)
        assert new_nodes[2] == TextNode(" word", TextType.TEXT)
        assert new_nodes[3] == TextNode("Another ", TextType.TEXT)
        assert new_nodes[4] == TextNode("example", TextType.CODE)
        assert new_nodes[5] == TextNode(" of splitting", TextType.TEXT)


class TestExtractMarkdown(unittest.TestCase):
    """Unit tests for extracting markdown images and links."""

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


class TestSplitNodes(unittest.TestCase):
    """Unit tests for splitting nodes by images and links."""

    def test_split_images(self) -> None:
        """Test the split_nodes_image function with a single node containing multiple images."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self) -> None:
        """Test the split_nodes_link function with a single node containing multiple links."""
        node = TextNode(
            "This is text with a [link](https://example.com) "
            "and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_nodes_image(self) -> None:
        """Test the split_nodes_image function with a single node containing multiple images."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_parts(self) -> None:
        """
        Test that split_nodes_link does not modify nodes without links.
        """
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_no_parts(self) -> None:
        """
        Test that split_nodes_image does not modify nodes without images.
        """
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    """Unit tests for the text_to_textnodes function."""

    def test_text_to_textnodes_plain_text(self) -> None:
        """
        Test text_to_textnodes with plain text (no formatting).
        """
        text = "This is a simple sentence."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is a simple sentence.", TextType.TEXT)], nodes
        )

    def test_text_to_textnodes_bold(self) -> None:
        """
        Test text_to_textnodes with bold formatting.
        """
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_italic(self) -> None:
        """
        Test text_to_textnodes with italic formatting.
        """
        text = "This is _italic_ text."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_code(self) -> None:
        """
        Test text_to_textnodes with code formatting.
        """
        text = "This is `code` text."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text.", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_image(self) -> None:
        """
        Test text_to_textnodes with an image.
        """
        text = "Here is an image: ![alt](http://img.com/img.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Here is an image: ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "http://img.com/img.png"),
            ],
            nodes,
        )

    def test_text_to_textnodes_link(self) -> None:
        """
        Test text_to_textnodes with a link.
        """
        text = "Here is a [link](http://example.com)."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://example.com"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_mixed(self) -> None:
        """
        Test text_to_textnodes with mixed formatting.
        """
        text = (
            "This is **bold** and _italic_ and `code` and ![img](url) and [link](url2)."
        )
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url2"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_same_format(self) -> None:
        """
        Test text_to_textnodes with multiple bold and italic segments.
        """
        text = "**bold1** normal **bold2** _italic1_ _italic2_"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" normal ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode("italic1", TextType.ITALIC),
                TextNode("italic2", TextType.ITALIC),
            ],
            nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    """Unit tests for the markdown_to_blocks function."""

    def test_markdown_to_blocks(self) -> None:
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self) -> None:
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self) -> None:
        md = "This is a single block with no empty lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block with no empty lines."])

    def test_markdown_to_blocks_multiple_blocks(self) -> None:
        md = "First block\n\nSecond block\n\nThird block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])

    def test_markdown_to_blocks_trailing_leading_empty_lines(self) -> None:
        md = "\n\nFirst block\n\nSecond block\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_markdown_to_blocks_multiline_blocks(self) -> None:
        md = "Line 1\nLine 2\n\nLine 3\nLine 4"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1\nLine 2", "Line 3\nLine 4"])

    def test_markdown_to_blocks_only_empty_lines(self) -> None:
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_block_with_only_spaces(self) -> None:
        md = "   \nBlock 1\n   \n\nBlock 2\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])
