import unittest

from src.block_markdown import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    """Test cases for block_to_block_type function."""

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```python"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)

    def test_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(
            block_to_block_type("123. Another item"), BlockType.ORDERED_LIST
        )

    def test_unlist(self):
        self.assertEqual(
            block_to_block_type("- Unordered item"), BlockType.UNORDERED_LIST
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("  Some text with leading spaces."), BlockType.PARAGRAPH
        )
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
