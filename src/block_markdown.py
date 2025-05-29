import re
from enum import Enum


class BlockType(Enum):
    """
    Enum representing different types of blocks in a static site.
    """

    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "list"
    UNORDERED_LIST = "ulist"


def block_to_block_type(block: str) -> BlockType:
    """
    Convert a block string to a BlockType.

    :param block: The block string to convert.
    :return: A BlockType corresponding to the block string.
    """
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if re.match(r"^\d+\.\s", block):
        return BlockType.ORDERED_LIST
    if block.startswith("- "):
        return BlockType.UNORDERED_LIST
    return BlockType.PARAGRAPH
