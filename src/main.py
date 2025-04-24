from generate_page import generate_page, generate_pages_recursive
from text_node import TextNode, TextType
from copy_static_to_public import copy_static_to_public

def main():

    copy_static_to_public()
    generate_pages_recursive("./content", "./template.html", "./public")


main()
