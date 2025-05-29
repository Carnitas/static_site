import unittest

from src.markdown_html import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    """Test cases for markdown_to_html_node function."""

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>\
<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\
\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading 1\n## Heading 2\n### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_blockquote(self):
        md = "> This is a quote\n> with two lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with two lines</blockquote></div>",
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_unordered_list(self):
        md = "- Apple\n- Banana\n- Cherry"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul></div>",
        )

    def test_mixed_blocks(self):
        md = """# Title

Some paragraph text.

- Item 1
- Item 2

> A quote

1. First
2. Second
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>Some paragraph text.</p><ul><li>Item 1</li><li>Item 2</li></ul>\
<blockquote>A quote</blockquote><ol><li>First</li><li>Second</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
