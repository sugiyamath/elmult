import logging
from gensim.models import word2vec
import multiprocessing

if __name__ == "__main__":
    import sys
    lang = sys.argv[1]
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)
    sentences = word2vec.LineSentence('./wiki_{}.txt'.format(lang))
    model = word2vec.Word2Vec(sentences,
                              size=200,
                              workers=multiprocessing.cpu_count())
    model.save("word2vec_{}.model".format(lang))
