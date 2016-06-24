#!/bin/sh


cur_dir="$( dirname "$0" )"

echo $(echo "$(bash $cur_dir/random_word.sh 2 | perl -pe "s/\'|\n//g")" | tr '[:upper:]' '[:lower:]')
