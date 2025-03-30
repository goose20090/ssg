from text_node import TextNode, TextType

def main():
    tn = TextNode("test", TextType.LINK, "https://www.boot.dev")
    print(tn.__repr__())


main()
