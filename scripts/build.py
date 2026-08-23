from pathlib import Path
from urllib.parse import quote
import html
import os
import shutil


SOURCE = Path("site")
OUTPUT = Path("_site")


def build_site():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)

    shutil.copytree(SOURCE, OUTPUT)

    directories = [OUTPUT]
    directories.extend(
        path
        for path in OUTPUT.rglob("*")
        if path.is_dir() and not path.name.startswith(".")
    )

    for directory in directories:
        generate_index(directory)


def generate_index(directory):
    index = directory / "index.html"

    # A hand-written index.html always wins.
    if index.exists():
        return

    relative_directory = directory.relative_to(OUTPUT)

    if relative_directory.parts:
        display_path = "/" + relative_directory.as_posix() + "/"
    else:
        display_path = "/"

    stylesheet = os.path.relpath(
        OUTPUT / "style.css",
        start=directory,
    ).replace(os.sep, "/")

    directories = sorted(
        (
            path
            for path in directory.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        ),
        key=lambda path: path.name.lower(),
    )

    files = sorted(
        (
            path
            for path in directory.iterdir()
            if path.is_file()
            and path.name != "index.html"
            and not path.name.startswith(".")
        ),
        key=lambda path: path.name.lower(),
    )

    links = []

    if relative_directory.parts:
        links.append('<a href="../">../</a>')

    for path in directories:
        name = html.escape(path.name)
        href = quote(path.name) + "/"
        links.append(f'<a href="{href}">{name}/</a>')

    for path in files:
        name = html.escape(path.name)
        href = quote(path.name)
        links.append(f'<a href="{href}">{name}</a>')

    listing = "\n".join(links)

    page = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Index of {html.escape(display_path)}</title>
    <link rel="stylesheet" href="{stylesheet}">
</head>

<body>
    <h1>Index of {html.escape(display_path)}</h1>

    <pre>{listing}</pre>
</body>
</html>
"""

    index.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build_site()
