#!/usr/bin/env bash
script_path=`realpath $0`
script_dir=`dirname $script_path`
echo "RUNNING: ${0}"
input_dir="${script_dir}/../data/input"
scans_dir="${input_dir}/scans"
scans_orig_dir="${input_dir}/scans-originals"
rm -rf "$scans_dir"
cp -r "$scans_orig_dir" "$scans_dir"
mogrify  -bordercolor White -border 10x10 -resize 3400x $scans_dir/*.jpg
