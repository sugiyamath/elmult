#!/bin/bash
wget http://wikipedia2vec.s3.amazonaws.com/models/de/2018-04-20/dewiki_20180420_100d.txt.bz2
wget http://wikipedia2vec.s3.amazonaws.com/models/it/2018-04-20/itwiki_20180420_100d.txt.bz2
wget http://wikipedia2vec.s3.amazonaws.com/models/es/2018-04-20/eswiki_20180420_100d.txt.bz2
wget http://wikipedia2vec.s3.amazonaws.com/models/fr/2018-04-20/frwiki_20180420_100d.txt.bz2
wget http://wikipedia2vec.s3.amazonaws.com/models/en/2018-04-20/enwiki_20180420_100d.txt.bz2

bzip2 -dk dewiki_20180420_100d.txt.bz2 &
bzip2 -dk itwiki_20180420_100d.txt.bz2 &
bzip2 -dk eswiki_20180420_100d.txt.bz2 &
bzip2 -dk frwiki_20180420_100d.txt.bz2 &
bzip2 -dk enwiki_20180420_100d.txt.bz2 &

wait

mkdir entity_vectors
mv *100d.txt* entity_vectors

echo "Done!"

