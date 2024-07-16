import os
import shutil
import re
import utils

def clear_destination(destination):
    if os.path.exists(destination) == False:
        raise ValueError("Destination Directory does not exist")
    else:
        objects = os.listdir(destination)
        for obj in objects:
            obj_path = os.path.join(destination, obj)
            if os.path.isfile(obj_path):
                os.remove(obj_path)
                print(f'Removed file: {obj_path}')
            else:
                shutil.rmtree(obj_path)
                print(f'Removed Directory: {obj_path}')
            
def copy_source_to_destination(source, destination):
    for obj in os.listdir(source):
        src_path = os.path.join(source, obj)
        dest_path = os.path.join(destination, obj)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f'Copied file: {obj} to {dest_path}')
        elif os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            copy_source_to_destination(src_path, dest_path)
            print(f'Copied directory: {obj} to {dest_path}')

def clear_and_copy_source_to_destination(source, destination):
    clear_destination(destination)
    copy_source_to_destination(source, destination)


def extract_title(markdown):
    lines = markdown.split('\n')
    if lines[0].strip().startswith('#'):
        stripped = lines[0].lstrip('#').strip()
        return stripped
    else:
        print(f'The expected header line is: {lines[0]}')
        raise Exception("No header on md file")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as file_object, open(template_path) as template_object:
        markdown = file_object.read()
        title = extract_title(markdown)
        template = template_object.read()
        content_nodes = utils.markdown_to_html_node(markdown)
        content = content_nodes.to_html()
        filled_content = template.replace('{{ Title }}', title).replace('{{ Content }}', content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(filled_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Iterate through all entries in the content directory
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(entry_path):
            # If it's a file, check if it's a markdown file
            if entry.endswith('.md'):
                # Generate the corresponding HTML file path
                html_file = entry[:-3] + '.html'  # Replace .md with .html
                dest_path = os.path.join(dest_dir_path, html_file)
                
                # Generate the page
                generate_page(entry_path, template_path, dest_path)
                print(f"Generated: {dest_path}")
        
        elif os.path.isdir(entry_path):
            # If it's a directory, recursively process it
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(entry_path, template_path, new_dest_dir)





def main():
    static = '/home/rob/workspace/github.com/Ephi/static_site_gen/static'
    public_dir = '/home/rob/workspace/github.com/Ephi/static_site_gen/public'
    content_dir = '/home/rob/workspace/github.com/Ephi/static_site_gen/content'
    template = '/home/rob/workspace/github.com/Ephi/static_site_gen/template.html'
    clear_and_copy_source_to_destination(static, public_dir)
    generate_pages_recursive(content_dir, template, public_dir)



if __name__ == "__main__":
    main()
