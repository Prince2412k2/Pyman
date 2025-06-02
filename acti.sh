#!/usr/bin/env bash

get_list() {
  ./list_env
}

menu() {
  echo "$1" | jq -r '.[] | keys[]' | gum choose
}

get_path() {
  echo "$1" | jq -r --arg key "$2" '.[] | select(has($key)) | .[$key]'
}

list=$(get_list)
choice=$(menu "$list")
p=$(get_path "$list" "$choice")

if [[ $choice == * ]]; then
  deactivate >/dev/null 2>&1
  conda deactivate >/dev/null 2>&1
  conda activate $(basename "$p")
else
  deactivate >/dev/null 2>&1
  conda deactivate >/dev/null 2>&1
  source "$p"/bin/activate
fi
