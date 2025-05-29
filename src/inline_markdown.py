import re

from src.textnode import TextNode, TextType


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
        if len(parts) == 1:
            new_nodes.append(node)
        if len(parts) > 1:
            for i, part in enumerate(parts):
                if not part.strip():
                    continue
                if not i % 2:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split text nodes by markdown images and convert them to TextNode objects.

    :param old_nodes: List of TextNode objects to be split.
    :return: A list of new TextNode objects with images.
    """
    new_nodes = []
    for node in old_nodes:
        parts = extract_markdown_images(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        text_parts = re.split(r"!\[.*?\]\(.*?\)", node.text)
        for i, part in enumerate(text_parts):
            if part.strip():
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(parts):
                image_text, url = parts[i]
                new_nodes.append(TextNode(image_text, TextType.IMAGE, url))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split text nodes by markdown links and convert them to TextNode objects.

    :param old_nodes: List of TextNode objects to be split.
    :return: A list of new TextNode objects with links.
    """
    new_nodes = []
    for node in old_nodes:
        parts = extract_markdown_links(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        text_parts = re.split(r"\[.*?\]\(.*?\)", node.text)
        for i, part in enumerate(text_parts):
            if part.strip():
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(parts):
                link_text, url = parts[i]
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Convert a plain text string into a list of TextNode objects.

    :param text: The plain text to convert.
    :return: A list of TextNode objects with appropriate TextType and URLs.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    delimiter_map = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    for delimiter, text_type in delimiter_map.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Convert markdown text to a list of block strings
    :param markdown: The markdown text to convert.
    :return: A list of block strings.
    """
    blocks = []
    lines = markdown.split("\n")
    current_block: list[str] = []

    for line in lines:
        if not line.strip():
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line.strip())

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks
