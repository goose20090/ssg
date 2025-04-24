import shutil
import os

def copy_static_to_docs():

    # delete docs

    shutil.rmtree("./docs")

    # recreate public as empty folder

    os.mkdir("./docs")

    # copy across what exists in static to docs

    transfer_contents("./static", "./docs")

def transfer_contents(src, dest):

    if not os.path.exists(src):
        raise Exception("Bad path")

    contents = os.listdir(src)

    for item in contents:
        item_src_path = os.path.join(src, item)
        item_dest_path = os.path.join(dest, item)


        if os.path.isdir(item_src_path):
            os.mkdir(item_dest_path)
            transfer_contents(item_src_path, item_dest_path)
        else:
            shutil.copy(item_src_path, item_dest_path) 


