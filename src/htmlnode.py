class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
       raise NotImplementedError
       
    def props_to_html(self):
       stringified_dict = ""
       for obj in self.props:
           for key, value in obj.items():
               stringified_dict += f' {key}="{value}"'
       return stringified_dict

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"