# KOOK

## Description

Repository containing code to extract recipes from printed recipe cards. Repository contains the following:

- `kook/` - code to extract recipes from printed recipes cards

    Run with: `python3 kook/main.py -o data/output/recipes.json`

- `webapp/` - webapp code

    Run with:

    ```sh
    npm install # Install dependencies
    npm run serve # Compiles and hot-reloads for development
    npm run build # Compiles and minifies for production
    npm run lint # Lints and fixes files
    ```

- `scripts/` - Bash utility scripts; for copying over recipes and scans
    - `copy-recipe-json.sh` - copy generated recipe json files to webapp
    - `refresh-scans.sh` - refresh scans based on scans in `data/input/original-scans` folder
    - `copy-recipe-json.sh` - update `original-scans` based latest `kook.zip` file in downloads dir, then runs `refresh-scans.sh`


## Requirements

The `kook/` code base requires installation of:

```
tesseract 4.1.1
 leptonica-1.79.0
...
```
  
## TODO

- [x] add fuzzy search title/subtitle to frontpage
- [x] add home button from recipe page
- [x] sort steps on order title
- [x] replace comma step title with nr.
- [x] order recipes on title alpahbetically
- [x] add copy to clipboard on ingredients list
- [X] require password before accessing page
- [ ] add check to verify if recipes are converted correctly, skip failing recipes
- [ ] add keywords/tags/to recipes
- [ ] generate index specifically for search
- [ ] remove allcaps phrases like  VREE from steps
