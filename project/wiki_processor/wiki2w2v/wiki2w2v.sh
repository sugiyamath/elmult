#!/bin/bash

git clone https://github.com/attardi/wikiextractor
cd wikiextractor
python3 WikiExtractor.py -o extracted_de ../../dumps/dewiki.xml.bz2
python3 WikiExtractor.py -o extracted_it ../../dumps/itwiki.xml.bz2
python3 WikiExtractor.py -o extracted_es ../../dumps/eswiki.xml.bz2
python3 WikiExtractor.py -o extracted_fr ../../dumps/frwiki.xml.bz2
python3 WikiExtractor.py -o extracted_en ../../dumps/enwiki.xml.bz2
cd ..

python3 dump2txt.py de &
python3 dump2txt.py it &
python3 dump2txt.py es &
python3 dump2txt.py fr &
python3 dump2txt.py en &

wait

python3 txt2model.py de
python3 txt2model.py it
python3 txt2model.py es
python3 txt2model.py fr
python3 txt2model.py en

mkdir tmp_data
mkdir w2v_models

mv *.txt tmp_data
mv word2vec* w2v_models
mv w2v_models ../data
echo "Done!"
