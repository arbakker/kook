#!/usr/bin/env bash
echo "RUNNING: ${0}"
script_path=`realpath $0`
script_dir=`dirname $script_path`
recipes_dir="${script_dir}/../webapp/public/recipes"
rm -f $recipes_dir/*.json
recipe_index="${script_dir}/../webapp/src/assets/recipes.json"
rm -f "$recipe_index"
processed_index="${script_dir}/../kook/output/processed-index.json"
rm -f "$processed_index"