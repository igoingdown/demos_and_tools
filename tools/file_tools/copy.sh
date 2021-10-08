#!/bin/bash

project_path="${HOME}/a"
new_project_path="${HOME}/b"

ls ${project_path} | grep -v "go.mod" | grep -v "go.sum" | xargs -0 > xxx

input="${new_project_path}/xxx"
while IFS= read -r line
do
  cp -a "${project_path}/${line}" $new_project_path/
done < "$input"


