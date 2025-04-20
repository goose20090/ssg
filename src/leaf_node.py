from src.html_node import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("Value is required for LeafNode.")
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        return f"<{self.tag}{" " + self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"
