from textnode import TextNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"

def main():
    node = TextNode("Hello, World!", TextType.BOLD, "https://example.com")
    print(node)

if __name__ == "__main__":
    main() 