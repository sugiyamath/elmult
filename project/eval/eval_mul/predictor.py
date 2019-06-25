import os
import sys

import nltk
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

import candidate_generator as cg
import entvec_encoder as eenc
import preprocessor as pre

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def ngram(words, n):
    return list(zip(*(words[i:] for i in range(n))))


def feature(words, trie, kv, embedding_dict, n=6, k=30):
    X_list = []
    cand_list = []
    gram_list = []
    ind_list = []
    x1, x2 = pre.words_features(words, embedding_dict)
    for i in range(1, n):
        sent_mask = [0.0 for _ in range(len(words))]
        for wind, gram in zip(ngram(range(len(words)), i), ngram(words, i)):
            mention_words = list(gram)
            mention = ' '.join(mention_words)
            #x3, x4 = pre.words_features(mention_words, embedding_dict)
            candidates = cg.generate_with_linkprob_and_windex(
                mention, wind[0], wind[-1], trie, k=k)
            encoded = eenc.encode_with_linkprob_and_windex(candidates, kv)

            tmp_X1 = []
            tmp_X2 = []
            tmp_X3 = []
            #tmp_X4 = []
            tmp_X5 = []
            tmp_X6 = []
            tmp_cand = []
            tmp_ind = []
            tmp_gram = []
            for target in encoded:
                tmp_cand.append(target["candname"])
                tmp_ind.append((target["begin"], target["end"]))
                x3 = sent_mask[:]
                x3[target["begin"]:target["end"]] = [
                    1.0 for _ in range(target["end"] - target["begin"])
                ]
                x3 = np.array(x3, dtype=np.int32)
                tmp_X1.append(x1)
                tmp_X2.append(x2)
                tmp_X3.append(x3)
                #tmp_X4.append(x4)
                tmp_X5.append(target["entvec"])
                tmp_X6.append([target["linkprob"]])
                tmp_gram.append(mention)
            if tmp_gram:
                X_list.append([
                    pad_sequences(tmp_X1),
                    pre.my_pad_sequences(tmp_X2),
                    pad_sequences(tmp_X3),
                    np.array(tmp_X5),
                    np.array(tmp_X6)
                ])
                cand_list.append(tmp_cand)
                gram_list.append(tmp_gram)
                ind_list.append(tmp_ind)
    return X_list, cand_list, gram_list, ind_list


def predict(model, X_list, cand_list, gram_list, ind_list, threshold=0.5):
    out = []
    for X, cands, grams, wind in zip(X_list, cand_list, gram_list, ind_list):
        y_preds = [x[0] for x in model.predict(X)]
        if np.max(y_preds) < threshold:
            continue
        index = np.argmax(y_preds)
        out.append({
            "entity": cands[index],
            "mention": grams[index],
            "word_index": wind[index]
        })
    return out


if __name__ == "__main__":
    import gensim
    n_words = 300000
    trie = cg.load("../../model3/data/mention_stat.marisa")
    kv = eenc.load("../../model3/entity_vector/enwiki_20180420_100d.bin")
    model = load_model("./model_wiki.h5")
    word2vec = gensim.models.KeyedVectors.load("./train/GN300.kv", mmap="r")
    embedding_dict, embedding_matrix = pre.create_embedding_weights(
        word2vec, n_words)
    del (word2vec)
    del (embedding_matrix)

    sent = None
    threshold = None
    while sent != "-1":
        while(not isinstance(threshold, float)):
            threshold = float(input("threshold>"))
        sent = input("sent>")
        words = nltk.word_tokenize(sent)
        X_list, cand_list, gram_list, ind_list = feature(
            words, trie, kv, embedding_dict)
        result = predict(model, X_list, cand_list, gram_list, ind_list,
                         threshold)
        print(result)
        threshold = None
