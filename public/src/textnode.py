from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    # Adicione outros tipos conforme necessário

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
    def __repr__(self):
        return f"TextNode('{str(self.text).upper()}', {str(self.text_type.value).upper()}, '{str(self.url).upper() if self.url else None}')"
    
    