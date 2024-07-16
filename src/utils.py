from leafnode import LeafNode
from textnode import TextNode
from htmlnode import HTMLNode
from parentnode import ParentNode
import re

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
                    print(f'The culprit is: {split_text}')
                    raise Exception("Even # of elements post-split, no matching delimiter found")
                for i in range (0, len(split_text)):
                    if i % 2 == 0:
                        if split_text[i]:  # Only create text nodes for non-empty strings
                            processed_nodes.append(TextNode(split_text[i], "text"))
                    else:
                        content = split_text[i] if delimiter == '`' else split_text[i].strip()
                        if content or delimiter == '`':
                            processed_nodes.append(TextNode(content, text_type))
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
    current_block = []
    lines = markdown.split('\n')
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if i == 0 and stripped:  # First non-empty line starts a block
            current_block.append(line)
        elif stripped == '' and current_block:  # Empty line ends a block
            blocks.append('\n'.join(current_block))
            current_block = []
        elif stripped:  # Non-empty line continues or starts a block
            current_block.append(line)
    
    # Add the last block if there's any content left
    if current_block:
        blocks.append('\n'.join(current_block))
    
    return blocks 


def block_to_block_type(markdown_block):
    match markdown_block[0]:
        # Headings
        case '#':
            heading_level = min(len(markdown_block) - len(markdown_block.lstrip('#')), 6)
            return f'H{heading_level}'
        # Code blocks
        case '`':
            if markdown_block.startswith('```'):
                if markdown_block.endswith('```') and len(markdown_block) > 6:
                    return 'code'
                else:
                    raise ValueError("Code block must start and end with ``` and contain content")
        # Quote blocks
        case '>':
            return 'quote'
        # Unordered lists
        case '-' | '*':
            if markdown_block[1].isspace():
                return 'unordered_list'
            else:
                return 'paragraph'
        # Ordered lists and paragraphs
        case _:
            if markdown_block[0].isdigit() and markdown_block[1] == '.':
                return f'ordered_list'
            else:
                return 'paragraph'

def markdown_to_html_node(markdown):
    block_types_with_nesting = {'unordered_list', 'ordered_list'}
    md_blocks = markdown_to_blocks(markdown)
    parents = []

    for block in md_blocks:
        block_type = block_to_block_type(block)
        tag = tag_from_block_type(block_type)

        # parent_node = ParentNode(None, opening_tag, None)
        children = []

        if block_type not in block_types_with_nesting:
            text_nodes = parse_block_by_block_type(block, block_type)
            for text_node in text_nodes:
                children.append(text_node_to_leaf_node(text_node))
        elif block_type == 'code':
            text_node = parse_block_by_block_type(block, block_type)
            code_parent = ParentNode(text_node, 'code', None)
            children.append(code_parent)
        else:
            list_of_text_nodes = parse_block_by_block_type(block, block_type)
            for text_nodes in list_of_text_nodes:
                inline_nodes = []
                for text_node in text_nodes:
                    inline_nodes.append(text_node_to_leaf_node(text_node))
                list_item = ParentNode(inline_nodes, 'li', None)
                children.append(list_item)

        parent_node = ParentNode(children, tag, None)
        parents.append(parent_node)

    div_parent = ParentNode(parents, 'div', None)
    return div_parent


def tag_from_block_type(block_type):
    if block_type[0] == 'H':
        return f'h{block_type[1]}'
    elif block_type == 'paragraph':
        return 'p'
    elif block_type == 'code':
        return 'pre'
    elif block_type == 'quote':
        return 'blockquote'
    elif block_type == 'unordered_list':
        return 'ul'
    elif block_type == 'ordered_list':
        return 'ol'
        
def parse_block_by_block_type(block, block_type):
    if block_type.startswith('H'):
        stripped = block.lstrip('#')
        stripped2 = stripped.strip()
        return [TextNode(stripped2, 'text', None)]
    elif block_type == 'paragraph':
        nodes = text_to_text_nodes(block)
        return nodes
    elif block_type == 'code':
        content = block.strip('`')
        return [TextNode(content, 'code')]
    elif block_type == 'quote':
        # Split into lines, remove '>' from each line, and reassemble
        lines = block.split('\n')
        stripped_lines = [line.lstrip('>').strip() for line in lines]
        cleaned_content = '\n'.join(stripped_lines)
        return [TextNode(cleaned_content, 'text')]
    elif block_type == 'unordered_list':
        list = []
        items = block.split('\n')
        for item in items:
            stripped = item.lstrip('*')
            stripped2 = stripped.lstrip('-')
            stripped3 = stripped2.strip()
            inline_nodes = text_to_text_nodes(stripped3)
            list.append(inline_nodes)
        return list
    elif block_type == 'ordered_list':
        list = []
        items = block.split('\n')
        for item in items:
            without_number = re.sub(r'^\d+\.', '', item)
            cleaned = without_number.strip()
            inline_nodes = text_to_text_nodes(cleaned)
            list.append(inline_nodes)
        return list
    
def text_node_to_leaf_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(text_node.text, None, None)
    elif text_node.text_type == "bold":
        return LeafNode(text_node.text, None, "b")
    elif text_node.text_type == "italic":
        return LeafNode(text_node.text, None, "i")
    elif text_node.text_type == "code":
        return LeafNode(text_node.text, None, "code")
    elif text_node.text_type == "link":
        return LeafNode(text_node.text, {"href": text_node.url}, "a")
    elif text_node.text_type == "image":
        return LeafNode("", {"src": text_node.url, "alt": text_node.text}, "img")
    elif text_node.text_type == "quote":
        return LeafNode("text_node.text", None, "quote")
    else:
        print(f'The culprit is {text_node.text}, of type {text_node.text_type}')
        raise ValueError(f"Invalid text type: {text_node.text_type}")
