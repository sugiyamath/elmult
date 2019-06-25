import sys
import json
import candidate_generator as cg
import entvec_encoder as eenc
import nltk
import numpy as np
from predictor import feature
from preprocessor import create_embedding_weights


def generate_aida(datapath, trie, kv, embedding_dict):
    with open(datapath) as f:
        data = json.load(f)[:946]

    for doc in data:
        for d in doc:
            words, entities = d["sentence"], d["entities"]
            try:
                X, cands = feature(words, trie, kv, embedding_dict, n=10, k=50)
                y = [cand in entities for cand in cands]
            except:
                continue
            if True in y and X[0].shape[0] > 0 \
               and X[1].shape[0] > 0 \
               and X[2].shape[0] > 0 \
               and X[3].shape[0] > 0 \
               and X[4].shape[0] > 0:
                yield X, np.array(y)


def generate_wiki(wikipath, trie, kv, embedding_dict):
    with open(wikipath) as f:
        for line in f:
            try:
                sent, entities = line.strip().split("\t")
            except ValueError:
                continue
            if not sent.replace(" ", ""):
                continue
            entities = {x: True for x in entities.split(":::")}
            words = nltk.word_tokenize(sent)
            if len(words) > 128:
                continue
            try:
                X, cands = feature(words, trie, kv, embedding_dict)
                y = [cand in entities for cand in cands]
            except:
                continue
            if True in y and X[0].shape[0] > 0 \
               and X[1].shape[0] > 0 \
               and X[2].shape[0] > 0 \
               and X[3].shape[0] > 0 \
               and X[4].shape[0] > 0:
                yield X, np.array(y)


def load_data3(n_words=500000):
    import gensim
    trie = cg.load("../../../model3/data/mention_stat.marisa")
    kv = eenc.load("../../../model3/entity_vector/enwiki_20180420_100d.bin")
    #word2vec = gensim.models.KeyedVectors.load_word2vec_format(
    #    "../GoogleNews-vectors-negative300.bin", binary=True)
    #word2vec.save("GN300.kv")
    word2vec = gensim.models.KeyedVectors.load("./GN300.kv", mmap="r")
    embedding_dict, embedding_matrix = create_embedding_weights(
        word2vec, n_words)
    return trie, kv, embedding_dict, embedding_matrix


def load_data_general(n_words=3000000, lang="en"):
    import gensim
    trie = cg.load(
        "../wiki_processor/data/marisa_data/mention_stat_{}.marisa".format(
            lang))
    kv = eenc.load(
        "../wiki_processor/entity_vectors/{}wiki_20180420_100d.bin".format(
            lang))
    word2vec = gensim.models.KeyedVectors.load(
        "../wiki_processor/data/w2v_models/word2vec_{}.model".format(lang),
        mmap="r")
    embedding_dict, embedding_matrix = create_embedding_weights(
        word2vec, n_words)
    return trie, kv, embedding_dict, embedding_matrix
