# KOOK

## Description

Repository containing code to extract recipes from printed recipe cards. Repository contains the following:

- `kook/` - code to extract recipes from printed recipes cards
    - reads scans directly from `Apps/arbakker-kook` directory
    - requires `kook/.env` file with `ACCESS_TOKEN` set 

    Run with: `python3 kook/main.py`

- `webapp/` - webapp code

    Run with:

    ```sh
    npm install # Install dependencies
    npm run serve # Compiles and hot-reloads for development
    npm run build # Compiles and minifies for production
    npm run lint # Lints and fixes files
    ```

- `scripts/` - Bash utility scripts; for copying over recipes and scans
    - `clear-processed-recipes.sh` - remove processed recipe index and recipe json files from webapp, so next run of `kook/main.py` reprocesses all recipes


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
- [x] require password before accessing page
- [x] read scans directly from dropbox
- [x] process only unprocessed recipes/scans
- [x] generate index specifically for search
- [ ] run python processing from Docker image
  - [ ] run python processing with GH Actions
    - [ ] GH Action processing after files is uploaded to dropbox folder
      - [ ] Redeploy webapp after running gh action processing
- [ ] add check to verify if recipes are converted correctly, skip failing recipes
- [ ] add keywords/tags/to recipes
- [ ] remove allcaps phrases like  VREE from steps

