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
  cp -R mh "$ABLETON_MRS/APC_mini_mh"
  cp -R mle "$ABLETON_MRS/APC_mini_mle"
  cp -R plus "$ABLETON_MRS/APC_mini_plus"
  cp -R jojo "$ABLETON_MRS/APC_mini_jojo"

  echo "Installation done."
fi

