import os
import shutil

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
        raise Exception("No header on md file")



def main():
    source = '/home/rob/workspace/github.com/Ephi/static_site_gen/static'
    destination = '/home/rob/workspace/github.com/Ephi/static_site_gen/public'
    clear_and_copy_source_to_destination(source, destination)




main()