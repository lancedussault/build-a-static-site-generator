from htmlnode import ParentNode
from textnode import text_node_to_html_node

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
        else:
            remaining_text = old_node.text
            for image_text, image_url in images:
                parts = remaining_text.split(f"![{image_text}]({image_url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], text_type_text))
                new_nodes.append(TextNode(image_text, text_type_image, image_url))
                if len(parts) > 1:
                    remaining_text = parts[1]
                else:
                    remaining_text = ""
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
        else:
            remaining_text = old_node.text
            for link_text, link_url in links:
                parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], text_type_text))
                new_nodes.append(TextNode(link_text, text_type_link, link_url))
                if len(parts) > 1:
                    remaining_text = parts[1]
                else:
                    remaining_text = ""
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):

    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    blocks_list = []
    current_block = ""
    for line in markdown.split("\n"):
        if line != "":
            if current_block == "":
                current_block += line.strip()
            else: 
                current_block += "\n" + line.strip()
        if line == "" and current_block != "":
             blocks_list.append(current_block)
             current_block = ""
    if current_block != "":
        blocks_list.append(current_block)
    return blocks_list

def block_to_blocktype(markdown_block):
    if markdown_block.startswith(("#", "##", "###", "####", "#####", "######")):
        return "heading"
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return "code"
    lines = markdown_block.split("\n")
    if all(line.strip().startswith('>') for line in lines if line.strip()):
        return "quote"
    if all(line.strip().startswith('* ') or line.startswith('- ') for line in lines if line.strip()):
        return "unordered_list"
    if is_ordered_list(lines):
        return "ordered_list"
    return "paragraph"
    
def is_ordered_list(lines):
    if not lines:
        return False
    for i,line in enumerate(lines, start=1):
        if not line.strip().startswith(f"{i}. "):
            return False
    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_blocktype(block)
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    if block_type == "heading":
        return heading_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    if block_type == "ordered_list":
        return olist_to_html_node(block)
    if block_type == "unordered_list":
        return ulist_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block: 
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError("Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""

print(markdown_to_html_node(markdown))

