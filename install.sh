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
  rm -rf "$ABLETON_MRS/APC_mini_$project"
  cp -r "$project/" "$ABLETON_MRS/APC_mini_$project/"
done

echo "Installation done."

