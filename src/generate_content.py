import os

from src.markdown_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Extracts the first H1 header from the markdown string.
    Returns the header text without the leading '#' and whitespace.
    Raises ValueError if no H1 header is found.
    """
    for line in markdown.splitlines():
        if line.lstrip().startswith("# "):
            return line.lstrip()[2:].strip()
        if line.lstrip().startswith("#") and not line.lstrip().startswith("##"):
            # Handles cases like "#Title" (no space after #)
            return line.lstrip()[1:].strip()
    raise ValueError("No H1 header found in markdown.")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str = "/"
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, encoding="utf-8") as f:
        markdown_content = f.read()

    # Read template content
    with open(template_path, encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders
    page_content = (
        template_content.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
        .replace('src="/', f'src="{basepath}')
        .replace('href="/', f'href="{basepath}')
    )

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML page
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/"
) -> None:
    """
    Recursively generate pages from markdown files in a directory.

    :param dir_path_content: Path to the directory containing markdown files.
    :param template_path: Path to the HTML template file.
    :param dest_dir_path: Path to the destination directory for generated HTML files.
    """
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(
                    dest_dir_path, relative_path.replace(".md", ".html")
                )
                generate_page(from_path, template_path, dest_path, basepath=basepath)
