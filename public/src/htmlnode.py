class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        attributes = []
        for key, value in self.props.items():
            attributes.append(f'{key}="{value}"')
        return " " + " ".join(attributes)
    
    def __repr__(self):
        value_repr = 'None' if self.value is None else f"'{self.value}'"
        return f"HTMLNode('{self.tag}', {value_repr}, {self.children}, {self.props})"
    
    