import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        props = {
            "href": "https://example.com",
            "class": "link",
            "target": "_blank",
            "data-info": "123"
        }
        node = HTMLNode(props=props)
        expected = ' href="https://example.com" class="link" target="_blank" data-info="123"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr_representation(self):
        child = HTMLNode(tag="span", value="child")
        parent = HTMLNode(
            tag="div",
            children=[child],
            props={"class": "container"}
        )
        expected = "HTMLNode('div', None, [HTMLNode('span', 'child', [], {})], {'class': 'container'})"
        self.assertEqual(repr(parent), expected)


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_image_with_special_characters(self):
        # Teste com caracteres especiais no texto alt e URL com caracteres especiais
        node = TextNode("Imagem com caracteres especiais: !@#$%^&*()", TextType.IMAGE, 
                        "https://example.com/image?param=value&special=true")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "Imagem com caracteres especiais: !@#$%^&*()")
        self.assertEqual(html_node.props["src"], "https://example.com/image?param=value&special=true")
    
    def test_link_with_empty_text(self):
        # Teste com texto vazio mas URL válido
        node = TextNode("", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["href"], "https://example.com")
    
    def test_code_with_html_characters(self):
        # Teste com código que contém caracteres HTML que precisariam ser escapados
        code_text = "<div>This is HTML code & it has special chars</div>"
        node = TextNode(code_text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, code_text)
        self.assertEqual(html_node.to_html(), f"<code>{code_text}</code>")

if __name__ == "__main__":
    unittest.main() 