import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_dif2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_dif3(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)

    # Testes para a função split_nodes_delimiter
    def test_split_nodes_delimiter_bold(self):
        # Teste para delimitador de negrito
        node = TextNode("This is **bold** text", TextType.TEXT)
        nodes = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(nodes, expected)
    
    def test_split_nodes_delimiter_multiple(self):
        # Teste para múltiplos delimitadores no mesmo texto
        node = TextNode("This is **bold** and **more bold** text", TextType.TEXT)
        nodes = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(nodes, expected)
    
    def test_split_nodes_delimiter_skip_non_text(self):
        # Teste para verificar se nós que não são do tipo TEXT são ignorados
        node1 = TextNode("This is **bold** text", TextType.TEXT)
        node2 = TextNode("This is italic text", TextType.ITALIC)
        nodes = TextNode.split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("This is italic text", TextType.ITALIC)
        ]
        
        self.assertEqual(nodes, expected)
    
    def test_split_nodes_delimiter_odd_delimiters(self):
        # Teste para verificar se a função lança exceção com número ímpar de delimitadores
        node = TextNode("This is **bold text", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertTrue("Odd number of '**' delimiters" in str(context.exception))
    
    def test_split_nodes_delimiter_no_delimiter(self):
        # Teste para verificar se a função lança exceção quando não há delimitador
        node = TextNode("This is plain text", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertTrue("No '**' delimiter found" in str(context.exception))

    def test_extract_markdown_images(self):
        matches = TextNode.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        # Teste para extrair múltiplas imagens
        text = "Here are two images: ![first](https://example.com/img1.jpg) and ![second](https://example.com/img2.png)"
        matches = TextNode.extract_markdown_images(text)
        expected = [
            ("first", "https://example.com/img1.jpg"),
            ("second", "https://example.com/img2.png")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_images(self):
        # Teste para verificar comportamento quando não há imagens
        text = "This is just plain text with no images."
        matches = TextNode.extract_markdown_images(text)
        self.assertEqual(0, len(matches))

    def test_extract_markdown_links(self):
        # Teste básico para extrair links
        text = "Visit [my website](https://example.com) for more information."
        matches = TextNode.extract_markdown_links(text)
        self.assertListEqual([("my website", "https://example.com")], matches)

    def test_extract_markdown_links_with_images(self):
        # Teste para verificar que links dentro de imagens não são capturados
        text = "Here's a ![image](https://example.com/img.jpg) and a [link](https://example.com)"
        matches = TextNode.extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    # Testes para split_nodes_image
    def test_split_nodes_image_basic(self):
        # Teste básico para a função split_nodes_image
        node = TextNode("This is an ![example](https://example.com/img.jpg) image", TextType.TEXT)
        nodes = TextNode.split_nodes_image([node])
        
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("example", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" image", TextType.TEXT)
        ]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_image_multiple(self):
        # Teste para múltiplas imagens
        node = TextNode("![first](https://example.com/img1.jpg) and ![second](https://example.com/img2.png)", TextType.TEXT)
        nodes = TextNode.split_nodes_image([node])
        
        expected = [
            TextNode("first", TextType.IMAGE, "https://example.com/img1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "https://example.com/img2.png")
        ]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_image_no_images(self):
        # Teste para texto sem imagens
        node = TextNode("This is just plain text", TextType.TEXT)
        nodes = TextNode.split_nodes_image([node])
        
        expected = [node]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_image_skip_non_text(self):
        # Teste para verificar que nós não-TEXT são ignorados
        node1 = TextNode("![image](https://example.com/img.jpg)", TextType.TEXT)
        node2 = TextNode("This is bold", TextType.BOLD)
        nodes = TextNode.split_nodes_image([node1, node2])
        
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode("This is bold", TextType.BOLD)
        ]
        
        self.assertEqual(nodes, expected)

    # Testes adicionais para split_nodes_image
    def test_split_nodes_image_empty_alt_text(self):
        # Teste para imagem com texto alternativo vazio
        node = TextNode("This is an image with empty alt text: ![](https://example.com/img.jpg)", TextType.TEXT)
        nodes = TextNode.split_nodes_image([node])
        
        expected = [
            TextNode("This is an image with empty alt text: ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/img.jpg")
        ]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_image_consecutive(self):
        # Teste para imagens consecutivas sem texto entre elas
        node = TextNode("![img1](https://example.com/img1.jpg)![img2](https://example.com/img2.jpg)", TextType.TEXT)
        nodes = TextNode.split_nodes_image([node])
        
        expected = [
            TextNode("img1", TextType.IMAGE, "https://example.com/img1.jpg"),
            TextNode("img2", TextType.IMAGE, "https://example.com/img2.jpg")
        ]
        
        self.assertEqual(nodes, expected)

    # Testes para split_nodes_link
    def test_split_nodes_link_basic(self):
        # Teste básico para a função split_nodes_link
        node = TextNode("This is a [link](https://example.com) in text", TextType.TEXT)
        nodes = TextNode.split_nodes_link([node])
        
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in text", TextType.TEXT)
        ]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_link_multiple(self):
        # Teste para múltiplos links
        node = TextNode("Visit [site1](https://example1.com) and [site2](https://example2.com)", TextType.TEXT)
        nodes = TextNode.split_nodes_link([node])
        
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("site1", TextType.LINK, "https://example1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("site2", TextType.LINK, "https://example2.com")
        ]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_link_no_links(self):
        # Teste para texto sem links
        node = TextNode("This is just plain text", TextType.TEXT)
        nodes = TextNode.split_nodes_link([node])
        
        expected = [node]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_link_skip_non_text(self):
        # Teste para verificar que nós não-TEXT são ignorados
        node1 = TextNode("[link](https://example.com)", TextType.TEXT)
        node2 = TextNode("This is italic", TextType.ITALIC)
        nodes = TextNode.split_nodes_link([node1, node2])
        
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("This is italic", TextType.ITALIC)
        ]
        
        self.assertEqual(nodes, expected)

    # Testes adicionais para split_nodes_link
    def test_split_nodes_link_empty_text(self):
        # Teste para link com texto vazio
        node = TextNode("This is a link with empty text: [](https://example.com)", TextType.TEXT)
        nodes = TextNode.split_nodes_link([node])
        
        expected = [
            TextNode("This is a link with empty text: ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com")
        ]
        
        self.assertEqual(nodes, expected)

    def test_split_nodes_link_consecutive(self):
        # Teste para links consecutivos sem texto entre eles
        node = TextNode("[link1](https://example1.com)[link2](https://example2.com)", TextType.TEXT)
        nodes = TextNode.split_nodes_link([node])
        
        expected = [
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode("link2", TextType.LINK, "https://example2.com")
        ]
        
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_basic(self):
        # Teste básico com diferentes tipos de formatação
        text = "This is **bold** and *italic* text with `code`."
        nodes = TextNode.text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]
        
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_complex(self):
        # Teste com combinação de links, imagens e formatação
        text = "Check this **important** [link](https://example.com) and ![image](https://example.com/img.jpg)"
        nodes = TextNode.text_to_textnodes(text)
        
        expected = [
            TextNode("Check this ", TextType.TEXT),
            TextNode("important", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg")
        ]
        
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_mixed_delimiters(self):
        # Teste com diferentes delimitadores misturados no mesmo texto
        text = "This has **bold**, *italic*, and `code` all together"
        nodes = TextNode.text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" all together", TextType.TEXT)
        ]
        
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_empty(self):
        # Teste com texto vazio
        text = ""
        nodes = TextNode.text_to_textnodes(text)
        
        # Deve retornar um único nó de texto vazio
        expected = [TextNode("", TextType.TEXT)]
        
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
