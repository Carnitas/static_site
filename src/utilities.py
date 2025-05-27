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
