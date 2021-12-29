#!/usr/bin/env bash

set -o errexit -o nounset

PROJECTS=('mle')

ABLETON_HOME="$HOME/Music/Ableton/User Library"
ABLETON_MRS="$ABLETON_HOME/Remote Scripts"
if [ -e "$ABLETON_HOME" ]
then
  echo "..."
else
  echo "$ABLETON_HOME does not exist."
  exit
fi

if [ -e "$ABLETON_MRS" ]
then
  echo "..."
else
  mkdir "$ABLETON_MRS"
fi

for project in "${PROJECTS[@]}"
do
  rm -rf "$project/__pycache__"
  rm -rf "compiled/$project"
  mkdir "compiled/$project"
  python -m compileall "$project"

  if [ -e "$project/__pycache" ]
  then
    for filename in $project/__pycache__/*.pyc; do
      filename_name=$(basename -- "${filename%%.*}")
      cp "$filename" "./compiled/$project/$filename_name.pyc"
      #uncompyle6 "./compiled/$project/$filename_name.pyc" > "./compiled/$project/$filename_name.py"
    done
  fi

  rm -rf "$ABLETON_MRS/APC_mini_$project"
  # cp -r "compiled/$project/" "$ABLETON_MRS/APC_mini_$project/"
  cp -r "$project/" "$ABLETON_MRS/APC_mini_$project/"

done

echo "Installation done."

