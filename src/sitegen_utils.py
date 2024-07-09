from leafnode import LeafNode

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


