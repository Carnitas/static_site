from enum import Enum

from src.htmlnode import HTMLNode, LeafNode


class TextType(Enum):
    """
    Enum representing different types of text content.
    """

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """
    Class representing a text node with a type and content.
    """

    def __init__(
        self,
        text: str,
        text_type: TextType | str | None = None,
        url: str | None = None,
    ):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TextNode):
            return NotImplemented
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        if self.url:
            return f"TextNode({self.text!r}, {self.text_type}, {self.url!r})"
        return f"TextNode({self.text!r}, {self.text_type})"


def text_node_to_html_node(node: TextNode) -> HTMLNode:
    """
    Convert a TextNode to an HTMLNode.

    :param node: The TextNode to convert.
    :return: An HTMLNode representation of the TextNode.
    """
    match node.text_type:
        case TextType.TEXT | None:
            return LeafNode(tag="", value=node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=node.text)
        case TextType.LINK:
            if not node.url:
                raise ValueError("Link text nodes must have a URL.")
            return LeafNode(tag="a", value=node.text, props={"href": node.url})
        case TextType.IMAGE:
            if not node.url:
                raise ValueError("Image text nodes must have a URL.")
            return LeafNode(
                tag="img", value=node.text, props={"src": node.url, "alt": node.text}
            )
        case _:
            raise ValueError(f"Unknown text type: {node.text_type}")
