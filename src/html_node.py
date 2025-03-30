class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props

    def __eq__(self, other):
        return (self.tag, self.value, self.children, self.props) == (other.tag, other.value, other.children, other.props)

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        if self.props == None:
            raise Exception("uh oh")
        result = "" 
        for key, value in self.props.items():
            result += f"{key}=\"{value}\" "
        return result[:-1]


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"
