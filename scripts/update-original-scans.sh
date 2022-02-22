#!/usr/bin/env bash
echo "RUNNING: ${0}"
latest_zip=$(find ~/Downloads/ -name "kook*.zip" -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")
script_path=`realpath $0`
script_dir=`dirname $script_path`
orig_scans_dir="${script_dir}/../data/input/scans-originals"
rm -f $orig_scans_dir/*
unzip -o "$latest_zip" -d "$orig_scans_dir"
$script_dir/refresh-scans.sh
