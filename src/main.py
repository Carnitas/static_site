from src.textnode import TextNode


def main() -> None:  # pragma: no cover
    first_text_node = TextNode("This is some text", "link", "https://example.com")
    print(first_text_node)


if __name__ == "__main__":
    main()
