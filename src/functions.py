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
    print("Lines:", lines)

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

markdown = " this - is a heading."

markdown2 = """
1. this is a quote
2. also a quote
3. another quote
"""

blocktype = block_to_blocktype(markdown2)

print(blocktype)