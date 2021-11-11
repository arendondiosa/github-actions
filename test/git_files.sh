#!/usr/bin/env bash

target_branch="staging"
output_file="out.txt"

while getopts b:f: flag
do
    case "${flag}" in
        b) target_branch=${OPTARG};;
        f) output_file=${OPTARG};;
    esac
done

git branch $target_branch origin/$target_branch # Clone the branch
git fetch origin $target_branch:$target_branch  # Update the branch with latest changes

git diff --name-only $target_branch > $output_file 
git diff --name-only $target_branch migrations/ > migrations.txt
