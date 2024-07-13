from leafnode import LeafNode
from textnode import TextNode
import re

TEXT_TYPES = {
    'text_type_text' : 'text',
    'text_type_bold' : 'bold',
    'text_type_italic' : 'italic',
    'text_type_code' : 'code',
    'text_type_link' : 'link',
    'text_type_image' : 'image'
}

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case 'text':
            return LeafNode(text_node.value, None, None)
        case 'bold':
            return LeafNode(text_node.value, None, 'b')
        case 'italic':
            return LeafNode(text_node.value, None, 'i')
        case 'code':
            return LeafNode(text_node.value, None, 'code')
        case 'link':
            props = { 'href' : text_node.url}
            return LeafNode(text_node.value, props, 'a')
        case 'image':
            props = {
                'src' : text_node.url,
                'alt' : None
            }
            return LeafNode('', props, 'img')

    raise Exception("Unhandled conversion of text_node text_type")


# Only for code, bold, italic text
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    processed_nodes = []
    for node in old_nodes:
        if node.text_type != 'text':
            processed_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) <= 1:
                processed_nodes.append(node)
            else:
                processed_substrings = []
                if len(split_text) % 2 == 0:
                    raise Exception("Even # of elements post-split, no matching delimiter found")
                for i in range (0, len(split_text)):
                    if i % 2 == 0:
                        if split_text[i]:  # Only create text nodes for non-empty strings
                            processed_nodes.append(TextNode(split_text[i], "text"))
                    else:
                        content = split_text[i] if delimiter == '`' else split_text[i].strip()
                        if content or delimiter == '`':
                            processed_nodes.append(TextNode(content, text_type))
                        # processed_nodes.append(TextNode(split_text[i].strip(), text_type))

                    #     if split_text[i] != "":
                    #         new_node = TextNode(split_text[i], "text")
                    #         processed_substrings.append(new_node)
                    # else:
                    #     new_node = TextNode(split_text[i], text_type)
                    #     processed_substrings.append(new_node)
                # processed_nodes.extend(processed_substrings)

    return processed_nodes

# Extract Images
def extract_markdown_images(text):
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)' ,text)
    return matches

# Extract links
def extract_markdown_links(text):
    matches = re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)
    return matches

def split_nodes_images(old_nodes):
    processed_nodes = []
    for node in old_nodes:
        if node.text_type != 'text':
            processed_nodes.append(node)
        else:
            img_text: list = extract_markdown_images(node.text)
            if len(img_text) == 0:
                processed_nodes.append(node)
            else:
                split_text = [node.text]
                for alt_text, url in img_text:
                    img_markdown = f'![{alt_text}]({url})'
                    new_split = []
                    for part in split_text:
                        if img_markdown not in part:
                            new_split.append(part)
                        else:
                            before, after = part.split(img_markdown, 1)
                            new_split.extend([before, '', after])
                    split_text = new_split
                img_index = 0
                for i in range(0, len(split_text)):
                    if i % 2 == 0:
                        node = TextNode(split_text[i], "text")
                        processed_nodes.append(node)
                    else:
                        alt_text, url = img_text[img_index]
                        alt_text = alt_text.strip()  # This removes leading and trailing whitespace
                        node = TextNode(alt_text, "image", url)
                        processed_nodes.append(node)
                        img_index += 1
                        # node = TextNode(img_text[img_index][0], "image", img_text[img_index][1])
                        # processed_nodes.append(node)
                        # img_index += 1
    return processed_nodes


def split_nodes_links(old_nodes):
    processed_nodes = []
    for node in old_nodes:
        if node.text_type != 'text':
            processed_nodes.append(node)
        else:
            link_text: list = extract_markdown_links(node.text)
            if len(link_text) == 0:
                processed_nodes.append(node)
            else:
                split_text = [node.text]
                for title, url in link_text:
                    link_markdown = f'[{title}]({url})'
                    new_split = []
                    for part in split_text:
                        if link_markdown not in part:
                            new_split.append(part)
                        else:
                            before, after = part.split(link_markdown, 1)
                            new_split.extend([before, '', after])
                    split_text = new_split
                link_index = 0
                for i in range(0, len(split_text)):
                    if i % 2 == 0:
                        node = TextNode(split_text[i], "text")
                        processed_nodes.append(node)
                    else:
                        text, url = link_text[link_index]
                        text = text.strip()  # This removes leading and trailing whitespace
                        node = TextNode(text, "link", url)
                        processed_nodes.append(node)
                        link_index += 1

                        # node = TextNode(link_text[link_index][0], "link", link_text[link_index][1])
                        # processed_nodes.append(node)
                        # link_index += 1
    return processed_nodes

def text_to_text_nodes(text):
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped:
            blocks.append(stripped)
    return blocks

def block_to_block_type(markdown_block):
    match markdown_block[0]:
        case '#':
            heading_level = min(len(markdown_block) - len(markdown_block.lstrip('#')), 6)
            return f'H{heading_level}'
        case '`':
            if markdown_block.startswith('```'):
                if markdown_block.endswith('```') and len(markdown_block) > 6:
                    return 'code'
                else:
                    raise ValueError("Code block must start and end with ``` and contain content")
        case '>':
            return 'quote'
        case '-' | '*':
            return 'unordered_list'
        case _:
            if markdown_block[0].isdigit() and markdown_block[1] == '.':
                return f'ordered_list_{markdown_block[0]}'
            else:
                return 'paragraph'





