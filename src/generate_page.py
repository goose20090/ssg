import os
from block_markdown import extract_header_from_markdown, markdown_to_html_nodes
from pathlib import Path


def generate_page(from_path, template_path, dest_path, basepath = "/"):
    print(f"generating page from {from_path} to {dest_path}")

    md_file = open(from_path)
    template_file = open(template_path)

    md_str = md_file.read()
    template_str = template_file.read()


    content = markdown_to_html_nodes(md_str).to_html()
    title = extract_header_from_markdown(md_str)

    template_str = template_str.replace("{{ Title }}", title)
    template_str = template_str.replace("{{ Content }}", content)
    template_str = template_str.replace("href=\"/", f"href=\"{basepath}")
    template_str = template_str.replace("src=\"/", f"src=\"{basepath}")

    with open(dest_path, "w") as dest_file:
            dest_file.write(template_str)

# Crawl every entry in the content directory
# For each markdown file found, generate a new .html file using the same template.html. 
# The generated pages should be written to the public directory in the same directory structure.


# generate_page("./content/index.md", "./template.html", "./public/index.html")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath = "/"):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)


    contents = os.listdir(dir_path_content)

    md_files = []

    dirs = []

    for file in contents:
        path = os.path.join(dir_path_content, file)
        if os.path.isfile(path):
            md_files.append(file)
        if os.path.isdir(path):
            dirs.append(file)

    for file in md_files:
        dest_path = os.path.join(dest_dir_path, file)
        dest_path = Path(dest_path).with_suffix(".html")
        generate_page(os.path.join(dir_path_content, file), template_path, str(dest_path), basepath)


    for dir in dirs:
        generate_pages_recursive(os.path.join(dir_path_content, dir), template_path, os.path.join(dest_dir_path, dir))

