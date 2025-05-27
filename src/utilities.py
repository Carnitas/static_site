import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Split text nodes by a delimiter and convert them to the specified text type.

    :param old_nodes: List of TextNode objects to be split.
    :param delimiter: The delimiter to split the text nodes.
    :param text_type: The type of text for the new nodes.
    :return: A list of new TextNode objects with the specified text type.
    """
    new_nodes = []
    for node in old_nodes:
        parts = node.text.split(delimiter)
        for part in parts:
            if part.strip():  # Avoid empty parts
                new_nodes.append(TextNode(part.strip(), text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extract image URLs from a markdown text.

    :param text: The markdown text containing image URLs.
    :return: A list of image URLs found in the text.
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extract links from a markdown text.

    :param text: The markdown text containing links.
    :return: A list of links found in the text.
    """
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)
