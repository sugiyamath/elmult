wget -O dewiki.xml.bz2 https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2
wget -O itwiki.xml.bz2 https://dumps.wikimedia.org/itwiki/latest/itwiki-latest-pages-articles.xml.bz2
wget -O eswiki.xml.bz2 https://dumps.wikimedia.org/eswiki/latest/eswiki-latest-pages-articles.xml.bz2
wget -O frwiki.xml.bz2 https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2
wget -O enwiki.xml.bz2 https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

bzip2 -dk dewiki.xml.bz2 &
bzip2 -dk itwiki.xml.bz2 &
bzip2 -dk eswiki.xml.bz2 &
bzip2 -dk frwiki.xml.bz2 &
bzip2 -dk enwiki.xml.bz2 &

wait

mkdir dumps

mv *.xml dumps
mv *.bz2 dumps

