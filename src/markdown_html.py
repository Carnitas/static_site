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
            paragraph_text = block.replace("\n", " ").strip()
            text_nodes = text_to_textnodes(paragraph_text)
            paragraph_node = text_node_to_parent_node(text_nodes, tag="p")
            parent_node.children.append(paragraph_node)
        elif block_type == BlockType.HEADING:
            heading_level = block.count("#")
            heading_text = block.lstrip("#").strip()
            text_nodes = text_to_textnodes(heading_text)
            heading_node = text_node_to_parent_node(text_nodes, tag=f"h{heading_level}")
            parent_node.children.append(heading_node)
        elif block_type == BlockType.CODE:
            code_text = TextNode(block.replace("```", "").lstrip(), TextType.TEXT)
            code_node = text_node_to_html_node(code_text)
            code_html_node = ParentNode(tag="code", children=[code_node])
            code_html_wrapper = ParentNode(tag="pre", children=[code_html_node])
            parent_node.children.append(code_html_wrapper)

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
