class HTMLNode:
    """
    Create a simple HTML node representation.

    :param tag: The HTML tag (e.g., 'div', 'span').
    :param value: A string value representing the value of the html tag.
    :param children: A list of child nodes or strings.
    :param props: A dictionary of attributes for the HTML tag.
    :return: A dictionary representing the HTML node.
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.props = props if props else {}

    def to_html(self) -> None:
        raise NotImplementedError

    def props_to_html(self) -> str:
        """
        Convert the properties dictionary to an HTML attribute string.

        :return: A string of HTML attributes.
        """
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        return (
            f"HTMLNode("
            f"tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )
