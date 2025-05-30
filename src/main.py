import os
import shutil
import sys

from src.generate_content import generate_pages_recursive


def main() -> None:  # pragma: no cover
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    clear_directory("docs")
    copy_static_to_docs()
    generate_pages_recursive("content", "template.html", "docs", basepath=basepath)


def clear_directory(directory: str) -> None:
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


def copy_directory(src: str, dst: str) -> None:
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory(s, d)
        else:
            shutil.copy2(s, d)
            print(f"Copied: {s} -> {d}")


def copy_static_to_docs() -> None:
    src = "static"
    dst = "docs"
    clear_directory(dst)
    copy_directory(src, dst)


if __name__ == "__main__":
    main()
