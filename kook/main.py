import json
import os
import argparse
import subprocess
import glob
import uuid
from pathlib import Path
import dropbox
from dotenv import load_dotenv
from lib import process_scans, get_project_kook, get_project_root



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


def main():
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    APP_KEY = os.getenv("APP_KEY")

    with dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY) as dbx:
        proj_root = get_project_root()
        proj_kook_dir = get_project_kook()

        # list files
        response = dbx.files_list_folder("")
        remote_scan_files = [os.path.basename(x.name) for x in response.entries]

        # list processed index
        processed_index_path = f"{proj_kook_dir}/output/processed-index.json"
        processed_index = {}
        if os.path.isfile(processed_index_path):
            with open(processed_index_path) as json_file:
                processed_index = json.load(json_file)
        processed_files = processed_index.keys()
        # substract processed files from processed files
        to_process_files = list(set(remote_scan_files) - set(processed_files))
        to_process_files.sort()
        if len(to_process_files) == 0:
            print(f"INFO: no new scans to process found")
            exit(0)
        # download files and preprocess files

        tmp_dir_name = str(uuid.uuid4())
        tmp_dir_path = f"/tmp/{tmp_dir_name}"
        Path(tmp_dir_path).mkdir(parents=True, exist_ok=True)

        for to_process_file in to_process_files:
            local_dl_path = f"{tmp_dir_path}/{to_process_file}"
            remote_dl_path = f"/{to_process_file}"
            print(f"INFO: downloading remote file {remote_dl_path} to {local_dl_path}")
            dbx.files_download_to_file(local_dl_path, remote_dl_path)

        print(f"INFO: preprocessing images in {tmp_dir_path}")
        subprocess.run(
            f"cp -r {tmp_dir_path} {tmp_dir_path}.bak",
            shell=True
        )
        subprocess.run(
            f"mogrify  -bordercolor White -border 10x10 -resize 3400x {tmp_dir_path}/*.jpg",
            shell=True,
            stdout=subprocess.PIPE,
        )

        to_process_local_files = glob.glob(f"{tmp_dir_path}/*.jpg")
        to_process_local_files.sort()
        recipes = process_scans(to_process_local_files)
        
        # create processed-index
        tmp_processed_index = list(map(create_processed_index, recipes))

        # merge processed_index file stored on dics, with the ones just processed
        for item in tmp_processed_index:
            processed_index = {**processed_index, **item}
        with open(processed_index_path, "w", encoding="utf-8") as f:
            json.dump(processed_index, f, ensure_ascii=False, indent=4)

        # create index file
        recipe_index = list(map(create_recipe_index, recipes))
        index_file_path = f"{proj_root}/webapp/src/assets/recipes.json"
        index_file_json = []
        if os.path.isfile(index_file_path):
            with open(index_file_path, "r", encoding="utf-8") as f:
                index_file_json = json.load(f)

        recipe_index = recipe_index + index_file_json
        recipe_index.sort(key=lambda x:x["title"])
        with open(index_file_path, "w", encoding="utf-8") as f:
            json.dump(recipe_index, f, ensure_ascii=False, indent=4)

        # create recipe files
        recipes = list(map(remove_images, recipes))
        for recipe in recipes:
            slug = recipe["slug"]
            recipe.pop("slug", None)
            recipes_dir_path = f"{proj_root}/webapp/public/recipes"
            recipe_file_path = f"{recipes_dir_path}/{slug}.json"
            Path(recipes_dir_path).mkdir(parents=True, exist_ok=True)
            with open(recipe_file_path, "w", encoding="utf-8") as f:
                json.dump(recipe, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    # parser.add_argument("-o", "--output", help="JSON output file path", required=True)
    args = parser.parse_args()
    main()
