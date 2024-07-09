from sitegen_utils import TEXT_TYPES

class TextNode:
    def __init__(self, text, text_type, url=None):
        if text_type not in TEXT_TYPES.values():
            raise ValueError("text_type not valid in TEXT_TYPES")

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False


    def __repr__(self):
        return f"Textnode({self.text}, {self.text_type}, {self.url})"