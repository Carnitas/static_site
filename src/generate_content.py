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


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
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
    page_content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML page
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_content)
