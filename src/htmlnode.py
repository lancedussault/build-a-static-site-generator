class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
       raise NotImplementedError("to_html method is not implemented")
       
    def props_to_html(self):
       stringified_dict = ""
       if self.props is None:
           return ""
       for key, value in self.props.items():
           stringified_dict += f' {key}="{value}"'
       return stringified_dict

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value good sir!")
        if self.tag is None:
            return self.value
        stringified_prop = self.props_to_html()
        return f"<{self.tag}{stringified_prop}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"