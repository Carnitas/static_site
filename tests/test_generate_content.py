import os
import tempfile
import unittest
from unittest import mock

import pytest

from src.generate_content import extract_title, generate_page


class TestExtractTitle(unittest.TestCase):
    """Tests for the extract_title function."""

    def test_extract_title_with_space(self):
        md = "# My Title\nSome content"
        assert extract_title(md) == "My Title"

    def test_extract_title_without_space(self):
        md = "#MyTitle\nSome content"
        assert extract_title(md) == "MyTitle"

    def test_extract_title_ignores_h2(self):
        md = "## Subtitle\n# Main Title"
        assert extract_title(md) == "Main Title"

    def test_extract_title_first_h1(self):
        md = "# First Title\n# Second Title"
        assert extract_title(md) == "First Title"

    def test_extract_title_leading_whitespace(self):
        md = "   #   Whitespace Title   "
        assert extract_title(md) == "Whitespace Title"

    def test_extract_title_no_h1_raises(self):
        md = "## Subtitle\nSome text\n- List item"
        with pytest.raises(ValueError, match="No H1 header found in markdown."):
            extract_title(md)

    def test_extract_title_h1_in_middle(self):
        md = "Intro text\n# Middle Title\nMore text"
        assert extract_title(md) == "Middle Title"

    def test_extract_title_h1_with_extra_hashes(self):
        md = "### Not H1\n# Real Title"
        assert extract_title(md) == "Real Title"

    def test_extract_title_h1_with_tabs(self):
        md = "\t# Tabbed Title"
        assert extract_title(md) == "Tabbed Title"


class DummyHtmlNode:
    """
    A dummy HTML node for testing purposes.
    This class simulates the behavior of an HTML node, allowing us to mock
    the markdown_to_html_node function without needing a real HTML node implementation.
    :param html: The HTML content to return when to_html() is called.
    """

    def __init__(self, html):
        self._html = html

    def to_html(self):
        return self._html

    def __str__(self):
        return self._html


@mock.patch("src.generate_content.markdown_to_html_node")
@mock.patch("src.generate_content.extract_title")
def test_generate_page_creates_html_file(mock_extract_title, mock_md_to_html):
    # Setup dummy return values
    mock_extract_title.return_value = "Test Title"
    mock_md_to_html.return_value = DummyHtmlNode("<p>Test HTML</p>")

    # Create temp files for markdown and template
    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = os.path.join(tmpdir, "test.md")
        tpl_path = os.path.join(tmpdir, "template.html")
        dest_path = os.path.join(tmpdir, "output", "index.html")

        md_content = "# Test Title\nSome content"
        tpl_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}\
</body></html>"

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        with open(tpl_path, "w", encoding="utf-8") as f:
            f.write(tpl_content)

        generate_page(md_path, tpl_path, dest_path)

        # Check output file exists
        assert os.path.exists(dest_path)
        # Check content
        with open(dest_path, encoding="utf-8") as f:
            output = f.read()
        assert "<title>Test Title</title>" in output
        assert "<p>Test HTML</p>" in output


@mock.patch("src.generate_content.markdown_to_html_node")
@mock.patch("src.generate_content.extract_title")
def test_generate_page_creates_parent_dirs(mock_extract_title, mock_md_to_html):
    mock_extract_title.return_value = "Dir Title"
    mock_md_to_html.return_value = DummyHtmlNode("<p>Dir HTML</p>")

    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = os.path.join(tmpdir, "a.md")
        tpl_path = os.path.join(tmpdir, "b.html")
        dest_dir = os.path.join(tmpdir, "nested", "dir")
        dest_path = os.path.join(dest_dir, "index.html")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Dir Title\nContent")
        with open(tpl_path, "w", encoding="utf-8") as f:
            f.write("<html>{{ Title }}{{ Content }}</html>")

        # Directory does not exist before
        assert not os.path.exists(dest_dir)
        generate_page(md_path, tpl_path, dest_path)
        # Directory should exist after
        assert os.path.exists(dest_dir)
        assert os.path.exists(dest_path)


@mock.patch("src.generate_content.markdown_to_html_node")
@mock.patch("src.generate_content.extract_title")
def test_generate_page_replaces_both_placeholders(mock_extract_title, mock_md_to_html):
    mock_extract_title.return_value = "Placeholder Title"
    mock_md_to_html.return_value = DummyHtmlNode("<div>HTML</div>")

    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = os.path.join(tmpdir, "c.md")
        tpl_path = os.path.join(tmpdir, "c.html")
        dest_path = os.path.join(tmpdir, "out.html")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Placeholder Title\nBody")
        with open(tpl_path, "w", encoding="utf-8") as f:
            f.write("{{ Title }} -- {{ Content }}")

        generate_page(md_path, tpl_path, dest_path)
        with open(dest_path, encoding="utf-8") as f:
            content = f.read()
        assert "Placeholder Title" in content
        assert "<div>HTML</div>" in content
        assert content == "Placeholder Title -- <div>HTML</div>"


if __name__ == "__main__":
    unittest.main()
    pytest.main([__file__])
