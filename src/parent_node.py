from html_node import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        if tag is None or children is None:
            raise ValueError("Tag and Children arguments are required for ParentNode.")
        super().__init__(tag=tag, value=None, children=children, props=props)


    def to_html(self):
        result = ""
        if self.children:
            for child in self.children:
                result += child.to_html()

        return f"<{self.tag}>{result}</{self.tag}>"
