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
                        if split_text[i] != "":
                            new_node = TextNode(split_text[i], "text")
                            processed_substrings.append(new_node)
                    else:
                        new_node = TextNode(split_text[i], text_type)
                        processed_substrings.append(new_node)
                processed_nodes.extend(processed_substrings)

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
                        node = TextNode(img_text[img_index][0], "image", img_text[img_index][1])
                        processed_nodes.append(node)
                        img_index += 1
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
                        node = TextNode(link_text[link_index][0], "link", link_text[link_index][1])
                        processed_nodes.append(node)
                        link_index += 1
    return processed_nodes


                # processed_substrings = []
                # img_text_sequential = []
                # for i in range (0, len(img_text)):
                #     img_text_sequential.append(img_text[i][0])
                #     img_text_sequential.append(img_text[i][1])
                # split_text = node.text.split(f'![{}]')



            

#     pass

# def split_nodes_link(old_nodes):
#     pass



        
