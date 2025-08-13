#!/bin/bash

function create_symlinks() {
  FOLDERS=("Documents" "Downloads" "Projects" "Pictures")

  cd
  for folder in "${FOLDERS[@]}"; do
    if [ -L "$folder" ]; then
      $(unlink ~/$folder)
    else
      $(rm -rf ~/$folder)
    fi

    $(ln -s /home/data/$folder)
  done
}

create_symlinks
