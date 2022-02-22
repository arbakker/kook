#!/usr/bin/env bash
set -eu
script_path=`realpath $0`
script_dir=`dirname $script_path`
echo "RUNNING: ${0}"
output_dir="${script_dir}/../data/output"
webapp_dir="${script_dir}/../webapp"

if [[ ! -d "$output_dir" ]];then
    echo "ERROR: ${output_dir} does not exist, cannot copy recipes"
    exit 1
fi

rm -f "${webapp_dir}/src/assets/recipes.json"
jq "[.[] | {\"title\": .title,\"subtitle\": .subtitle,\"slug\": .slug}]" \
    < "${output_dir}/recipes.json" \
    > "${webapp_dir}/src/assets/recipes.json"

rm -rf "${webapp_dir}/public/recipes/"
mkdir -p "${webapp_dir}/public/recipes/"
rsync -avq "${output_dir}/" "${webapp_dir}/public/recipes/" --exclude=recipes.json 