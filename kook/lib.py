import subprocess
import shutil
from pathlib import Path
import os
import re
import itertools
from slugify import slugify

def get_project_kook():
    return Path(__file__).parent

def get_project_root():
    return Path(__file__).parent.parent

def ocr_image_front(image):
    basename = Path(image).stem
    proj_root = get_project_root()
    image_dir = os.path.dirname(image)
    uzn_path = f"{image_dir}/{basename}.uzn"
    shutil.copy(f"{proj_root}/kook/uzn-template", uzn_path)
    result = subprocess.run([
        'tesseract',
        '-l',
        'nld',
        '--psm',
        '4',
        image,
        'stdout',
        '-c',
        'debug_file=/dev/null'
    ], stdout=subprocess.PIPE)
    os.remove(uzn_path)
    string_result=result.stdout.decode('utf-8')
    string_result = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', string_result)
    return re.sub(r'[\u201c-\u201d]', "\"", string_result)

def ocr_image(image):
    result = subprocess.run([
        'tesseract',
        '-l',
        'nld',
        image,
        'stdout',
        '-c',
        'debug_file=/dev/null'
    ], stdout=subprocess.PIPE)
    string_result=result.stdout.decode('utf-8')
    string_result = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', string_result)
    return re.sub(r'[\u201c-\u201d]', "\"", string_result)
    

def count_until_first_empty_line(text):
    i=0
    for line in text.split('\n'):
        if line == '':
            break
        i+=1
    return i
        
def get_titles(text):
    title_text = "\n".join(list(filter(lambda x:  x.strip() != "", text.split("\n"))))
    line_nr = get_line_nr_first_match(title_text, r'(?i).*2\s?(?:persone(?:n|r)|porties)')[0] # expect exactly one match - TODO: if not processingerror should be thrown and recipe should be skipped, 
    line_nr_title = line_nr -2
    line_nr_subtitle = line_nr-1
    title=title_text.split("\n")[line_nr_title]
    subtitle=title_text.split("\n")[line_nr_subtitle]
    description = " ".join(title_text.split("\n")[line_nr+1:])
    slug = slugify(title)
    return title,subtitle,description,slug

 

def get_between_lines(text, start, end):
    f = text.split("\n")
    it = itertools.dropwhile(lambda line: line.strip() != start, f)
    it = itertools.islice(it, 1, None)
    it = itertools.takewhile(lambda line: line.strip() != end, it)
    return '\n'.join(it)

def regex_sub_until(text, pattern):
    while True: # some lines have multiple weird chars ending
        prev_text = text
        text = re.sub(pattern, "", text)
        if prev_text == text:
            break
    return text

def get_ingredients(text):
    ingredients=[]
    for line in text.split("\n"):
        line=line.strip()
        line = regex_sub_until(line, r"^(‚|,|-|_|\*|…|\+)").strip() # note: comma in regex is U+201a
        line = regex_sub_until(line, r'(?:[0-9]+|!|\?|\u2019|\||\:)$').strip()
        line = re.sub(r'^\s*Tui\s*$', "1 ui", line).strip()
        line = re.sub(r'^\s?([0-9]+)9', r'\1g', line).strip() # assuming no ingredients en
        line = re.sub(r'(?i)^([0-9]+)x\s?', r'\1 ', line).strip()
        line = line.lower()
        if line == "":
            continue
        ingredients.append(line)
    return ingredients

def get_line_nr_first_match(text, pattern):
    result=-1
    result = []
    for number, line in enumerate(text.split("\n")):
        regex = re.compile(pattern)
        match = regex.match(line)
        if match != None:
            result.append(number)
    return result

# uppercase 2nd match group (out of 3)
def replfunc(m):
     return m.groups()[0]+m.groups()[1].upper()+m.groups()[2]

def get_recipe_steps(text):
    pattern = r"^[0-9](?:\.|,)\s.*$"
    steps_start_line_nr=get_line_nr_first_match(text, pattern)
    steps = []    
    for i, line_nr in enumerate(steps_start_line_nr):
        if i == len(steps_start_line_nr)-1:
            step_result = text.split("\n")[line_nr:]
            # TODO: strip "Vragen over de bereiding of over het recept?"

        else:
            end_line_nr=steps_start_line_nr[i+1]
            step_result = text.split("\n")[line_nr:end_line_nr]
        step_title = " ".join(step_result[:1]).strip()
        step_title = re.sub('^([0-9]),(.*)', r'\1.\2', step_title)
        step_title = re.sub('^([0-9]\.\s?)([a-z])(.*)',replfunc,step_title)
        step_description = " ".join(step_result[1:]).strip()
        
        step_description = re.split(r'Je kunt je in je online account', step_description, maxsplit=1)[0].strip()
        
        step_description = re.split(r'(?:Vragen over de bereiding)? of over het recept?', step_description, maxsplit=1)[0].strip()

        step = {
            "title": step_title,
            "description": step_description
        }
        steps.append(step)
    steps = sorted(steps, key=lambda d: d['title'])
    return steps

def get_all_ingredients(text):
    ingredients_text=get_between_lines(text, "Wat je van ons krijgt", "Wat je thuis nodig hebt")
    ingredients_home_text=get_between_lines(text, "Wat je thuis nodig hebt","Kookgerei")
    ingredients=get_ingredients(ingredients_text)
    ingredients_home=get_ingredients(ingredients_home_text)
    ingredients = ingredients + ingredients_home
    return ingredients


def process_recipe_image(images):
    front_image = images[0]
    back_image = images[1]
    # ocr images
    front_text=ocr_image_front(front_image)
    back_text=ocr_image(back_image)
    # process ocr output
    title,subtitle,description,slug=get_titles(front_text)
    ingredients = get_all_ingredients(back_text)
    steps = get_recipe_steps(back_text)
    recipe = {}
    recipe["front_scan"] = front_image
    recipe["back_scan"] = back_image
    recipe["title"] = title
    recipe["subtitle"] = subtitle
    recipe["description"] = description
    recipe["slug"] = slug
    recipe["ingredients"] = ingredients
    recipe["steps"] = steps
    return recipe

def process_scans(files_to_process):
    recipes = []
    for i in range(0,len(files_to_process)-1,2):
        front_scan = files_to_process[i]
        back_scan = files_to_process[i+1]
        print(f"front_scan: {front_scan}")
        print(f"back_scan: {back_scan}")
        recipe = process_recipe_image((front_scan, back_scan))
        recipes.append(recipe)
    recipes.sort(key=lambda x:x["title"])
    return recipes

root_dir = get_project_root()
SCAN_DIR=f"{root_dir}/data/input/scans"



# back_text=ocr_image("./scans/2022-02-19 17.38.59.jpg")
# print(back_text)
# steps = get_recipe_steps(back_text)
# print(json.dumps(steps, indent=4))
