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

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str | None:
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


class LeafNode(HTMLNode):
    """
    A leaf node in the HTML tree, which has no children.

    :param tag: The HTML tag (e.g., 'div', 'span').
    :param value: A string value representing the value of the html tag.
    :param props: A dictionary of attributes for the HTML tag.
    """

    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        """
        Convert the leaf node to an HTML string.

        :return: An HTML string representation of the node.
        """
        if not self.value:
            raise ValueError("LeafNode must have a value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    A parent node in the HTML tree, which can have children.

    :param tag: The HTML tag (e.g., 'div', 'span').
    :param children: A list of child nodes.
    :param props: A dictionary of attributes for the HTML tag.
    """

    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        """
        Convert the parent node and its children to an HTML string.

        :return: An HTML string representation of the node and its children.
        """
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        if not self.children:
            raise ValueError("ParentNode must have children.")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
