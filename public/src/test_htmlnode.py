import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

if __name__ == "__main__":
    unittest.main() 