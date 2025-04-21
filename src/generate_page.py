import os
from block_markdown import extract_header_from_markdown, markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path}")

    md_file = open(from_path)
    template_file = open(template_path)

    md_str = md_file.read()
    template_str = template_file.read()


    content = markdown_to_html_node(md_str).to_html()
    title = extract_header_from_markdown(md_str)

    template_str = template_str.replace("{{ Title }}", title)
    template_str = template_str.replace("{{ Content }}", content)

    with open(dest_path, "w") as dest_file:
            dest_file.write(template_str)
