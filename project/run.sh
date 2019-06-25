#!/bin/bash

cd wiki_processor
./download_wikipedia.sh &
./download_entity_vector.sh &
wait

./extract.sh
./fix_txt_format_entvec.sh

cd ../train
python3 train.py

