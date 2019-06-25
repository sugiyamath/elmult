#!/bin/bash

#python3 wait_wget.py

python3 extract_mention.py dewiki.xml
python3 extract_mention.py itwiki.xml
python3 extract_mention.py eswiki.xml
python3 extract_mention.py frwiki.xml
python3 extract_mention.py enwiki.xml

python3 json2marisa.py de
python3 json2marisa.py it
python3 json2marisa.py es
python3 json2marisa.py fr
python3 json2marisa.py en

python3 extract_ELdata.py dewiki.xml &
python3 extract_ELdata.py itwiki.xml &
python3 extract_ELdata.py eswiki.xml &
python3 extract_ELdata.py frwiki.xml &
python3 extract_ELdata.py enwiki.xml &

wait

mkdir data
mkdir marisa_data
mkdir training_data
mkdir tmp_data
mv *.txt training_data
mv *.marisa marisa_data
mv *.json tmp_data
mv training_data data
mv marisa_data data
mv tmp_data data

cd wiki2w2v
./wiki2w2v.sh
cd ..

echo "Done extraction!"
