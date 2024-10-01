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
