#!/usr/bin/env bash

set -o errexit -o nounset

ABLETON_HOME="/Applications/Ableton Live 10 Lite.app"
if [ -e "$ABLETON_HOME" ]
then
  echo "..."
else
  echo "$ABLETON_HOME does not exist."
  exit
fi

ABLETON_MRS="$ABLETON_HOME/Contents/App-Resources/MIDI Remote Scripts"

if [ -e "$ABLETON_MRS" ]
then

  rm -rf "$ABLETON_MRS/APC_mini_mh/"
  rm -rf "$ABLETON_MRS/APC_mini_mle/"
  rm -rf "$ABLETON_MRS/APC_mini_plus/"
  rm -rf "$ABLETON_MRS/APC_mini_jojo/"

  cp -r mh/ "$ABLETON_MRS/APC_mini_mh/"
  cp -r mle/ "$ABLETON_MRS/APC_mini_mle/"
  cp -r plus/ "$ABLETON_MRS/APC_mini_plus/"
  cp -r jojo/ "$ABLETON_MRS/APC_mini_jojo/"

  echo "Installation done."
fi

