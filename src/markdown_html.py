from src.block_markdown import BlockType, block_to_block_type
from src.htmlnode import HTMLNode, ParentNode
from src.inline_markdown import markdown_to_blocks, text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Convert a markdown string to an HTMLNode.

    :param markdown: The markdown string to convert.
    :return: An HTMLNode representing the converted markdown.
    """
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode(tag="div", children=[])

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            parent_node.children.append(handle_paragraph(block))
        elif block_type == BlockType.HEADING:
            parent_node.children.extend(handle_heading(block))
        elif block_type == BlockType.CODE:
            parent_node.children.append(handle_code(block))
        elif block_type == BlockType.QUOTE:
            parent_node.children.append(handle_quote(block))
        elif block_type == BlockType.ORDERED_LIST:
            parent_node.children.append(handle_ordered_list(block))
        elif block_type == BlockType.UNORDERED_LIST:
            parent_node.children.append(handle_unordered_list(block))

    return parent_node


def text_node_to_parent_node(
    text_nodes: list[TextNode], tag: str = "div"
) -> ParentNode:
    """
    Convert a list of TextNode objects to a ParentNode.

    :param text_nodes: List of TextNode objects to convert.
    :return: A ParentNode containing the converted HTMLNodes.
    """
    return ParentNode(
        tag, children=[text_node_to_html_node(node) for node in text_nodes]
    )


def handle_paragraph(block: str) -> ParentNode:
    paragraph_text = block.replace("\n", " ").strip()
    text_nodes = text_to_textnodes(paragraph_text)
    return text_node_to_parent_node(text_nodes, tag="p")


def handle_heading(block: str) -> list[ParentNode]:
    nodes = []
    for heading in block.split("\n"):
        heading_level = len(heading) - len(heading.lstrip("#"))
        heading_text = heading.lstrip("#").strip()
        text_nodes = text_to_textnodes(heading_text)
        heading_node = text_node_to_parent_node(text_nodes, tag=f"h{heading_level}")
        nodes.append(heading_node)
    return nodes


def handle_code(block: str) -> ParentNode:
    code_text = TextNode(block.replace("```", "").lstrip(), TextType.TEXT)
    code_node = text_node_to_html_node(code_text)
    code_html_node = ParentNode(tag="code", children=[code_node])
    return ParentNode(tag="pre", children=[code_html_node])


def handle_quote(block: str) -> ParentNode:
    quote_text = block.replace(">", "").strip()
    joined_quote_text = "".join(quote_text.split("\n"))
    text_nodes = text_to_textnodes(joined_quote_text)
    return text_node_to_parent_node(text_nodes, tag="blockquote")


def handle_ordered_list(block: str) -> ParentNode:
    list_items = block.split("\n")
    list_nodes: list[HTMLNode] = []
    for item in list_items:
        item_text = item.lstrip("1234567890. ").strip()
        text_nodes = text_to_textnodes(item_text)
        list_node = text_node_to_parent_node(text_nodes, tag="li")
        list_nodes.append(list_node)
    return ParentNode(tag="ol", children=list_nodes)


def handle_unordered_list(block: str) -> ParentNode:
    list_items = block.split("\n")
    list_nodes: list[HTMLNode] = []
    for item in list_items:
        item_text = item.lstrip("- ").strip()
        text_nodes = text_to_textnodes(item_text)
        list_node = text_node_to_parent_node(text_nodes, tag="li")
        list_nodes.append(list_node)
    return ParentNode(tag="ul", children=list_nodes)
