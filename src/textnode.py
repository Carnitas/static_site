from enum import Enum


class TextType(Enum):
    """
    Enum representing different types of text content.
    """

    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGES = "images"


class TextNode:
    """
    Class representing a text node with a type and content.
    """

    def __init__(
        self,
        text: str | None = None,
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
        return f"TextNode(text={self.text!r}, text_type={self.text_type!r}, url={self.url!r})"
