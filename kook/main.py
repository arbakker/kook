import json
import os
import argparse
import subprocess
import glob
from typing import List
import uuid
from pathlib import Path
import dropbox
from dotenv import load_dotenv
from matplotlib.pyplot import sca
from lib import process_scans, get_project_kook, get_project_root

PROJ_ROOT = get_project_root()
PROJ_KOOK_DIR = get_project_kook()

if os.path.isfile(f"{PROJ_KOOK_DIR}/.env"):
    load_dotenv()
    print("INFO: reading vars from .env file")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    APP_KEY = os.getenv("APP_KEY")
else:
    print("INFO: reading vars from environment")
    REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
    APP_KEY = os.environ["APP_KEY"]

def remove_images(r):
    r.pop("front_scan", None)
    r.pop("back_scan", None)
    return r


def create_processed_index(r):
    return {
        os.path.basename(r["front_scan"]): r["slug"],
        os.path.basename(r["back_scan"]): r["slug"],
    }


def create_recipe_index(r):
    return {"title": r["title"], "subtitle": r["subtitle"], "slug": r["slug"]}

def list_files(scan_dir):
    scan_files = [glob.glob(f"{scan_dir}/*.{e}") for e in ['png', 'jpg']]
    scan_files = [item for sublist in scan_files for item in sublist]   
    # return [os.path.basename(x) for x in scan_files]
    return scan_files

def list_files_dropbox():
    with dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY) as dbx:
        # list files
        response = dbx.files_list_folder("")
        remote_scan_files = [os.path.basename(x.name) for x in response.entries]
        
        if (len(remote_scan_files)% 2) != 0:
            print(f"INFO: nr of files in dropbox folder is not even")
            return []
        return remote_scan_files

def download_files_dropbox(tmp_dir_path, to_process_files):
    Path(tmp_dir_path).mkdir(parents=True, exist_ok=True)

    with dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY) as dbx:
        for to_process_file in to_process_files:
            local_dl_path = f"{tmp_dir_path}/{to_process_file}"
            remote_dl_path = f"/{to_process_file}"
            print(f"INFO: downloading remote file {remote_dl_path} to {local_dl_path}")
            dbx.files_download_to_file(local_dl_path, remote_dl_path)


def main(dropbox, scan_dir, processed_index_path, outputdir):
    

    if dropbox:
        scan_files = list_files_dropbox()
    else:
        scan_files = list_files(scan_dir)
    print(scan_files)
    extension =  os.path.splitext(scan_files[0])[1]
    # list processed index
    processed_index = {}
    if processed_index_path and os.path.isfile(processed_index_path):
        with open(processed_index_path) as json_file:
            processed_index = json.load(json_file)
    processed_files = processed_index.keys()
        # substract processed files from processed files
    to_process_files = list(set(scan_files) - set(processed_files))
    to_process_files.sort()
    if len(to_process_files) == 0:
        print(f"INFO: no new scans to process found")
        exit(0)
        # download files and preprocess files


    if dropbox:
        scan_dir_name = str(uuid.uuid4())
        scan_dir = f"/tmp/{scan_dir_name}"
        download_files_dropbox(scan_dir, to_process_files)

    print(f"INFO: preprocessing images in {scan_dir}")
    subprocess.run(f"rm -rf {scan_dir}.bak", shell=True)
    subprocess.run(f"cp -r {scan_dir} {scan_dir}.bak", shell=True)
    scan_dir = f"{scan_dir}.bak"
    print(f"mogrify -bordercolor White -border 10x10 -resize 3400x {scan_dir}/*{extension}")
    subprocess.run(
        f"mogrify -bordercolor White -border 10x10 -resize 3400x {scan_dir}/*{extension}",
        shell=True,
        stdout=subprocess.PIPE,
    )

    to_process_local_files = list_files(scan_dir)
    to_process_local_files.sort()
    recipes = process_scans(to_process_local_files)

    # create processed-index
    tmp_processed_index = list(map(create_processed_index, recipes))

    # merge processed_index file stored on dics, with the ones just processed
    for item in tmp_processed_index:
        processed_index = {**processed_index, **item}
    
    if processed_index_path:
        with open(processed_index_path, "w", encoding="utf-8") as f:
            json.dump(processed_index, f, ensure_ascii=False, indent=4)

    # create index file
    recipe_index = list(map(create_recipe_index, recipes))
    index_file_path = os.path.join(outputdir, "index.json")
    index_file_json = []
    if os.path.isfile(index_file_path):
        with open(index_file_path, "r", encoding="utf-8") as f:
            index_file_json = json.load(f)
    else:
        Path(os.path.dirname(index_file_path)).mkdir(parents=True, exist_ok=True)

    recipe_index = recipe_index + index_file_json
    recipe_index.sort(key=lambda x: x["title"])

    with open(index_file_path, "w", encoding="utf-8") as f:
        json.dump(recipe_index, f, ensure_ascii=False, indent=4)

    # create recipe files
    recipes = list(map(remove_images, recipes))
    for recipe in recipes:
        slug = recipe["slug"]
        recipe.pop("slug", None)
        recipe_file_path = f"{outputdir}/{slug}.json"
        Path(outputdir).mkdir(parents=True, exist_ok=True)
        with open(recipe_file_path, "w", encoding="utf-8") as f:
            json.dump(recipe, f, ensure_ascii=False, indent=4)
    subprocess.run(f"rm -rf {scan_dir}", shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--index", help="JSON index of already processed files", required=False)
    parser.add_argument("-s", "--scandir", help="Directory with scans to process (required when not reading from dropbox folder)", required=False)
    parser.add_argument("-o", "--outputdir", help="Output dir (for recipes and recipe index)", required=True)
    
    parser.add_argument('--dropbox', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    dropbox = True if args.dropbox else False
    index = args.index
    scandir = args.scandir
    outputdir = args.outputdir
    if not dropbox and (scandir is None):
        print("if --dropbox not set then --scandir is a required argument")
        exit(1)

    main(dropbox, scandir, index, outputdir)
