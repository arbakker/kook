import json
import os
import argparse
from lib import process_scans
import glob
from pathlib import Path

def remove_images(r):
    r.pop('front_scan', None)
    r.pop('back_scan', None)
    return r

    

def main(output_filepath):
    dirname = os.path.dirname(output_filepath)

    Path(dirname).mkdir(parents=True, exist_ok=True)


    files_to_delete = glob.glob(f"{dirname}/*")
    for f in files_to_delete:
        os.remove(f)
    recipes = process_scans()
    recipes = list(map(remove_images, recipes))
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)
    for recipe in recipes:
        slug = recipe["slug"]
        recipe.pop('slug', None)
        recipe_file_path = f"{dirname}/{slug}.json"
        with open(recipe_file_path, 'w', encoding='utf-8') as f:
            json.dump(recipe, f, ensure_ascii=False, indent=4)
            



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="JSON output file path", required=True)
    args = parser.parse_args()
    main(args.output)