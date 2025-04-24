from generate_page import generate_page, generate_pages_recursive
from copy_static_to_public import copy_static_to_docs
import sys

def main():
    if len(sys.argv) > 1:
            basepath = sys.argv[1]
    else:
        basepath = "/"

    if not basepath.startswith("/"):
        basepath = "/" + basepath
        print(f"INFO: Prepended '/' to basepath. Using: {basepath}")
    if basepath != "/" and basepath.endswith("/"):
        basepath = basepath.rstrip("/")
        print(f"INFO: Removed trailing '/' from basepath. Using: {basepath}")

    copy_static_to_docs()
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


main()
