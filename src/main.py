from generate_page import generate_page, generate_pages_recursive
from copy_static_to_public import copy_static_to_docs
import sys

def main():
    if len(sys.argv) > 1:
            basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_static_to_docs()
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


main()
