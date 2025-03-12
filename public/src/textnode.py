from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
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
    
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        """
        Divide os nós de texto com base em um delimitador e atribui um tipo específico aos textos delimitados.
        
        Args:
            old_nodes: Lista de TextNode a ser processada
            delimiter: String que serve como delimitador (ex: "**", "_", "`")
            text_type: O TextType a ser aplicado ao texto entre delimitadores
        
        Returns:
            Uma nova lista de TextNode com os textos delimitados convertidos para o tipo especificado
        
        Raises:
            ValueError: Se o markdown for inválido (número ímpar de delimitadores ou delimitador não encontrado)
        """
        new_nodes = []
        delimiter_found = False
        
        for old_node in old_nodes:
            # Só processamos nós do tipo TEXT
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            # Dividimos o texto pelos delimitadores
            splits = old_node.text.split(delimiter)
            
            # Se não há delimitador no texto, mantemos o nó original
            if len(splits) == 1:
                new_nodes.append(old_node)
                continue
            
            # Marcamos que encontramos pelo menos um delimitador
            delimiter_found = True
            
            # Verificamos se temos um número ímpar de delimitadores (markdown inválido)
            if len(splits) % 2 == 0:
                raise ValueError(f"Invalid markdown: Odd number of '{delimiter}' delimiters")
            
            # Processamos os splits para criar novos nós
            for i in range(len(splits)):
                # Se o split não está vazio, adicionamos como nó de texto
                if splits[i]:
                    # Se é um índice par, é texto normal
                    if i % 2 == 0:
                        new_nodes.append(TextNode(splits[i], TextType.TEXT))
                    # Se é um índice ímpar, é texto delimitado
                    else:
                        new_nodes.append(TextNode(splits[i], text_type))
        
        # Se não encontramos nenhum delimitador em nenhum nó, lançamos uma exceção
        if not delimiter_found:
            raise ValueError(f"Invalid markdown: No '{delimiter}' delimiter found")
        
        return new_nodes
    
    @staticmethod
    def extract_markdown_images(text):
        """
        Extrai marcadores de imagens no formato Markdown ![alt text](url) de um texto
        e retorna uma lista de tuplas (alt_text, url).
        
        Args:
            text: String contendo o texto a ser analisado
        
        Returns:
            Uma lista de tuplas, onde cada tupla contém (texto_alternativo, url_da_imagem)
        
        Exemplo:
            Para o texto "Veja esta ![imagem](https://example.com/img.jpg) e ![outra](https://example.com/img2.png)"
            Retorna: [("imagem", "https://example.com/img.jpg"), ("outra", "https://example.com/img2.png")]
        """
        # Padrão regex para encontrar imagens no formato ![alt text](url)
        pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        
        # Encontra todas as ocorrências do padrão no texto
        matches = re.findall(pattern, text)
        
        # Retorna a lista de tuplas (alt_text, url)
        return matches
    
    @staticmethod
    def extract_markdown_links(text):
        """
        Extrai marcadores de links no formato Markdown [texto do link](url) de um texto
        e retorna uma lista de tuplas (texto_do_link, url).
        
        Returns:
            Uma lista de tuplas, onde cada tupla contém (texto_do_link, url)
        
        Exemplo:
            Para o texto "Visite [Google](https://google.com) e [GitHub](https://github.com)"
            Retorna: [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        """
        # Padrão regex para encontrar links no formato [texto do link](url)
        # Exclui links de imagem que começam com !
        pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        
        # Encontra todas as ocorrências do padrão no texto
        matches = re.findall(pattern, text)
        
        # Retorna a lista de tuplas (texto_do_link, url)
        return matches
    
    @staticmethod
    def split_nodes_image(old_nodes):
        """
        Processa nós de texto para identificar marcadores de imagem no formato Markdown ![alt](url)
        e convertê-los em nós do tipo IMAGE.
        
        Args:
            old_nodes: Lista de TextNode a ser processada
        
        Returns:
            Uma nova lista de TextNode com os marcadores de imagem convertidos para nós do tipo IMAGE
        """
        new_nodes = []
        
        for old_node in old_nodes:
            # Só processamos nós do tipo TEXT
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            # Extraímos as imagens do texto
            images = TextNode.extract_markdown_images(old_node.text)
            
            # Se não há imagens, mantemos o nó original
            if not images:
                new_nodes.append(old_node)
                continue
            
            # Processamos o texto para substituir as imagens por nós apropriados
            remaining_text = old_node.text
            
            for alt_text, url in images:
                # Encontramos a posição da imagem no texto
                image_marker = f"![{alt_text}]({url})"
                parts = remaining_text.split(image_marker, 1)
                
                # Adicionamos o texto antes da imagem, se houver
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                # Adicionamos a imagem como um nó IMAGE
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                
                # Atualizamos o texto restante
                remaining_text = parts[1] if len(parts) > 1 else ""
            
            # Adicionamos o texto restante, se houver
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        
        return new_nodes
    
    @staticmethod
    def split_nodes_link(old_nodes):
        """
        Processa nós de texto para identificar marcadores de link no formato Markdown [text](url)
        e convertê-los em nós do tipo LINK.
        
        Args:
            old_nodes: Lista de TextNode a ser processada
        
        Returns:
            Uma nova lista de TextNode com os marcadores de link convertidos para nós do tipo LINK
        """
        new_nodes = []
        
        for old_node in old_nodes:
            # Só processamos nós do tipo TEXT
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            # Extraímos os links do texto
            links = TextNode.extract_markdown_links(old_node.text)
            
            # Se não há links, mantemos o nó original
            if not links:
                new_nodes.append(old_node)
                continue
            
            # Processamos o texto para substituir os links por nós apropriados
            remaining_text = old_node.text
            
            for link_text, url in links:
                # Encontramos a posição do link no texto
                link_marker = f"[{link_text}]({url})"
                parts = remaining_text.split(link_marker, 1)
                
                # Adicionamos o texto antes do link, se houver
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                # Adicionamos o link como um nó LINK
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                
                # Atualizamos o texto restante
                remaining_text = parts[1] if len(parts) > 1 else ""
            
            # Adicionamos o texto restante, se houver
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        
        return new_nodes
    
    @staticmethod
    def text_to_textnodes(text):
        """
        Transforma um texto em Markdown em uma lista de TextNode,
        processando delimitadores, links e imagens.
        
        Args:
            text: String contendo o texto em formato Markdown
        
        Returns:
            Uma lista de TextNode representando o texto processado
        """
        # Começamos com um único nó de texto
        nodes = [TextNode(text, TextType.TEXT)]
        
        # Processamos os delimitadores para texto em negrito
        try:
            nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        except ValueError:
            # Se não houver delimitadores de negrito, continuamos com os nós atuais
            pass
        
        # Processamos os delimitadores para texto em itálico
        try:
            nodes = TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        except ValueError:
            # Se não houver delimitadores de itálico, continuamos com os nós atuais
            pass
        
        # Processamos os delimitadores para código
        try:
            nodes = TextNode.split_nodes_delimiter(nodes, "`", TextType.CODE)
        except ValueError:
            # Se não houver delimitadores de código, continuamos com os nós atuais
            pass
        
        # Processamos imagens
        nodes = TextNode.split_nodes_image(nodes)
        
        # Processamos links
        nodes = TextNode.split_nodes_link(nodes)
        
        return nodes
    
    